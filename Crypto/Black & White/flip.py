from PIL import Image

# Open an already existing image
imageObject = Image.open("pt2.png")

# Do a flip of left and right
secret_inv = imageObject.transpose(Image.FLIP_LEFT_RIGHT)
secret_inv.save("pt2_flip.png")