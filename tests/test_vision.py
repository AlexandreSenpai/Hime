import sys
import os

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from PIL import Image

from hime.lib.vision import Vision

vision = Vision()

def test_extract_image_test_successfully():
    image = Image.open("./tests/data/images/boxes/0.png")
    text = vision.detect_text(image=image)
    assert text.content.upper() == "WEREN'T YOU LOOKING FOR JOBS BEFORE?"

def test_extract_image_test_successfully_case_02():
    image = Image.open("./tests/data/images/boxes/1.png")
    text = vision.detect_text(image=image)
    assert text.content.upper() == "UMM, SO YOU ARE_?"

def test_extract_image_test_successfully_case_03():
    image = Image.open("./tests/data/images/boxes/2.png")
    text = vision.detect_text(image=image)
    assert text.content.upper() == 'WHAT DO YOU MEAN "AH"'

def test_extract_image_test_successfully_case_04():
    image = Image.open("./tests/data/images/boxes/3.png")
    text = vision.detect_text(image=image)
    assert text.content.upper() == "OH, YEAH~ I NEVER INTRODUCED MYSELF, DID I? THE NAME'S SMITH, NICE TO MEET YOU:"