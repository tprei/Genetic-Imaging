from imager import *
from imager import Image as Img
from imager import array_to_img as ati
import time
import random

num_epochs = 10
total_inds = 10000
circle_size = 2 
k = 10
rectangle = 1
circle = 0

class Shape():
   def __init__(self):
       pass

   def rng(self):
       pass

   @staticmethod
   def draw_shape(shape_type, array, center=(0,0), radius=0, color=(255, 255, 255), thickness=-1, image_type=1, top=(0, 0), bottom=(0, 0)):
       if shape_type == circle:
           cv.circle(array, center, radius, color, thickness, image_type)
       elif shape_type == rectangle:
           cv.rectangle(array, top, bottom, color, thickness)


class Circle(Shape):
    def __init__(self, radius=0, x=0, y=0):
        self.r = radius
        self.center = (x, y)

    @staticmethod
    def rng(total, x_max, y_max, max_radius = circle_size):
        r = np.random.rand(1, total)
        r *= max_radius

        x = np.random.rand(1, total)
        x *= x_max

        y = np.random.rand(1, total)
        y *= y_max
        
        r = np.rint(r)
        x = np.rint(x)
        y = np.rint(y)

        r = r.astype(int)
        x = x.astype(int)
        y = y.astype(int)

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        circles = [(circle, r[0][i], x[0][i], y[0][i], color) for i in range(total)]
        return circles

class Rectangle(Shape):
    def __init__(self, x_t, y_t, x_b, y_b):
        self.top = (x_t, y_t)
        self.bottom = (x_b, y_b)

    @staticmethod
    def rng(total, x_max, y_max):
        xt = np.random.rand(1, total)
        xt *= x_max
        xb = np.random.rand(1, total)
        xb *= x_max

        yt = np.random.rand(1, total)
        yt *= y_max
        yb = np.random.rand(1, total)
        yb *= y_max

        xt = np.rint(xt)
        xb = np.rint(xb)
        yt = np.rint(yt)
        yb = np.rint(yb)

        xt = xt.astype(int)
        xb = xb.astype(int)
        yt = yt.astype(int)
        yb = yb.astype(int)

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        rectangles = [(rectangle, (xt[0][i], yt[0][i]), (xb[0][i], yb[0][i]), color) for i in range(total)]
        return rectangles

def get_img(img_name, img_type=1):
    return Img(img_name, img_type) 

def mse(imageA, imageB):
    sub = np.array(imageB) - np.array(imageA)
    chn_means = sub.mean(axis=0)
    rgb_err = chn_means.mean()

    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return (err + rgb_err)/2

def get_individuals(img, total, shape='c'):
    if shape == 'c':
        inds = Circle.rng(total, img.shape[1], img.shape[0])
    elif shape == 'r':
        inds = Rectangle.rng(total, img.shape[1], img.shape[0])
    else:
        inds = Circle.rng(total//2, img.shape[1], img.shape[0])
        inds2 = Rectangle.rng(total-total//2, img.shape[1], img.shape[0])
        inds = inds + inds2

    return inds

def create_new_img(img):
    return np.zeros(img.shape)

def get_fitnesses(img, new, inds):
    errors = []
    mse_new = mse(new, img)
    for i in range(len(inds)): 
        updt = np.copy(new)
        if(inds[i][0] == circle):
            Shape.draw_shape(circle, updt, center=(inds[i][2], inds[i][3]), radius=inds[i][1], color=inds[i][4])
        elif(inds[i][0] == rectangle):
            Shape.draw_shape(rectangle, updt, top=inds[i][1], bottom=inds[i][2], color=inds[i][3])

        mse_updt = mse(updt, img)
        errors.append((mse_updt - mse_new, i, inds[i][0]))
    
    errors.sort(key = lambda s: s[0])
    return errors

def draw_k_best(shapes, n, new, inds):
    best_ret = -1
    best_circ = -1

    for i in range(n):
        index = shapes[i][1]
        shape_type = shapes[i][2]

        if shape_type == circle and best_circ == -1:
            best_circ = (circle, (inds[index][2], inds[index][3]), inds[i][1], inds[index][4])
        if shape_type == rectangle and best_ret == -1:
            best_ret = (rectangle, (inds[index][1], inds[index][2]), inds[index][3]) 

        if(shape_type == circle):
            Shape.draw_shape(circle, new, center=(inds[index][2], inds[index][3]), radius=inds[i][1], color=inds[index][4])
        elif(shape_type == rectangle):
            Shape.draw_shape(rectangle, new, top=inds[index][1], bottom=inds[index][2], color=inds[index][3])

    return [best_circ, best_ret]

if __name__ == '__main__':

    print("Choose image type: 1 for RGB, 0 for grayscale")
    flag = int(input())

    print("Choose the number of epochs")
    num_epochs = int(input())

    print("Choose the population size")
    total_inds = int(input())

    print("Choose your type of shape: Circle(c), Rectangle(r), Mixed(m)")
    s_type = input()

    if s_type != 'r':
        print("Choose the maximum circle size")
        circle_size = int(input())

    k = total_inds//10 

    print("What is the name of the input image?")
    image_name = input()
    image_name = image_name.strip()

    print("What is the name of the output image?")
    otp_name = input()
    otp_name = otp_name.strip()

    img_obj = get_img(image_name, flag)
    image = img_obj.img

    new_img = create_new_img(image)

    first = time.time()
    epoch_time = 0

    best_c, best_r = -1, -1 

    for epoch in range(num_epochs):
        print(f'Generation: {epoch}')
        print(f'Estimated time left: {(num_epochs-epoch)*(time.time() - epoch_time)/60.0} minutes')
        epoch_time = time.time()
        inds = get_individuals(image, total_inds, s_type)
        fits = get_fitnesses(image, new_img, inds)

        draw_k_best(fits, k, new_img, inds)

    elapsed = time.time() - first
    hours = elapsed // 3600
    minutes = elapsed % 3600
    seconds = 60*minutes/60%60
    minutes//=60

    print(f"It took me {num_epochs} epochs, {k * num_epochs} shapes to draw your image. A total of {hours} hours, {minutes} minutes and {seconds} seconds")

    cv.imwrite(otp_name, new_img)
    get_img(otp_name, flag).display() 
