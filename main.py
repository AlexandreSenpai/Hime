from hime import hime, TranslateImageRequestDTO, LanguageOptions

if __name__ == '__main__':
    for image in ['/root/code/Manga-AutoTranslate/tests/static/2.jpg',
                  '/root/code/Manga-AutoTranslate/tests/static/2.jpg',
                  '/root/code/Manga-AutoTranslate/tests/static/3.jpg',
                  '/root/code/Manga-AutoTranslate/tests/static/4.jpg',
                  '/root/code/Manga-AutoTranslate/tests/static/h.jpg',
                  '/root/code/Manga-AutoTranslate/tests/static/m.jpg']:
        hime.execute(data=TranslateImageRequestDTO(language=LanguageOptions(source='en-US',
                                                                            target='pt-BR'),
                                                    images=[image]))