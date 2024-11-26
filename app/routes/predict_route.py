from flask import Blueprint, jsonify, request
from ..controllers import PredictController
from ..configs import Config, FatSecretClient

predict_route = Blueprint('predict', __name__) # or named it as predict_bp

fatsecret_client = FatSecretClient(
      Config.FATSECRET_CONSUMER_KEY, 
      Config.FATSECRET_CONSUMER_SECRET,
      Config.FATSECRET_BASE_URL
  )

predict_controller = PredictController(fatsecret_client)

@predict_route.route('/predict', methods=['POST'])
def predict():
  try:
    image_file = request.files['image']
    
    result = predict_controller.predict(image_file)
    
    return result
  except Exception as e:
    return jsonify({'error': str(e)}), 500
