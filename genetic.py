from imager import *
from imager import Image as Img
from imager import array_to_img as ati

image_obj = Img('monalisa.jpeg', 0)

image_name = image_obj.img_name
image_type = image_obj.type
image = image_obj.img
shape = image.shape

new_img = np.zeros(shape, np.uint8)

draw_circle(new_img, (0, 0), 50, image_type = image_type)

array_to_img(new_img)
