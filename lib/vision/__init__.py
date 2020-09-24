###[BUILT-IN MODULES]###
from typing import Tuple
import io
import os
# import pickle
###[EXTERNAL MODULES]###
from PIL import Image, ImageDraw
from google.cloud import vision
from google.cloud.vision import types
###[PERSONAL MODULES]###


class Vision:
    def __init__(self, service_account: str = None):
        self._credentials = self._set_service_account(path=service_account)
        self.client = vision.ImageAnnotatorClient()
        self.text_blocks = []

    def __repr__(self):
        return 'Class made to scan and recognize text in images.'

    def _set_service_account(self, path: str):
        if path is not None:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path

    def detect_text(self, image_path: str) -> (Tuple[Image.open, list]):

        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image_bytes = types.Image(content=content)
        image = Image.open(io.BytesIO(content)).convert('L')
        canvas = ImageDraw.Draw(image)

        response = self.client.text_detection(image=image_bytes)

        # # added this so we don't need to send requests for google when testing
        # with open("response_test.txt", "rb") as response_file:
        #     response = pickle.load(response_file)

        texts = response.full_text_annotation
        for block in texts.pages[0].blocks:

            block_text = ''
            coords = block.bounding_box.vertices
            coord1 = (coords[0].x - 5, coords[0].y - 3)
            coord2 = (coords[2].x + 5, coords[2].y + 5)

            # filling the old space with background color
            # canvas.rectangle([coord1, coord2], fill=130)
            canvas.rectangle([coord1, coord2], fill=image.getpixel((coord1[0] + 10, coord1[1] - 5)))

            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        block_text += str(symbol.text)
                    block_text += ' '

            self.text_blocks.append({
                "text": block_text,
                "font_color": image.getpixel((coord1[0] + 10, coord1[1] - 5)),
                "area": (
                    (coords[0].x - 5, coords[0].y),
                    (coords[2].x - 5, coords[2].y)
                ),
                "text_box_size": (
                    coords[2].x - coords[0].x,
                    coords[2].y - coords[0].y
                )
            })

        # image.save('./blank.png', 'png')

        return (image, self.text_blocks)


if __name__ == '__main__':
    vision = Vision(service_account=r'C:\Users\alexa\Documents\GCP\manga.json')
    vision.detect_text('./images/sample1.jpg')
