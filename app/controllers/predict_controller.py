from flask import jsonify
from PIL import Image
from ..configs import Config
from ..services import NutritionService, PredictionService


class PredictController:
    def __init__(self):
        self.nutrition_service = NutritionService()
        self.prediction_service = PredictionService(Config.MODEL_PATH)

    def predict(self, image_file):
        if image_file is None:
            return jsonify({"error": "No image uploaded"}), 400

        image = Image.open(image_file)

        food_name, food_id = self.prediction_service.predict(image)
        nutrition_detail = self.nutrition_service.get_nutrition_detail(food_id)

        if food_id == 0:
            nutrition_data = {"detail": None, "nutrition_detail": None}

        else:
            nutrition_data = nutrition_detail

        response = {"name": food_name, **nutrition_data}

        return response
