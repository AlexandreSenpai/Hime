import sys
import os

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from PIL import Image

from hime.lib.vision import TextNormalizer

cleaner = TextNormalizer()

def test_remove_spaces():
    text = "DID I?           THE NAME'S SMITH, NICE TO MEET YOU."
    assert cleaner.remove_spaces(text) == \
        "DID I? THE NAME'S SMITH, NICE TO MEET YOU."
