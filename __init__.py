###[BUILT-IN MODULES]###
from typing import Tuple
###[EXTERNAL MODULES]###
from PIL import Image, ImageDraw
###[PERSONAL MODULES]###
from lib.translate import Translate
from lib.vision import Vision
from lib.textfit import TextFit

if __name__ == '__main__':

    img_in = './images/sample9.jpg'

    fit_tool = TextFit()
    vision = Vision(service_account=r'') # pass here the path of your service account
    translate = Translate()
    translations = []

    response: Tuple[Image.open, list] = vision.detect_text(img_in) #Image to translate
    for block in response[1]:
        translations.append({
            "font_color": block.get('font_color'),
            "translated": translate.translate(text=block.get('text', ''), target_language='pt-br'),
            "text_area": block.get('area'),
            "text_box_size": block.get('text_box_size')
        })

    # added this so we don't need to send requests for google when testing
    # translations = [
    #     {'translated': 'DE ACORDO COM O QUE ELA DISSE,', 'text_area': ((313, 136), (397, 186)), 'text_box_size': (84, 50)},
    #     {'translated': 'ESTE NÃO É XADREZ NORMAL.', 'text_area': ((694, 102), (788, 192)), 'text_box_size': (94, 90)},
    #     {'translated': 'CERTO.', 'text_area': ((63, 306), (117, 320)), 'text_box_size': (54, 14)},
    #     {'translated': '10', 'text_area': ((42, 370), (52, 378)), 'text_box_size': (10, 8)},
    #     {'translated': 'ATÉ QUE EU DESCUBRA O TRUQUE PARA ESTE JOGO, CERTIFIQUE-SE DE GANHAR.', 'text_area': ((309, 430), (404, 526)), 'text_box_size': (95, 96)},
    #     {'translated': '... ENTÃO, VAMOS SER', 'text_area': ((44, 922), (101, 968)), 'text_box_size': (57, 46)},
    #     {'translated': 'O PRIMEIRO MOVIMENTO É SEU.', 'text_area': ((72, 1100), (184, 1165)), 'text_box_size': (112, 65)}
    # ]

    img = response[0]
    # img = Image.open('./blank.png')
    canvas = ImageDraw.Draw(img)

    #Trying to fix text position ;-;
    for obj in translations:
        rows = fit_tool.fit(row_obj=obj, canvas=canvas)

    #Output image
    img.save('out.png', 'png')