from flask import Flask, request, jsonify
import requests
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load the trained h5 model
MODEL = tf.keras.models.load_model('model_freshgrocie.h5')

# Define the class mapping
class_mapping = {
    0: 'Apple',
    1: 'Banana',
    2: 'Bellpepper',
    3: 'Carrot',
    4: 'Cucumber',
    5: 'Mango',
    6: 'Orange',
    7: 'Potato',
    8: 'Strawberry',
    9: 'Tomato',
    10: 'Rotten Apple',
    11: 'Rotten Banana',
    12: 'Rotten Bellpepper',
    13: 'Rotten Carrot',
    14: 'Rotten Cucumber',
    15: 'Rotten Mango',
    16: 'Rotten Orange',
    17: 'Rotten Potato',
    18: 'Rotten Strawberry', 
    19: 'Rotten Tomato'
    # Add the rest of the class mappings for your 20 classes
}

# Set up FatSecret API credentials
API_KEY = '47536e6dddad4029a53803e647f617a1'
API_SECRET = '6c4a025652754296a885dfb5caaf9f02'

# Step 4: Make a request to the FatSecret API
def get_nutrition_info(food_name):
    url = 'https://platform.fatsecret.com/rest/server.api'
    params = {
        'method': 'foods.search',
        'search_expression': food_name,
        'format': 'json',
        'oauth_consumer_key': API_KEY,
        'oauth_signature': API_SECRET
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'foods' in data and 'food' in data['foods']:
        food = data['foods']['food'][0]  # Assuming the first search result is the desired food
        food_id = food['food_id']

        # Request nutrition information for the food
        params = {
            'method': 'food.get',
            'food_id': food_id,
            'format': 'json',
            'oauth_consumer_key': API_KEY,
            'oauth_signature': API_SECRET
        }
        response = requests.get(url, params=params)
        nutrition_data = response.json()
        return nutrition_data

    return None

# Step 5: Parse and prepare the nutrition information response
def prepare_response(food_name, nutrition_data):
    serving_size = nutrition_data['food']['servings']['serving'][0]['serving_description']
    calories = nutrition_data['food']['servings']['serving'][0]['calories']
    # Extract other relevant nutrition information as needed
    
    response = {
        'food_name': food_name,
        'serving_size': serving_size,
        'calories': calories
        # Include other nutrition information in the response
    }
    return response

@app.route('/')
def hello(): 
    return "Hello, this is a test"

@app.route('/predict', methods=['POST'])
def predict():
    image = request.files['gambar']
    img = Image.open(image)
    img = img.resize((150, 150))

    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255

    pred = MODEL.predict(img_array)

    # Get the predicted class or label
    predicted_class = np.argmax(pred)

    # Map the predicted class index to the corresponding food name
    if predicted_class in class_mapping:
        food_name = class_mapping[predicted_class]
    else:
        food_name = 'unknown'

    # Retrieve the nutrition information
    nutrition_data = get_nutrition_info(food_name)

    # Prepare the response with nutrition information
    if nutrition_data is not None:
        serving_size = nutrition_data['food']['servings']['serving'][0]['serving_description']
        calories = nutrition_data['food']['servings']['serving'][0]['calories']
        # Extract other relevant nutrition information as needed

        response = {
            'food_name': food_name,
            'serving_size': serving_size,
            'calories': calories
            # Include other nutrition information in the response
        }
    else:
        # Handle case when nutrition information is not available
        response = {
            'food_name': food_name,
            'serving_size': 'N/A',
            'calories': 'N/A',
            'message': 'Nutrition information not available'
        }

    img.close()

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')