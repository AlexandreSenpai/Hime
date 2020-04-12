###[BUILT-IN MODULES]###
import six
###[EXTERNAL MODULES]###
from google.cloud import translate_v2 as translate 
###[PERSONAL MODULES]###

class Translate(object):
    def __init__(self):
        self.client = translate.Client()

    def __repr__(self):
        return 'Class made to translate text.'

    def translate(self, text, target_language):
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        result = self.client.translate(
        text, target_language=target_language)
        
        return result['translatedText']