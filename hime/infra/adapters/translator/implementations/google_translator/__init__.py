import six

from google.cloud import translate_v2 as translate

from hime.application.core.entities.translation import Language, Translation
from hime.application.core.utils.handlers.error.api_error import ApiError

class GoogleTranslate:
    _client: translate.Client = None

    def __init__(self, service_account_path: str = None):
        self._client = self._get_client_authenticated(service_account_path=service_account_path)
    
    @property
    def client(self) -> translate.Client:
        return self._client

    def _get_client_authenticated(self, service_account_path: str) -> translate.Client:
        if service_account_path is not None:
            return translate.Client.from_service_account_json(service_account_path)
        return translate.Client()
    
    def translate(self, text: str, language: Language) -> Translation:
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        try:
            translation = self.client.translate(text, target_language=language.target, source_language=language.source)
            return Translation(language=language,
                               text=translation.get('translatedText', ''),
                               original=text)
        except Exception as err:
            raise ApiError.comunication_error(message='Something went wrong while trying to translate text',
                                              payload={'text': text, 
                                                       'target_language': language.target,
                                                       'source_language': language.source}, 
                                              stack_trace=err.message)