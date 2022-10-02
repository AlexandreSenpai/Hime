from manga_translator.application.use_cases.convert_image_to_text.convert_image_to_text_use_case import ConvertImageToTextUseCase
from manga_translator.application.use_cases.convert_image_to_text.convert_image_to_text_controller import ConvertImageToTextController
from manga_translator.infra.adapters.image_editor.implementations.pillow import Pillow 

from manga_translator.infra.adapters.ocr.implementations.cloud_vision import CloudVision
from manga_translator.infra.adapters.storage.implementations.file_system import FileSystem
from manga_translator.infra.adapters.translator.implementations.google_translator import GoogleTranslate

convert_image_to_text_use_case = ConvertImageToTextUseCase(CloudVision(service_account_path='/home/alexandresenpai/credentials/GCP/manga.json'),
                                                           GoogleTranslate(service_account_path='/home/alexandresenpai/credentials/GCP/manga.json'),
                                                           Pillow(),
                                                           FileSystem())
convert_image_to_text_controller = ConvertImageToTextController(convert_image_to_text_use_case=convert_image_to_text_use_case)