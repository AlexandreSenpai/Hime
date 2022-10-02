from typing import Protocol

from PIL import ImageDraw

from hime.application.core.entities.image import Image
from hime.application.core.entities.ocr_analysis import TextBlock

class ImageEditorInterface(Protocol):
    def set_translated_text_to_image(self, image: Image) -> Image: ...
    def cover_old_text_with_dialog_boxes(self, image: Image) -> Image: ...
    def detect_boundary_boxes_by_starting_point(self, text_block: TextBlock, canvas: ImageDraw) -> ImageDraw: ...