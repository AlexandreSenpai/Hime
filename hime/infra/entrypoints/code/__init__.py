from hime.application.use_cases.translate_image import TranslateImageUseCase
from hime.infra.adapters.image_editor.implementations.pillow import Pillow
from hime.infra.adapters.ocr.implementations.cloud_vision import CloudVision
from hime.infra.adapters.translator.implementations.google_translator import GoogleTranslate

class TranslateImageUseCaseFactory:
    @staticmethod
    def create() -> TranslateImageUseCase:
        return TranslateImageUseCase(ocr_service=CloudVision(service_account_path='/home/alexandresenpai/credentials/GCP/manga.json'),
                                     translator=GoogleTranslate(service_account_path='/home/alexandresenpai/credentials/GCP/manga.json'),
                                     image_editor_service=Pillow())