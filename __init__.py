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
    vision = Vision(service_account=r'')  # pass here the path of your service account
    translate = Translate()
    translations = []

    response: Tuple[Image.open, list] = vision.detect_text(img_in)  # Image to translate
    for block in response[1]:
        translations.append({
            "font_color": block.get('font_color'),
            "translated": translate.translate(text=block.get('text', ''), target_language='pt-br'),
            "text_area": block.get('area'),
            "text_box_size": block.get('text_box_size')
        })

    # # added this so we don't need to send requests for google when testing
    # translations = [
    #     {'font_color': 255, 'translated': 'SE PAPI E SUU VIREM BRINCAR COMIGO ...', 'text_area': ((1368, 294), (1582, 499)), 'text_box_size': (214, 205)},
    #     {'font_color': 255, 'translated': 'ENTÃO QUERO FICAR AQUI.', 'text_area': ((182, 648), (395, 757)), 'text_box_size': (213, 109)},
    #     {'font_color': 255, 'translated': 'MAS VOCÊ NÃO TEM QUE VIR.', 'text_area': ((1005, 1014), (1131, 1243)), 'text_box_size': (126, 229)},
    #     {'font_color': 255, 'translated': 'O QUE VOCÊ FAZ, QUERIDA?', 'text_area': ((160, 1028), (344, 1142)), 'text_box_size': (184, 114)},
    #     {'font_color': 255, 'translated': 'HÃ?!', 'text_area': ((435, 1067), (594, 1121)), 'text_box_size': (159, 54)},
    #     {'font_color': 255, 'translated': '!!', 'text_area': ((1547, 1265), (1560, 1283)), 'text_box_size': (13, 18)},
    #     {'font_color': 255, 'translated': '35', 'text_area': ((1667, 1521), (1689, 1533)), 'text_box_size': (22, 12)},
    #     {'font_color': 255, 'translated': 'VOCÊ AMA ESSE HUMANO. MAS POR QUE...?', 'text_area': ((1034, 1655), (1282, 1764)), 'text_box_size': (248, 109)},
    #     {'font_color': 255, 'translated': 'MAS ... PAPI, SUU ...', 'text_area': ((1546, 1634), (1647, 1743)), 'text_box_size': (101, 109)},
    #     {'font_color': 255, 'translated': 'Você fez algo estranho com ela?', 'text_area': ((791, 1735), (994, 1786)), 'text_box_size': (203, 51)},
    #     {'font_color': 255, 'translated': 'Ah bem. isso é; üh.', 'text_area': ((597, 1781), (757, 1845)), 'text_box_size': (160, 64)},
    #     {'font_color': 255, 'translated': 'BEM...', 'text_area': ((131, 1814), (280, 1847)), 'text_box_size': (149, 33)},
    #     {'font_color': 255, 'translated': 'SIMPLESMENTE NÃO CONSIGO ENTENDER.', 'text_area': ((494, 2192), (675, 2368)), 'text_box_size': (181, 176)},
    #     {'font_color': 255, 'translated': 'Adivinhando com base em suas ações ...', 'text_area': ((1347, 2241), (1477, 2341)), 'text_box_size': (130, 100)}
    # ]

    # print(translations)

    img = response[0]
    # img = Image.open('./blank.png')
    canvas = ImageDraw.Draw(img)

    # Trying to fix text position ;-;
    for obj in translations:
        rows = fit_tool.fit(row_obj=obj, canvas=canvas)

    # Output image
    img.save('out.png', 'png')
