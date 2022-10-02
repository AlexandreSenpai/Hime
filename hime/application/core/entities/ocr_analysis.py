from dataclasses import dataclass, field
import datetime
from enum import Enum
from typing import List
from dataclasses import dataclass

from hime.application.core.entities.entity import Entity
from hime.application.core.entities.translation import Translation

class Symbols(Enum):
    SPACE =  ' '
    LINE_BREAK = '\n'

@dataclass
class Position:
    x: int
    y: int

@dataclass
class Area:
    width: int
    height: int

@dataclass
class TextBlock:
    text: str
    position: Position
    area: Area
    translation: Translation = field(default_factory=Translation)
    
    def set_translation(self, translation: List[Translation]):
        self.translation = translation
        
        return self
    
    def set_area(self, area: Area):
        self.area = area
        
        return self

    def set_position(self, position: Position):
        self.position = position
        
        return self

@dataclass
class OCRAnalysis(Entity):
    
    blocks: List[TextBlock] = None
    
    def __init__(self,
                 entity_id: str = None,
                 created_at: datetime.datetime = None,
                 updated_at: datetime.datetime = None,
                 blocks: List[TextBlock] = None):
        super().__init__(entity_id=entity_id,
                         created_at=created_at,
                         updated_at=updated_at)
        
        self.blocks = blocks if blocks is not None else list()

