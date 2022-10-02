from io import BytesIO
from typing import Protocol

from hime.application.core.entities.image import Image

class ImageEditorInterface(Protocol):
    def set_translated_text_to_image(self, image: Image) -> Image: ...
    def cover_old_text_with_dialog_boxes(self, image: Image) -> Image: ...