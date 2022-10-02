from typing import Protocol

from hime.application.core.entities.ocr_analysis import OCRAnalysis

class OCRInterface(Protocol):
    def extract_text(self, image: bytes) -> OCRAnalysis: ...