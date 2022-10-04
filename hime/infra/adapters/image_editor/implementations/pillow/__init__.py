from io import BytesIO
import os
import textwrap
from string import ascii_letters
from typing import Tuple

from PIL import Image as PilImage, ImageDraw, ImageFont

from hime.application.core.entities.image import Image
from hime.application.core.entities.ocr_analysis import Area, Position, TextBlock

class Pillow:
    X_MARGINS = 3
    Y_MARGINS = 10
    FONT_SIZES = [ 12, 16, 24, 32, 45, 64 ]

    def cover_old_text_with_dialog_boxes(self, image: Image) -> Image:
        output_image = BytesIO()
        image_pillow = PilImage.open(image.content)
        canvas = ImageDraw.Draw(image_pillow)
        
        for block in image.ocr_analysis.blocks:

            # X_TOP_LEFT = block.position.x - self.MARGINS
            # Y_TOP_LEFT = block.position.y - self.MARGINS
            # X_BOTTOM_RIGHT = X_TOP_LEFT + block.area.width + self.MARGINS
            # Y_BOTTOM_RIGHT = Y_TOP_LEFT + block.area.height + self.MARGINS
            
            L_POSITION, R_POSITION = self.detect_boundary_boxes_by_starting_point(block, image_pillow)
            X_TOP_LEFT, Y_TOP_LEFT = L_POSITION
            X_BOTTOM_RIGHT, Y_BOTTOM_RIGHT = R_POSITION

            block.set_position(Position(X_TOP_LEFT, Y_TOP_LEFT))
            block.set_area(Area(width=X_BOTTOM_RIGHT - X_TOP_LEFT, 
                                height=Y_BOTTOM_RIGHT - Y_TOP_LEFT))
            
            canvas.rectangle(xy=[(X_TOP_LEFT, Y_TOP_LEFT), (X_BOTTOM_RIGHT, Y_BOTTOM_RIGHT)], 
                             fill='white')

        image_pillow.save(output_image, 'png')
        
        image.set_image(output_image)
        
        return image

    def detect_boundary_boxes_by_starting_point(self, text_block: TextBlock, image: PilImage) -> Tuple[Tuple[int, int], 
                                                                                                       Tuple[int, int]]:
        area_width = text_block.area.width
        area_height = text_block.area.height
        
        top_left_x = text_block.position.x
        top_left_y = text_block.position.y
        bottom_right_x = text_block.position.x + area_width
        bottom_right_y = text_block.position.y + area_height
    
        n_x = top_left_x
        n_y = top_left_y
    
        reference_pixel_color = image.getpixel((top_left_x, top_left_y))
        current_pixel_color = reference_pixel_color
        while reference_pixel_color == current_pixel_color and n_x > 0:
            n_x -= 1
            current_pixel_color = image.getpixel((n_x, n_y))
            if top_left_x - n_x >= 20: break
        
        top_left_x = n_x
        
        n_x = bottom_right_x
        n_y = bottom_right_y
        
        reference_pixel_color = image.getpixel((bottom_right_x, bottom_right_y))
        current_pixel_color = reference_pixel_color
        while reference_pixel_color == current_pixel_color:
            n_x += 1
            current_pixel_color = image.getpixel((n_x, n_y))
            
            if n_x - bottom_right_x >= 20: break
        
        bottom_right_x = n_x
        
        return ((top_left_x, top_left_y), (bottom_right_x, bottom_right_y))
        
    def calculate_text_size(self, text_block: TextBlock, font_size: int, canvas: ImageDraw):
        font = ImageFont.truetype(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../application/core/fonts/cc-wild-words-roman.ttf')), font_size)
        AVG_CHAR_WIDTH = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        MAX_CHAR_COUNT = int(text_block.area.width // AVG_CHAR_WIDTH)
        
        if MAX_CHAR_COUNT <= 0: return "", font, canvas.textsize("", font=font) 
        
        wrapped_text = textwrap.fill(text=text_block.translation.text, 
                                     width=MAX_CHAR_COUNT + 1, 
                                     break_long_words=True)
        
        return wrapped_text, font, canvas.textsize(wrapped_text, font=font)    
    
    def fit_text_into_text_box_area(self, text_block: TextBlock, canvas: ImageDraw) -> ImageDraw:
        
        for font_size in self.FONT_SIZES:
            
            text, font, sizes = self.calculate_text_size(text_block=text_block, 
                                                         font_size=font_size,
                                                         canvas=canvas)
            
            _, height = sizes
            
            if height < text_block.area.height - 20: continue    
        
            canvas.text(xy=((text_block.position.x + self.X_MARGINS), (text_block.position.y - self.Y_MARGINS)), 
                        text=text, 
                        fill=(0,0,0), 
                        align='center', 
                        font=font)
            
            return canvas
        
        text, font, sizes = self.calculate_text_size(text_block=text_block,
                                                     font_size=12,
                                                     canvas=canvas)
        
        canvas.text(xy=((text_block.position.x + self.X_MARGINS), (text_block.position.y - self.Y_MARGINS)), 
                    text=text, 
                    fill=(0,0,0), 
                    align='center', 
                    font=font)
        
        return canvas
            
    def set_translated_text_to_image(self, image: Image) -> Image:
        output_image = BytesIO()
        image_pillow = PilImage.open(image.content)
        image_pillow = self.convert_to_rgb(image=image_pillow)
        canvas = ImageDraw.Draw(image_pillow)

        for block in image.ocr_analysis.blocks:
            canvas = self.fit_text_into_text_box_area(block, canvas)

        image_pillow.save(output_image, 'png')

        image.set_image(output_image)
        
        return image

    def convert_to_rgb(self, image: PilImage) -> ImageDraw:
        return image.convert('RGBA')