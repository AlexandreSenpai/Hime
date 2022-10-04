from dataclasses import dataclass, field
import datetime
from io import BytesIO, open
import os

from PIL import Image as PilImage

from hime.application.core.entities.entity import Entity
from hime.application.core.entities.ocr_analysis import OCRAnalysis
from hime.application.core.utils.handlers.error.api_error import ApiError

@dataclass
class Dimensions:
    width: int = field(default=0)
    height: int = field(default=0)


@dataclass
class Image(Entity):
    
    dimensions: Dimensions = Dimensions()
    content: BytesIO = BytesIO()
    ocr_analysis: OCRAnalysis = OCRAnalysis()
    title: str = ""
    
    def __init__(self,
                 entity_id: str = None,
                 created_at: datetime.datetime = None,
                 updated_at: datetime.datetime = None,
                 dimensions: Dimensions = None,
                 ocr_analysis: OCRAnalysis = None):
        super().__init__(entity_id=entity_id,
                         created_at=created_at,
                         updated_at=updated_at)
        
        self.dimensions = dimensions if dimensions is not None else Dimensions()
        self.ocr_analysis = ocr_analysis if ocr_analysis is not None else OCRAnalysis()
        
    def load(self, image_path: str):
        file_exists = os.path.exists(image_path)
        
        if not file_exists:
            raise ApiError.resource_not_found(message='Could not find the provided file.', 
                                              payload={ 'image_path': image_path })
        print(image_path)
        with open(image_path, 'rb') as img:
            self.content.write(img.read())
            image = PilImage.open(self.content)
            self.dimensions.width = image.width
            self.dimensions.height = image.height
            self._updated_at = datetime.datetime.now()
            self.title = image_path
            
        return self
    
    def save(self, filename: str):
        
        image = PilImage.open(self.content)
        image.save(filename)
        
        return self
    
    def set_ocr_analysis(self, analysis: OCRAnalysis):
        self.ocr_analysis = analysis
        self._updated_at = datetime.datetime.now()
        
        return self

    def set_image(self, image: BytesIO):
        self.content = image
        
        self._updated_at = datetime.datetime.now()
        
        return self
