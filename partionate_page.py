from PIL import Image

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

for box, (x, y, w, h) in enumerate(coords):
    piece = image.crop((x, y, x + w, y + h))
    piece.save(f"./tests/data/images/boxes/{box}.png", format="png")