###[BUILT-IN MODULES]###

###[EXTERNAL MODULES]###
import cv2
###[PERSONAL MODULES]###
from lib.translate import Translate
from lib.vision import Vision
from lib.textfit import TextFit

if __name__ == '__main__':
    vision = Vision()
    translate = Translate()
    translations = []

    response = vision.detect_text('./1.png') #Image to translate
    for block in response[1]:
        translations.append((translate.translate(text=block.get('text', ''), target_language='pt-br'), block.get('area'), block.get('text_box_size')))

    """
    # added this so we don't need to send requests for google when testing
    translations = [
        ('E eu vou ficar aqui como seu convidado a partir de agora!', ((77, 76), (186, 211)), (109, 135)),
        ('EU SOU UMA SEREIA PELO NOME MEROUNE LORELEI.', ((506, 92), (616, 190)), (110, 98)),
        ('30', ((43, 611), (50, 616)), (7, 5)),
        ('Espero que estejamos juntos,', ((537, 687), (605, 771)), (68, 84)),
        ('SENHOR!', ((100, 716), (172, 745)), (72, 29)),
        ('* CONTINUA*', ((61, 908), (168, 922)), (107, 14)),
        ('XXXXXX', ((348, 242), (321, 327)), (-27, 85)),
    ]
    """
    img = response[0]

    #Trying to fix text position ;-;
    for text in translations:
        """
        index = 0
        new_phrase = ''
        
        x, y = text[1][0]
        spacing = 20
        font_scale = 1

        for word in text[0].split():
            index += 1
            if text[2][0] <= 220 and text[2][0] > 150:
                spacing = 50
                font_scale = 1.5
                if index % 2 == 0:
                    new_phrase += f'{word} \n'
                else:
                    new_phrase += f'{word} '
            elif text[2][0] <= 150:
                font_scale = 1
                spacing = 25
                if index % 1 == 0:
                    new_phrase += f'{word} \n'
                else:
                    new_phrase += f'{word} '
        """
        x, y = text[1][0]
        new_phrase, font_scale, spacing, shiftX, shiftY = TextFit().fitText(text[0], text[2][0], text[2][1], cv2.FONT_HERSHEY_SIMPLEX)
        x += shiftX
        y += shiftY
        for i, line in enumerate(new_phrase.split('\n')):
            #Writing translated text into image.
            cv2.putText(img=img, text=line, org=(x, y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=font_scale, color=(0, 0, 0), thickness=2)
            y = y + spacing
 
    #Output image
    cv2.imwrite('out.png', img)