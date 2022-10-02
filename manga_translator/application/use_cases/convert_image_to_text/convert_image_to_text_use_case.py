import io
import os
from typing import List

from manga_translator.application.use_cases.convert_image_to_text.interfaces import Dimensions, Image, ImageToTextResponseDTO, ImageToTextRequestDTO, Position, TextBlock, TranslatorResponse
from manga_translator.infra.adapters.image_editor.image_editor_interface import ImageEditorInterface
from manga_translator.infra.adapters.ocr.ocr_interface import OCRInterface
from manga_translator.infra.adapters.storage.storage_interface import StorageInterface
from manga_translator.infra.adapters.translator.translator_interface import TranslatorInterface
from manga_translator.utils.handlers.error.api_error import ApiError


class ConvertImageToTextUseCase:
    def __init__(self, 
                 ocr_service: OCRInterface,
                 translate_service: TranslatorInterface,
                 image_editor_service: ImageEditorInterface,
                 drive_service: StorageInterface):
        self._ocr_service = ocr_service
        self._translate_service = translate_service
        self._image_editor_service = image_editor_service
        self._drive_service = drive_service
    
    def extract_text_from_image(self, image: bytes) -> List[TextBlock]:
        image_to_text = self._ocr_service.extract_text(image)
        return [TextBlock(text=block.text, position=block.position, area=block.area) for block in image_to_text.blocks]
    
    def load_file(self, image_path: str) -> bytes:
        if not os.path.isfile(image_path): raise ApiError.resource_not_found(message='Could not find any valid file at path: {}'.format(image_path))
        return io.open(image_path, 'rb').read()
    
    def translate_text(self, text: str, target_language: str, source_language: str=None) -> TranslatorResponse:
        return self._translate_service.translate(text=text,
                                                 target_language=target_language,
                                                 source_language=source_language)

    def execute(self, image_information: ImageToTextRequestDTO) -> ImageToTextResponseDTO:
        if image_information.image_path is not None:
            image = self.load_file(image_path=image_information.image_path)
        else:
            image = image_information.image_bytes
        
        text_blocks = self.extract_text_from_image(image=image)

        for block in text_blocks:
            translated = self.translate_text(text=block.text,
                                             target_language='pt-br')
            block.set_translated_text(translated_text=translated.translated_text)

        image = self._image_editor_service.cover_old_text_with_dialog_boxes(image=io.BytesIO(image), text_blocks=text_blocks)
        image = self._image_editor_service.set_translated_text_to_image(image=image, text_blocks=text_blocks)

        self._drive_service.upload(image=image, path='./teste.png')

        return ImageToTextResponseDTO(image=Image(image_path=image_information.image_path, 
                                                  image_extension='',
                                                  dimensions=Dimensions(width=0, height=0)),
                                      text_blocks=text_blocks)