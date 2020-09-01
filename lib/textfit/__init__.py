from typing import List
import math

from PIL import ImageFont, ImageDraw

class TextFit:
    def __init__(self):
        self.font = ImageFont.truetype('./fonts/cc-wild-words-roman.ttf', 12)

    def __repr__(self):
        return 'Class made to fit a text in a rectangle'

    def how_many_words_per_row(self, text: str, font_size: tuple, x_area: int) -> (int):
        text_chars_count = len(text)
        letters_per_row = math.ceil(x_area / (math.ceil(font_size[0] / text_chars_count)))
        return letters_per_row
    
    def need_slash_space(self, words_per_row: int=0, row_index: int=0) -> (bool):
        if row_index > words_per_row:
            return True
        return False 

    def create_row_with_slash(self, row_obj: dict) -> (List[str]):
        rows = []    
        font_size = self.font.getsize(text=row_obj.get('translated'))
        words_per_row = self.how_many_words_per_row(text=row_obj.get('translated'), font_size=font_size, x_area=row_obj.get('text_box_size')[0])
        
        raw_index = 0
        row = ''
        for index, letter in enumerate(row_obj.get('translated')):
            raw_index += 1
            need_slash = self.need_slash_space(words_per_row=words_per_row, row_index=raw_index)

            if need_slash is not True:
                row += letter
            elif need_slash is True:
                raw_index = 0
                row += letter + '-'
                rows.append(row)
                row = ''
                
            if index == len(row_obj.get('translated')) - 1:
                rows.append(row)

        return rows
    
    def fit(self, row_obj: dict, canvas: ImageDraw.Draw):
        rows = self.create_row_with_slash(row_obj=row_obj)
        x, y = row_obj.get('text_area')[0]
        shift_y = 0
        for row in rows:
            canvas.text((x, y + shift_y), row, font=self.font)
            shift_y += 12