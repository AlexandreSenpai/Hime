###[BUILT-IN MODULES]###
import io
import pickle
###[EXTERNAL MODULES]###
import cv2
from google.cloud import vision
from google.cloud.vision import types
###[PERSONAL MODULES]###

class Vision(object):
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
        self.text_blocks = []

    def __repr__(self):
        return 'Class made to scan and recognize text in images.'

    def detect_text(self, image_path):
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        response = self.client.text_detection(image=image)

        """
        # added this so we don't need to send requests for google when testing
        with open("response_test.txt", "rb") as response_file:
            response = pickle.load(response_file)
        """

        texts = response.full_text_annotation
        for block in texts.pages[0].blocks:
            block_text = ''
            coords = block.bounding_box.vertices
            cv2.rectangle(img, (coords[0].x - 5, coords[0].y - 5), (coords[2].x + 5, coords[2].y + 5), (255, 255, 255), -1)
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        block_text += str(symbol.text)
                    block_text += ' '
            self.text_blocks.append({"text": block_text, "area": ((coords[0].x, coords[0].y), (coords[2].x, coords[2].y)), "text_box_size": (coords[2].x - coords[0].x, coords[2].y - coords[0].y)})
        return (img, self.text_blocks)

if __name__ == '__main__':
    vision = Vision()
    vision.detect_text('./teste1.png')


