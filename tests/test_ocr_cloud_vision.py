import io
import unittest

from manga_translator.infra.adapters.ocr.implementations.cloud_vision import CloudVision
from manga_translator.infra.adapters.ocr.interfaces import ImageToText


class TestCloudVision(unittest.TestCase):
    def test_cloud_vision_get_authenticated_client(self):
        vision = CloudVision(service_account_path='/home/alexandresenpai/credentials/GCP/manga.json')
        self.assertIsNotNone(vision.client)
    
    def test_get_text_from_image(self):
        vision = CloudVision(service_account_path='/home/alexandresenpai/credentials/GCP/manga.json')
        image = io.open('./tests/static/image_1.jpg', 'rb')
        text_blocks = vision.extract_text(image=image.read())
        image.close()
        self.assertIsNotNone(text_blocks)
        self.assertIsNotNone(text_blocks.image)
        self.assertGreater(len(text_blocks.blocks), 0)
        self.assertIsInstance(text_blocks, ImageToText)
        

if __name__ == '__main__':
    unittest.main()