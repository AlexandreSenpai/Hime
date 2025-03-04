from PIL.Image import Image, new as NewImage
from PIL.ImageDraw import ImageDraw

class Canvas:

    def remove_text_block(self, 
                          image: Image,
                          coords: tuple[tuple[int, int], 
                                        tuple[int, int]]) -> Image:

        draw = ImageDraw(image, 'RGBA')
        draw.rectangle(coords, (255, 255, 255, 255))

        image.save("blank.png")

        return image
    
    def text_block_aware(self, 
                         image: Image,
                         coords: tuple[tuple[int, int],
                                       tuple[int, int]]) -> Image:
        
        draw = ImageDraw(image, 'RGBA')
        draw.ellipse(coords, (255, 255, 255, 0), (255, 0, 0))

        image.save("ellipsis.png")

        return image