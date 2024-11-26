from flask import Flask, request, jsonify
import hmac
import hashlib
import base64
import time
import random
import string
import urllib.parse
import requests
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load the trained h5 model
MODEL = tf.keras.models.load_model('model_freshgrocie.h5')

# Define the class mapping
class_mapping = {
    0: {'name': 'Apple', 'id': 5367},
    1: {'name': 'Banana', 'id': 5388},
    2: {'name': 'Bellpepper', 'id': 285829},
    3: {'name': 'Carrot', 'id': 6034},
    4: {'name': 'Cucumber', 'id': 6244},
    5: {'name': 'Mango', 'id': 5436},
    6: {'name': 'Orange', 'id': 5271},
    7: {'name': 'Potato', 'id': 5718},
    8: {'name': 'Strawberry', 'id': 5525},
    9: {'name': 'Tomato', 'id': 6138},
    10: {'name': 'Rotten Apple', 'id': 0},
    11: {'name': 'Rotten Banana', 'id': 0},
    12: {'name': 'Rotten Bellpepper', 'id': 0},
    13: {'name': 'Rotten Carrot', 'id': 0},
    14: {'name': 'Rotten Cucumber', 'id': 0},
    15: {'name': 'Rotten Mango', 'id': 0},
    16: {'name': 'Rotten Orange', 'id': 0},
    17: {'name': 'Rotten Potato', 'id': 0},
    18: {'name': 'Rotten Strawberry', 'id': 0},
    19: {'name': 'Rotten Tomato', 'id': 0},
}

class FatSecretClient:
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.base_url = 'https://platform.fatsecret.com/rest/server.api'

    def generate_nonce(self, length=10):
        """Generate a random nonce string."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def create_signature_base_string(self, method, params):
        """Create the signature base string as per FatSecret documentation."""
        # Sort parameters alphabetically
        sorted_params = sorted(params.items(), key=lambda x: (x[0], x[1]))
        
        # Create normalized parameter string
        param_string = "&".join(f"{urllib.parse.quote(str(k))}={urllib.parse.quote(str(v))}" 
                              for k, v in sorted_params)
        
        # Create signature base string
        signature_base = "&".join([
            method.upper(),
            urllib.parse.quote(self.base_url, safe=''),
            urllib.parse.quote(param_string, safe='')
        ])
        
        return signature_base

    def generate_signature(self, signature_base_string, access_secret=""):
        """Generate HMAC-SHA1 signature."""
        # Create key by combining consumer secret and access secret with &
        key = f"{urllib.parse.quote(self.consumer_secret, safe='')}&{access_secret}"
        
        # Generate signature using HMAC-SHA1
        raw_hmac = hmac.new(
            key.encode('utf-8'),
            signature_base_string.encode('utf-8'),
            hashlib.sha1
        ).digest()
        
        # Base64 encode the HMAC value
        signature = base64.b64encode(raw_hmac).decode('utf-8')
        
        return signature

    def make_request(self, method='GET', api_method='foods.search', **additional_params):
        """Make a request to the FatSecret API."""
        # Prepare OAuth parameters
        oauth_params = {
            'oauth_consumer_key': self.consumer_key,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(time.time())),
            'oauth_nonce': self.generate_nonce(),
            'oauth_version': '1.0',
            'method': api_method,
            'format': 'json'
        }
        
        # Add additional parameters
        params = {**oauth_params, **additional_params}
        
        # Generate signature base string
        signature_base_string = self.create_signature_base_string(method, params)
        
        # Generate signature
        signature = self.generate_signature(signature_base_string)
        
        # Add signature to parameters
        params['oauth_signature'] = signature
        
        # Make the request
        if method.upper() == 'POST':
            response = requests.post(self.base_url, data=params)
        else:
            response = requests.get(self.base_url, params=params)
            
        return response.json()

# Initialize Flask app with FatSecret client
fatsecret = FatSecretClient(
    consumer_key='<input consumer key>',
    consumer_secret='<input consumer secret>'
)

def map_nutrition_details(serving):
  nutrition_details = {
    'calcium': f"{serving['calcium']}%",
    'calories': f"{serving['calories']}kcal",
    'carbohydrate': f"{serving['carbohydrate']}g",
    'cholesterol': f"{serving['cholesterol']}mg",
    'fat': f"{serving['fat']}g",
    'fiber': f"{serving['fiber']}g",
    'iron': f"{serving['iron']}%",
    'monounsaturated_fat': f"{serving['monounsaturated_fat']}g",
    'polyunsaturated_fat': f"{serving['polyunsaturated_fat']}g",
    'potassium': f"{serving['potassium']}mg",
    'protein': f"{serving['protein']}g",
    'saturated_fat': f"{serving['saturated_fat']}g",
    'sodium': f"{serving['sodium']}mg",
    'sugar': f"{serving['sugar']}g",
    'vitamin_a': f"{serving['vitamin_a']}%",
    'vitamin_c': f"{serving['vitamin_c']}%",
  }
  
  return nutrition_details
  
# Step 4: Make a request to the FatSecret API
def get_food_data(food_id):
  try:
      result = fatsecret.make_request(
          method='GET',
          api_method='food.get',
          food_id=str(food_id)
      )
      
      food_data = result['food']
      
      servings = food_data['servings']['serving']
      serving = next((serving for serving in servings if serving['serving_description'] == '100 g'), None) or servings
      
      food_detail = {
        'detail': serving['serving_url'],
        'nutrition_detail': map_nutrition_details(serving)
      }
      
      return food_detail
  except Exception as e:
      return {'error': str(e)}

@app.route('/')
def hello(): 
    return "Model API is running"

@app.route('/predict', methods=['POST'])
def predict():
  try:
    image = request.files['gambar']
    img = Image.open(image)
    
    if img.mode == 'RGBA':
      img = img.convert('RGB')
            
    img = img.resize((150, 150))

    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    pred = MODEL.predict(img_array)
    
    # Get the predicted class or label
    predicted_class = np.argmax(pred)
    
    # Map the predicted class index to the corresponding food name
    if predicted_class in class_mapping:
        food_name = class_mapping[predicted_class]['name']
        food_id = class_mapping[predicted_class]['id']
    else:
        food_name = 'unknown'

    # Retrieve the nutrition information
    if food_id == 0:
      food_data = {
        'detail': None,
        'nutrition_detail': None
      }
      
    else:
      food_data = get_food_data(food_id)

    response = {
        'name': food_name,
        **food_data
    }

    img.close()

    return jsonify(response)
  except Exception as e:
    print(str(e))
    return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')