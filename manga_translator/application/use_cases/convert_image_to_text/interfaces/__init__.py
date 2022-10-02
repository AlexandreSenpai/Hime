from dataclasses import asdict, dataclass
from typing import List

@dataclass(frozen=True)
class Dimensions:
    width: int
    height: int

@dataclass(frozen=True)
class Image:
    image_path: str
    image_extension: str
    dimensions: Dimensions

@dataclass(frozen=True)
class Position:
    x: int
    y: int

@dataclass(frozen=True)
class Area:
    width: int
    height: int

@dataclass()
class TextBlock:
    text: str
    position: Position
    area: Area
    translated_text: str = ""

    def set_translated_text(self, translated_text):
        self.translated_text = translated_text

@dataclass()
class ImageToTextResponseDTO:
    image: Image
    text_blocks: List[TextBlock]

    def as_dict(self):
        return asdict(self)

@dataclass(frozen=True)
class ImageToTextRequestDTO:
    image_path: str=None
    image_bytes: str=None

@dataclass()
class TranslatorResponse:
    source_language: str
    target_language: str
    original_text: str
    translated_text: str