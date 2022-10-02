from io import BytesIO
import os
import textwrap
from string import ascii_letters

from PIL import Image as PilImage, ImageDraw, ImageFont

from hime.application.core.entities.image import Image
from hime.application.core.entities.ocr_analysis import TextBlock

class Pillow:
    MARGINS = 0
    FONT_SIZES = [ 12, 16, 24, 32, 48, 64 ]

    def cover_old_text_with_dialog_boxes(self, image: Image) -> Image:
        output_image = BytesIO()
        image_pillow = PilImage.open(image.content)
        canvas = ImageDraw.Draw(image_pillow)
        
        for block in image.ocr_analysis.blocks:

            # X_TOP_LEFT = block.position.x - self.MARGINS
            # Y_TOP_LEFT = block.position.y - self.MARGINS
            # X_BOTTOM_RIGHT = X_TOP_LEFT + block.area.width + self.MARGINS
            # Y_BOTTOM_RIGHT = Y_TOP_LEFT + block.area.height + self.MARGINS
            
            self.detect_boundary_boxes_by_starting_point(block, image_pillow)

            # canvas.rectangle([(X_TOP_LEFT, Y_TOP_LEFT), (X_BOTTOM_RIGHT, Y_BOTTOM_RIGHT)], fill='white')

        image_pillow.save(output_image, 'png')
        
        image.set_image(output_image)
        
        return image

    def detect_boundary_boxes_by_starting_point(self, text_block: TextBlock, image: PilImage) -> ImageDraw:
        area_width = text_block.area.width
        area_height = text_block.area.height
        
        top_left_x = text_block.position.x
        top_left_y = text_block.position.y
        bottom_right_x = text_block.position.x + area_width
        bottom_right_y = text_block.position.y + area_height
        n_x = top_left_x
        n_y = top_left_y
        
        new_left_x = 0
        new_right_x = 0
        
        reference_pixel_color = image.getpixel((top_left_x, top_left_y))
        current_pixel_color = reference_pixel_color
        while reference_pixel_color ==  current_pixel_color:
            n_x -= 1
            current_pixel_color = image.getpixel((n_x, n_y))
        
        new_left_x = n_x
        print((top_left_x, top_left_y), (new_left_x, n_y))
        
        n_x = bottom_right_x
        n_y = bottom_right_y
        
        reference_pixel_color = image.getpixel((bottom_right_x, bottom_right_y))
        current_pixel_color = reference_pixel_color
        while reference_pixel_color == current_pixel_color:
            n_x += 1
            current_pixel_color = image.getpixel((n_x, n_y))
        
        new_right_x = n_x
        
        print((bottom_right_x, bottom_right_y), (new_right_x, n_y))
        print("*" * 100)
    
    def fit_text_into_text_box_area(self, text_block: TextBlock, canvas: ImageDraw) -> ImageDraw:
        
        for index, font_size in enumerate(self.FONT_SIZES):
            font = ImageFont.truetype(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../application/core/fonts/cc-wild-words-roman.ttf')), font_size)
            AVG_CHAR_WIDTH = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            MAX_CHAR_COUNT = int(text_block.area.width / AVG_CHAR_WIDTH)
            
            if MAX_CHAR_COUNT <= 0: continue
            
            wrapped_text = textwrap.fill(text_block.translation.text, width=MAX_CHAR_COUNT)
            width, height = canvas.textsize(wrapped_text, font=font)

            if height >= text_block.area.height:
                best_font_size = self.FONT_SIZES[index - 1] if index > 0 else self.FONT_SIZES[index]
                font = ImageFont.truetype(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../application/core/fonts/cc-wild-words-roman.ttf')), best_font_size)
                canvas.text((text_block.position.x, text_block.position.y), wrapped_text, (0,0,0), align='center', font=font)
                break
        
        return canvas


    def set_translated_text_to_image(self, image: Image) -> Image:
        output_image = BytesIO()
        image_pillow = PilImage.open(image.content)
        canvas = ImageDraw.Draw(image_pillow)

        for block in image.ocr_analysis.blocks:
            canvas = self.fit_text_into_text_box_area(block, canvas)

        image_pillow.save(output_image, 'png')

        image.set_image(output_image)
        
        return image