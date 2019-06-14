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
            image_path = os.path.join(dirs, file)
            print image_name
            print image_path
            exit(1)

            predictions = find_seal(image_path)
            print predictions

            save_json_file(subdir, image_name, predictions)


def save_json_file(path, image, predictions):
    json_data = {
        data: predictions
    }
    with open(path + image + '.json', 'w') as fp:
        json.dump(json_data, fp)


if __name__ == '__main__':
    test_images_against_classifier()
