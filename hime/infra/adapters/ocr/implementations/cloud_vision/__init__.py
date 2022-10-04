from typing import Any
from google.cloud import vision

from hime.application.core.entities.image import Image
from hime.application.core.entities.ocr_analysis import OCRAnalysis, Position, Area, Symbols, TextBlock

class CloudVision:
    _client: vision.ImageAnnotatorClient = None

    def __init__(self, service_account_path: str = None):
        self._client = self._get_client_authenticated(service_account_path=service_account_path)
    
    @property
    def client(self) -> vision.ImageAnnotatorClient:
        return self._client

    def _get_client_authenticated(self, service_account_path: str) -> vision.ImageAnnotatorClient:
        if service_account_path is not None:
            return vision.ImageAnnotatorClient.from_service_account_json(filename=service_account_path)
        return vision.ImageAnnotatorClient()
    
    def extract_text_left_top_coords(self, bounding_box: Any) -> Position:
        return Position(x=bounding_box.vertices[0].x, y=bounding_box.vertices[0].y)
    
    def extract_text_area(self, bounding_box: Any) -> Area:
        return Area(width=bounding_box.vertices[2].x - bounding_box.vertices[0].x,
                    height=bounding_box.vertices[2].y - bounding_box.vertices[0].y)

    def extract_text_from_paragraphs(self, paragraphs: Any) -> str:
        text = ''
        for paragraph in paragraphs:
            for word in paragraph.words:
                for symbol in word.symbols:
                    text += symbol.text
                    if (text_break := symbol.property.detected_break) is not None:
                        if str(text_break.type_) == 'BreakType.SPACE':
                            text += Symbols.SPACE.value
                        if str(text_break.type_) == 'BreakType.EOL_SURE_SPACE':
                            text += Symbols.SPACE.value
        return text
    
    def extract_text(self, image: Image) -> OCRAnalysis:
        vision_image = vision.Image(content=bytes(image.content.getbuffer()))
        response = self.client.text_detection(image=vision_image)
        text_blocks = response.full_text_annotation
        
        imageToText = OCRAnalysis()
        
        if not text_blocks: return imageToText
        
        for text_block in text_blocks.pages[0].blocks:
            current_text_block = TextBlock(text=self.extract_text_from_paragraphs(paragraphs=text_block.paragraphs),
                                           position=self.extract_text_left_top_coords(bounding_box=text_block.bounding_box),
                                           area=self.extract_text_area(bounding_box=text_block.bounding_box))
            imageToText.blocks.append(current_text_block)
        
        return imageToText
