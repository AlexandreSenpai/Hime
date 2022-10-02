from dataclasses import dataclass
from typing import List

from hime.application.core.entities.image import Image
from hime.application.core.entities.translation import Language
from hime.infra.adapters.image_editor.image_editor_interface import ImageEditorInterface
from hime.infra.adapters.ocr.ocr_interface import OCRInterface
from hime.infra.adapters.translator.translator_interface import TranslatorInterface

@dataclass
class LanguageOptions:
    source: str
    target: str

@dataclass
class TranslateImageRequestDTO:
    language: LanguageOptions
    images: List[str]

class TranslateImageUseCase:
    
    def __init__(self,
                 ocr_service: OCRInterface,
                 translator: TranslatorInterface,
                 image_editor_service: ImageEditorInterface):
        self.ocr_service = ocr_service
        self.translator = translator
        self.image_editor_service = image_editor_service
        
    def get_text_blocks_from_image(self, images: List[Image]) -> List[Image]:
        return [image.set_ocr_analysis(self.ocr_service.extract_text(image)) for image in images]
    
    def translate_text_blocks_from_image(self, images: List[Image]) -> List[Image]:
        for image in images:
            for block in image.ocr_analysis.blocks:
                translation = self.translator.translate(text=block.text, 
                                                                language=Language(source='en-US', target='pt-BR'))
                block.set_translation(translation)
        return images
        
    def execute(self, data: TranslateImageRequestDTO):
        
        images = [Image().load(image_path) for image_path in data.images]
        
        images_with_ocr_analysis = self.get_text_blocks_from_image(images=images)
        images_with_translations = self.translate_text_blocks_from_image(images=images_with_ocr_analysis)
        
        blank_images = [self.image_editor_service.cover_old_text_with_dialog_boxes(image) for image in images_with_translations]
        final_images = [self.image_editor_service.set_translated_text_to_image(image) for image in blank_images]
    
        final_images[0].save()
        
        
        
        

    
        
        