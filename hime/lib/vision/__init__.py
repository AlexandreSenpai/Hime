
from dataclasses import dataclass, field
from io import BytesIO
import math
from typing import List, Tuple, Union
import easyocr
from PIL.Image import Image, fromarray as p_fromarray
from PIL.Image import open as p_open
from PIL import ImageOps

import numpy as np
import math

import cv2
import numpy as np


from deskew import determine_skew


class ImagePrep:
    def resize(self, 
               image: Image, 
               scale: float = 2.5) -> Tuple[float, Image]:
        w_size, h_size = image.size
        return scale, image.resize(
            size=(math.ceil(w_size * scale),
                  math.ceil(h_size * scale))
        )
    
    def set_dpi(self, 
                image: Image, 
                dpi: int = 300) -> Image:
        temp_img = BytesIO()
        image.save(temp_img, format="png", dpi=(dpi, dpi))
        return p_open(temp_img)
     
    def rotate(self,
               image: Image,
               angle: float,
               background: Union[int, 
                                 Tuple[int, int, int]]) -> np.ndarray:
        img_arr = np.asarray(image)
        old_width, old_height = img_arr.shape[:2]
        angle_radian = math.radians(angle)
        width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
        height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

        image_center = tuple(np.array(img_arr.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        rot_mat[1, 2] += (width - old_width) / 2
        rot_mat[0, 2] += (height - old_height) / 2
        return cv2.warpAffine(
            img_arr, 
            rot_mat, 
            (int(round(height)), int(round(width))), 
            borderValue=background # type: ignore
        ) # type: ignore

    def deskew(self, image: Image):
        grayscale = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2GRAY)
        angle = determine_skew(grayscale)

        if angle is None:
            raise Exception("Could not determine angle.")
        
        rotated = self.rotate(image, float(angle), (0, 0, 0))
        cv2.imwrite('output.png', rotated)
        return p_fromarray(rotated)
    
    def convert_to_vector(self, image: Image):
        
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection to find outlines
        edges = cv2.Canny(gray_image, 100, 200)

        # Find contours (shapes) in the image
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # Create a new blank image to draw the vectorized image with white background
        vector_image = np.ones_like(gray_image) * 255

        # Draw contours on the blank image to form vectorized shapes in black color
        cv2.drawContours(vector_image, contours, -1, (0, 0, 0), thickness=6)

        cv2.imwrite("box.png", vector_image)

        return p_fromarray(vector_image)
    
class TextNormalizer:
    def remove_spaces(self, text: str) -> str:
        full_txt = ""
        for i, c in enumerate(text):
            if i == 0:
                full_txt += c
                continue

            if c == " " and text[i-1] == " ":
                continue

            full_txt += c
        
        return full_txt.replace(" ,", ",").replace(" .", ".").strip()
    
    def remove_breaklines(self, text: str) -> str:
        return text.replace("\n", " ")

@dataclass
class Text:
    content: str = field(default="")
    top_left: Tuple[int, int] = field(default_factory=lambda: (0, 0))
    bottom_right: Tuple[int, int] = field(default_factory=lambda: (0, 0))
    width: int = field(default=0)
    height: int = field(default=0)
    scale_factor: float = field(default=0)

EasyOCROutput = List[
    Tuple[
        Tuple[
            Tuple[np.int32, np.int32],
            Tuple[np.int32, np.int32],
            Tuple[np.int32, np.int32],
            Tuple[np.int32, np.int32]
        ],
        str,
        np.float64
    ]
]

class Vision:

    def __init__(self):
        self.scale_factor = 0.0

    def preprocess_image(self, image: Image) -> np.ndarray:
        processor = ImagePrep()
        scale, image = processor.resize(image=image, scale=2.5)
        self.scale_factor = scale
        image = processor.set_dpi(image)
        # Convert image to grayscale
        image = ImageOps.grayscale(image)

        # Convert image to NumPy array for OpenCV operations
        img_array = np.asarray(image)

        # Apply Gaussian blur to remove noise
        img_array = cv2.GaussianBlur(img_array, (5, 5), 0)

        # Apply adaptive thresholding to create a binary image
        img_array = cv2.adaptiveThreshold(img_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Use OpenCV to equalize the histogram of the image
        img_array = cv2.equalizeHist(img_array)

        cv2.imwrite("filter.png", img_array)

        return np.asarray(image)
    
    def translate_ocr_output(self, ocr_response: EasyOCROutput) -> Text:
        text = Text()

        top_left_y_options = []
        top_left_x_options = []
        bottom_right_y_options = []
        bottom_right_x_options = []

        for finding in ocr_response:
            top_left, _, \
            bottom_right, _ = finding[0]
            content, _ = finding[1:]

            top_left_x, top_left_y = top_left
            bottom_right_x, bottom_right_y = bottom_right

            top_left_y_options.append(top_left_y)
            top_left_x_options.append(top_left_x)
            bottom_right_y_options.append(bottom_right_y)
            bottom_right_x_options.append(bottom_right_x)

            text.content += content + " "

        top_left_y_options.sort()
        top_left_x_options.sort()

        bottom_right_y_options.sort(reverse=True)
        bottom_right_x_options.sort(reverse=True)

        text.top_left = (top_left_x_options[0], top_left_y_options[0])
        text.bottom_right = (bottom_right_x_options[0], bottom_right_y_options[0])

        text.content = text.content.strip()

        return text

    def detect_text(self, image: Image):
        text_norm = TextNormalizer()
        img = self.preprocess_image(image=image)
        response = easyocr.Reader(lang_list=["en"], verbose=False)
        text: EasyOCROutput = response.readtext(img)
        output = self.translate_ocr_output(text)
        output.scale_factor = self.scale_factor
        normalized = output.content
        normalized = text_norm.remove_breaklines(normalized)
        normalized = text_norm.remove_spaces(normalized)
        output.content = normalized
        return output
