###[BUILT-IN MODULES]###

###[EXTERNAL MODULES]###
import cv2
###[PERSONAL MODULES]###
from lib.translate import Translate
from lib.vision import Vision

if __name__ == '__main__':
    vision = Vision()
    translate = Translate()
    translations = []

    response = vision.detect_text('./1.png') #Image to translate
    for block in response[1]:
        translations.append((translate.translate(text=block.get('text', ''), target_language='pt-br'), block.get('area'), block.get('text_box_size')))

    img = response[0]

    #Trying to fix text position ;-;
    for text in translations:
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

        for i, line in enumerate(new_phrase.split('\n')):
            #Writing translated text into image.
            cv2.putText(img=img, text=line, org=(x, y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=font_scale, color=(0, 0, 0), thickness=2)
            y = y + spacing
 
    #Output image
    cv2.imwrite('out.png', img)