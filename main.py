from hime import hime, TranslateImageRequestDTO, LanguageOptions

if __name__ == '__main__':
    hime.execute(data=TranslateImageRequestDTO(language=LanguageOptions(source='en-US',
                                                                        target='pt-BR'),
                                               images=['/root/code/Manga-AutoTranslate/tests/static/2.jpg']))