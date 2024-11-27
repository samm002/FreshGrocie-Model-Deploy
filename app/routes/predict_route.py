from flask import Blueprint, jsonify, request
from ..controllers import PredictController

predict_route = Blueprint("predict", __name__)  # or named it as predict_bp

predict_controller = PredictController()


@predict_route.route("/predict", methods=["POST"])
def predict():
    try:
        image_file = request.files["image"]

        result = predict_controller.predict(image_file)

        return result
    except Exception as e:
        return jsonify({"error": str(e)}), 500
