import numpy as np
import os
import tensorflow as tf
from ..configs import ModelDownloader
from ..utils import class_mapping


class PredictionService:
    def __init__(self, model_path):
        # Check if model exists locally before downloading
        if not os.path.exists(model_path):
            try:
                # Synchronous download
                model_dowloader = ModelDownloader()
                model_dowloader.download_model()
            except Exception as e:
                print(f"Error downloading model: {e}")
                raise

        # Only load model after confirmed download
        try:
            self.model = tf.keras.models.load_model(model_path)
            print("Model load success")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def preprocess_image(self, image):
        if image.mode == "RGBA":
            image = image.convert("RGB")

        image = image.resize((150, 150))

        img_array = np.array(image)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        return img_array

    def predict(self, image):
        preprocessed_image = self.preprocess_image(image)
        prediction = self.model.predict(preprocessed_image)

        # Get the predicted index
        predicted_class = np.argmax(prediction)

        # Map the predicted class index to the corresponding food name
        if predicted_class in class_mapping:
            food_name = class_mapping[predicted_class]["name"]
            food_id = class_mapping[predicted_class]["id"]
        else:
            food_name = "unknown"
            food_id = 0

        return food_name, food_id
