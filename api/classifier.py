from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import config

endpoint = config.ENDPOINT
project_id = config.PROJECT_ID
iteration_name = config.ITERATION_NAME
prediction_key = config.PREDICTION_KEY


def find_seal(image_path):
    predictor = CustomVisionPredictionClient(prediction_key, endpoint=endpoint)

    # Open the image and get back the prediction results.
    with open(image_path, mode="rb") as image_contents:
        results = predictor.classify_image(
            project_id, iteration_name, image_contents)

    return results.predictions
