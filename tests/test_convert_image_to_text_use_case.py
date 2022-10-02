import unittest
from manga_translator.application.use_cases.convert_image_to_text import ConvertImageToTextUseCase

from manga_translator.infra.adapters.ocr.implementations.cloud_vision import CloudVision
from manga_translator.infra.adapters.ocr.interfaces import TextBlock
from manga_translator.utils.handlers.error.api_error import ApiError


class TestConvertImageToTextUseCase(unittest.TestCase):
    def test_load_file(self):
        sut = ConvertImageToTextUseCase(ocr_service=CloudVision(service_account_path='/home/alexandresenpai/credentials/GCP/manga.json'))
        image_bytes = sut.load_file(image_path='./tests/static/image_1.jpg')
        self.assertIsNotNone(image_bytes)
        self.assertIsInstance(image_bytes, bytes)
    
    def test_raise_error_inexistent_file(self):
        sut = ConvertImageToTextUseCase(ocr_service=CloudVision(service_account_path='/home/alexandresenpai/credentials/GCP/manga.json'))
        with self.assertRaises(ApiError) as context:
            sut.load_file(image_path='./tests/static/image.jpg')
        self.assertIsNotNone(context.exception)
            
    def test_return_text_blocks_from_image(self):
        sut = ConvertImageToTextUseCase(ocr_service=CloudVision(service_account_path='/home/alexandresenpai/credentials/GCP/manga.json'))
        image_bytes = sut.load_file(image_path='./tests/static/image_1.jpg')
        text_blocks = sut.extract_text_from_image(image=image_bytes)
        self.assertIsNotNone(text_blocks)
        self.assertIsInstance(text_blocks[0], TextBlock)

if __name__ == '__main__':
    unittest.main()