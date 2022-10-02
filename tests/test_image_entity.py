import pytest
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from hime.application.core.entities.image import Dimensions, Image
from hime.application.core.utils.handlers.error.api_error import ApiError

class TestImageEntity:
    def test_successful_image_entity_instantiation(self) -> None:
        image = Image(dimensions=Dimensions(width=100,
                                            height=100))
        
        assert isinstance(image.dimensions, Dimensions) == True
        assert image.dimensions.width == 100
        assert image.dimensions.height == 100
        
    def test_successful_image_entity_instantiation_with_no_parameters(self) -> None:
        image = Image()
        
        assert isinstance(image.dimensions, Dimensions)
        assert image.dimensions.width == 0
        assert image.dimensions.height == 0

    def test_successful_data_return(self) -> None:
        image = Image()
        
        assert isinstance(image.data, dict)
        assert image.data.get('dimensions', {}).get('width') == 0
    
    def test_successful_id_return(self) -> None:
        image = Image(entity_id=0)
        
        assert image.id == 0
    
    def test_successful_image_loading(self) -> None:
        image = Image()
        has_loaded = image.load('/home/alexandresenpai/scripts/desktop/manga-translator/tests/static/2.jpg')
        assert isinstance(has_loaded, Image)
        assert len(image.content.getvalue()) > 0
        
    def test_failed_image_loading(self) -> None:
        image = Image()
        try:
            has_loaded = image.load('/home/alexandresenpai/scripts/desktop/manga-translator/tests/static/NAO-EXISTE.jpg')
            if has_loaded:
                raise pytest.fail('Did not raise when file does not exists.')
        except Exception as err:
            assert isinstance(err, ApiError)
            assert err.message[0] == 'Could not find the provided file.'
        
    def test_successful_image_dimensions_set_when_loading_file(self) -> None:
        image = Image()
        image.load('/home/alexandresenpai/scripts/desktop/manga-translator/tests/static/2.jpg')

        assert image.dimensions.width == 1280
        assert image.dimensions.height == 1830