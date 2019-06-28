import os
import csv
import json
import config
from api.classifier import find_seal

ALLOWED_EXTENSIONS = set(['jpg'])
ITERATION = config.ITERATION
TEST_IMAGE_FOLDER = '../classifier-test-images/' + ITERATION + '/'


#
# FOLDER STRUCTURE:
#
# classifier-test-images/
#    {iteration}/
#              LF1/
#                  image1-0.32.jpg
#                  image2-0.22.jpg
#              LF4/
#                  image1-0.94.jpg
#                  image2-0.65.jpg

# Get the iteration ID to know which folders to look through
# Loop through the seal folders and each image in it
# Submit each image to the classifier and store the result in a JSON file with the same image name
# Save JSON of results as:
# {
#     "LF1": {
#         "image_name.jpg": {
#             "predictions": {}
#         }
#     }
# }


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def test_images_against_classifier():
    print 'test_images_against_classifier'
    seals = {}
    for subdir, dirs, files in os.walk(TEST_IMAGE_FOLDER):

        if subdir not in seals:
            seals[subdir] = {}

        for file in files:
            if allowed_file(file):

                seals[subdir][file] = {}

                image_path = os.path.join(subdir, file)

                results = find_seal(image_path)
                json_predictions = {}

                for prediction in results.predictions:
                    json_predictions[prediction.tag_name] = prediction.probability
                    print ("\t" + prediction.tag_name +
                           ": {0:.2f}%".format(prediction.probability * 100))

                seals[subdir][file] = json_predictions

        save_seals_to_json(seals)


def save_seals_to_json(seals):
    seal_name_file = 'seals.json'
    file_path = TEST_IMAGE_FOLDER + '/' + seal_name_file
    with open(file_path, 'w') as json_file:
        json.dump(seals, json_file)


if __name__ == '__main__':
    test_images_against_classifier()
