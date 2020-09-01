###[BUILT-IN MODULES]###
from typing import Tuple
###[EXTERNAL MODULES]###
from PIL import Image, ImageDraw
###[PERSONAL MODULES]###
from lib.translate import Translate
from lib.vision import Vision
from lib.textfit import TextFit

if __name__ == '__main__':

    img_in = './images/sample4.jpg'

    fit_tool = TextFit()
    vision = Vision(service_account=r'') # pass here the path of your service account
    translate = Translate()
    translations = []

    response: Tuple[Image.open, list] = vision.detect_text(img_in) #Image to translate
    for block in response[1]:
        translations.append({
            "translated": translate.translate(text=block.get('text', ''), target_language='pt-br'),
            "text_area": block.get('area'),
            "text_box_size": block.get('text_box_size')
        })

    # added this so we don't need to send requests for google when testing
    # translations = [
    #     {'translated': 'ASSIM, QUANTO TEMPO DURA O CARA RESISTENTE?', 'text_area': ((671, 123), (797, 184)), 'text_box_size': (124, 61)},
    #     {'translated': 'POR QUE NÃO SABEMOS?', 'text_area': ((68, 544), (188, 575)), 'text_box_size': (117, 31)},
    #     {'translated': 'Oh,', 'text_area': ((288, 1011), (310, 1022)), 'text_box_size': (20, 11)},
    #     {'translated': 'WHOO00 000000 AAAAAA !!', 'text_area': ((675, 1041), (769, 1098)), 'text_box_size': (92, 57)},
    #     {'translated': 'meu?', 'text_area': ((79, 1111), (104, 1123)), 'text_box_size': (23, 12)},
    #     {'translated': '120', 'text_area': ((759, 1205), (785, 1216)), 'text_box_size': (24, 11)}
    # ]

    img = response[0]
    # img = Image.open('./blank.jpg')
    canvas = ImageDraw.Draw(img)

    #Trying to fix text position ;-;
    for obj in translations:
        rows = fit_tool.fit(row_obj=obj, canvas=canvas)

    #Output image
    img.save('out.png', 'png')