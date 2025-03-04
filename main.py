import math
from hime.lib.vision import Vision
from hime.lib.canvas import Canvas
from PIL import Image

if __name__ == '__main__':
    vision = Vision()
    canvas = Canvas()

    coords = (
        (474, 657, 158, 252),
        (924, 658, 153, 249),
        (878, 64, 170, 228),
        (108, 803, 179, 239),
        (637, 819, 150, 231),
        (894, 1072, 182, 224),
        (18, 1066, 251, 347),
        (50, 54, 204, 260),
        (433, 1078, 219, 202),
        (453, 1358, 177, 207),
        (164, 650, 169, 197)
    )

    image = Image.open("./tests/data/images/full/4fba58c3-0.png")
    box = Image.open("./tests/data/images/boxes/0.png")

    for i, coord in enumerate(coords):
        t_l_x_offset, t_l_y_offset, w, h = coord
        text = vision.detect_text(box)
        print(text)

        t_l_x, t_l_y = text.top_left
        b_r_x, b_r_y = text.bottom_right

        t_l_x = math.floor(t_l_x // text.scale_factor)
        t_l_y = math.floor(t_l_y // text.scale_factor)
        b_r_x = math.floor(b_r_x // text.scale_factor)
        b_r_y = math.floor(b_r_y // text.scale_factor)

        width = b_r_x - t_l_x
        height = b_r_y - t_l_y

        image = canvas.remove_text_block(image, coords=((t_l_x + t_l_x_offset, t_l_y + t_l_y_offset),
                                                        (t_l_x + t_l_x_offset + width, t_l_y + t_l_y_offset + height)))
        

        canvas.text_block_aware(image, ((t_l_x_offset, t_l_y_offset),
                                        (t_l_x_offset + w, t_l_y_offset + h)))
        
        box = Image.open(f"./tests/data/images/boxes/{i+1}.png")
        