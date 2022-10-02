from flask import request

from manga_translator.application.use_cases.convert_image_to_text import ConvertImageToTextUseCase
from manga_translator.application.use_cases.convert_image_to_text.interfaces import ImageToTextRequestDTO

class ConvertImageToTextController:
    def __init__(self, convert_image_to_text_use_case: ConvertImageToTextUseCase):
        self.convert_image_to_text_use_case = convert_image_to_text_use_case

    def execute(self, request_object: request):
        file = request_object.files['file']
        response = self.convert_image_to_text_use_case.execute(ImageToTextRequestDTO(image_bytes=file.stream.read()))
        return response.as_dict()