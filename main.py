from hime import hime, TranslateImageRequestDTO, LanguageOptions

if __name__ == '__main__':
    hime.execute(data=TranslateImageRequestDTO(language=LanguageOptions(source='en-US',
                                                                        target='pt-BR'),
                                               images=['/home/alexandresenpai/scripts/desktop/manga-translator/tests/static/2.jpg']))