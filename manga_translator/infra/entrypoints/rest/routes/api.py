from flask import request

from manga_translator.infra.entrypoints.rest.app import APP

# interfaces
from manga_translator.application.use_cases.convert_image_to_text.interfaces import ImageToTextResponseDTO

# controllers
from manga_translator.application.use_cases.convert_image_to_text import convert_image_to_text_controller


@APP.route('/rest', methods=['POST'], strict_slashes=False)
def pdf() -> ImageToTextResponseDTO:
    return convert_image_to_text_controller.execute(request_object=request)

@APP.route('/healthcheck', methods=['GET'])
def health_check() -> str:
    return 'service is up and running'