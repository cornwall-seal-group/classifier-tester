import os
import json
import config
from api.classifier import find_seal

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


def test_images_against_classifier():
    print 'test_images_against_classifier'
    for subdir, dirs, files in os.walk(TEST_IMAGE_FOLDER):

        for file in files:
            image_name = file.replace('.jpg', '')
            image_path = os.path.join(subdir, file)

            results = find_seal(image_path)
            json_predictions = {}

            for prediction in results.predictions:
                json_predictions[prediction.tag_name] = prediction.probability
                print ("\t" + prediction.tag_name +
                       ": {0:.2f}%".format(prediction.probability * 100))

            print json_predictions
            save_json_file(subdir, image_name, json_predictions)
            exit(1)


def save_json_file(path, image, predictions):

    with open(path + image + '.json', 'w') as fp:
        json.dump(predictions, fp)


if __name__ == '__main__':
    test_images_against_classifier()
