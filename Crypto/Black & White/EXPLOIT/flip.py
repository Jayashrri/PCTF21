from PIL import Image

# Open an already existing image
imageObject = Image.open("full_b.png")

# Do a flip of left and right
secret_inv = imageObject.transpose(Image.FLIP_LEFT_RIGHT)
#secret_inv = imageObject.transpose(Image.FLIP_TOP_BOTTOM)
secret_inv.save("flip_b.png")