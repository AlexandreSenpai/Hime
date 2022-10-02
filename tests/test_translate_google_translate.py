import unittest

from manga_translator.infra.adapters.translator.implementations.google_translator import GoogleTranslate
from manga_translator.infra.adapters.translator.interfaces import TranslatorResponse


class TestGoogleTranslate(unittest.TestCase):
    def test_cloud_vision_get_authenticated_client(self):
        sut = GoogleTranslate(service_account_path='/home/alexandresenpai/credentials/GCP/manga.json')
        self.assertIsNotNone(sut.client)
    
    def test_translate_text(self):
        sut = GoogleTranslate(service_account_path='/home/alexandresenpai/credentials/GCP/manga.json')
        translate_response = sut.translate(text='Hello, friend!', target_language='pt-br', source_language='en')
        
        self.assertIsNotNone(translate_response)
        self.assertEqual(translate_response.translated_text, 'Olá amiga!')
        self.assertEqual(translate_response.original_text, 'Hello, friend!')
        self.assertIsInstance(translate_response, TranslatorResponse)
        

if __name__ == '__main__':
    unittest.main()