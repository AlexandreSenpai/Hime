import sys

from hime.infra.entrypoints.code import TranslateImageUseCaseFactory
from hime.application.use_cases.translate_image import TranslateImageRequestDTO, LanguageOptions

__version__ = '0.0.1'
__author__ = 'AlexandreSenpai'
__email__ = 'alexandreramos469@gmail.com'

major_version = 3
minor_version = 8

if(int(sys.version_info[0]) != major_version or int(sys.version_info[1]) < minor_version):
    print(f'[-] You need python version {major_version}.{minor_version} to run this application.')
    sys.exit(1)

hime = TranslateImageUseCaseFactory.create()