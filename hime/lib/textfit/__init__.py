from cgitb import text
from tkinter import font
from typing import List, Tuple
import math

from PIL import ImageFont, ImageDraw


class TextFit:
    def __repr__(self):
        return 'Class made to fit a text in a rectangle'

    def need_slash_space(self, words_per_row: int = 0, row_index: int = 0) -> (bool):
        """This function tells if its time to break the line or not.
        """
        if row_index + 1 > words_per_row:
            return True
        return False

    def how_many_words_per_row(self, text: str, font_size: tuple, x_area: int) -> (int):
        """This function calculates how many letters fits on each row of the text box.
        """
        text_chars_count = len(text)
        if x_area < 0:
            x_area = x_area * -1
        letters_per_row = math.ceil(x_area / (math.ceil(font_size[0] / text_chars_count)))
        return letters_per_row

    def find_proportions(self, row_obj: dict, font_size: int) -> (Tuple[ImageFont.truetype, int]):
        """This function calculates the text proportions based on current font size.
        """
        font = ImageFont.truetype('./fonts/cc-wild-words-roman.ttf', font_size)
        font_size_px = font.getsize(text=row_obj.get('translated'))
        words_per_row = self.how_many_words_per_row(
            text=row_obj.get('translated'),
            font_size=font_size_px,
            x_area=row_obj.get('text_box_size')[0]
        )

        return (words_per_row, font, font_size)

    def adjust_font_size(self, row_obj: dict) -> (Tuple[int, ImageFont.truetype, int]):
        """This function tries to find the best font size to make the text fits in its box.
        """
        fonts = [12, 16, 20, 24]

        text_size = len(row_obj.get('translated'))
        font_proportions = [self.find_proportions(row_obj=row_obj, font_size=font_s) for font_s in fonts]

        default_prop = font_proportions[0]
        for index, props in enumerate(font_proportions):
            words, font, font_size = props

            if (math.ceil(text_size / words) * (font_size + 5)
                >= row_obj.get('text_box_size')[1]):

                return (words, font, font_size)

            else:
                default_prop = font_proportions[index]

        return default_prop

    def create_row_with_slash(self, row_obj: dict) -> (List[str]):
        """This function create the rows with break line slash.
        """
        rows = []

        words_per_row, font, font_size = self.adjust_font_size(row_obj=row_obj)

        raw_index = 0
        row = ''
        for index, letter in enumerate(row_obj.get('translated')):
            phrase_len = len(row_obj.get('translated'))
            raw_index += 1
            need_slash = self.need_slash_space(words_per_row=words_per_row, row_index=raw_index)

            if need_slash is not True:
                row += letter
            elif need_slash is True:
                raw_index = 0
                if (row_obj.get('translated')[index] != ' '
                    and index < phrase_len - 1
                        and row_obj.get('translated')[index + 1] != ' '):

                    row += letter + '-'

                else:
                    row += letter

                rows.append(row)
                row = ''

            if index == len(row_obj.get('translated')) - 1:
                rows.append(row)

        return (rows, (font, font_size))

    def fit(self, row_obj: dict, canvas: ImageDraw.Draw):
        """This function prints the text on image output.
        """
        rows, font_properties = self.create_row_with_slash(row_obj=row_obj)
        font, font_size = font_properties
        color = 0 if row_obj.get('font_color') >= 255 / 2 else 255
        x, y = row_obj.get('text_area')[0]
        shift_y = 0
        for row in rows:
            if len(row) - 1 > 0 and row[0] == ' ':
                row = row[1:]
            canvas.text((x - 1, y + shift_y), row, fill=color, font=font)
            shift_y += font_size + 5
