# Hime

## What is this?
This script translates manga pages using CLOUD VISION API to recognize text in images [planning to change to tesseract], Translate API to translate the extracted text and PIL to manipulate images.

For update notes follow me on [Twitter](https://twitter.com/AlexandreSenpa1).

### Latest commit
|Before|After|
|:------:|:-----:|
|<img src='https://pbs.twimg.com/media/EhP-PQMWkAAB50H?format=jpg&name=large' />|<img src='https://pbs.twimg.com/media/EhP-P4-XgAEuYAO?format=png&name=large' />|

### Previous commit
|Before|After|
|:------:|:-----:|
|<img src='https://pbs.twimg.com/media/EhCZjiIXgAc194Q?format=jpg&name=large' />|<img src='https://pbs.twimg.com/media/EhCZku7WsAAHSdR?format=png&name=large' />|

## Requirements

- Python 3.8+
- Google Cloud Vision API
- Google Cloud Translate API

>You have to get the service account of your google cloud project with access granted to the google api's listed above to run this code.

## How to run?!
This code is just for development purposes yet so to run it you'll have to open it in a notepad or something that you rather be using.

Once you've opened it just change the img_in variable with the source image path that you want to translate.

Ex:

```python
from hime import hime, TranslateImageRequestDTO, LanguageOptions

if __name__ == '__main__':
    hime.execute(data=TranslateImageRequestDTO(language=LanguageOptions(source='en-US',
                                                                        target='pt-BR'),
                                               images=['/root/code/Manga-AutoTranslate/tests/static/1.jpg']))
```

Now you just have to run it and wait for the **./results/{image.id}.png** be generated at the results folder of this project.

Thanks for using!
