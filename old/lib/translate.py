###[BUILT-IN MODULES]###
import six
###[EXTERNAL MODULES]###
from google.cloud import translate_v2 as translate 
###[PERSONAL MODULES]###
from .authenticator import Auth

class Translate(Auth):
    def __init__(self, credentials_path):
        super().__init__(service=translate.Client,
                         credentials_path=credentials_path)

    def __repr__(self):
        return 'Class made to translate text.'

    def translate(self, text: str, target_language: str) -> (dict):
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        result = self.client.translate(
        text, target_language=target_language)
        
        return result['translatedText']