from hime.application.core.entities.image import Dimensions, Image, ImageProps

if __name__ == '__main__':
    img = Image(props=ImageProps(dimensions=Dimensions(width=100,
                                                       height=200)))
    print(img)