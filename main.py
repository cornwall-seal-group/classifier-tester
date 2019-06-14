import os
import csv
import json
import config
from api.classifier import find_seal

ALLOWED_EXTENSIONS = set(['jpg'])
ITERATION = config.ITERATION
TEST_IMAGE_FOLDER = '../classifier-test-images/' + ITERATION + '/'


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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def test_images_against_classifier():
    print 'test_images_against_classifier'
    seals = []
    for subdir, dirs, files in os.walk(TEST_IMAGE_FOLDER):

        if subdir not in seals:
            seals[subdir] = []

        for file in files:
            if allowed_file(file):

                seals[subdir].append(file)

                image_name = file.replace('.jpg', '')
                image_path = os.path.join(subdir, file)

                results = find_seal(image_path)
                json_predictions = {}

                for prediction in results.predictions:
                    json_predictions[prediction.tag_name] = prediction.probability
                    print ("\t" + prediction.tag_name +
                           ": {0:.2f}%".format(prediction.probability * 100))

                save_json_file(subdir, image_name, json_predictions)

        save_seals_to_csv(seals)


def save_json_file(path, image, predictions):
    json_path = os.path.join(path, image) + '.json'
    with open(json_path, 'w') as fp:
        json.dump(predictions, fp)


def save_seals_to_csv(seals):
    seal_name_file = 'seals.csv'
    file_path = TEST_IMAGE_FOLDER + '/' + seal_name_file
    with open(file_path, 'w') as csv_file:
        for key in seals.keys():
            csv_file.write("%s,%s\n" % (key, ''.join(seals[key])))


if __name__ == '__main__':
    test_images_against_classifier()
