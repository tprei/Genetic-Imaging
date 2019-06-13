from imager import *
from imager import Image as Img
from imager import array_to_img as ati
import time

num_epochs = 500
total_inds = 100
circle_size = 10
k = 30

def get_img(img_name, img_type=1):
    return Img(img_name, img_type) 

def mse(imageA, imageB):
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err

def get_individuals(img, total):
    ind_r = np.random.rand(1, total)
    ind_r *= circle_size 

    ind_x = np.random.rand(1, total)
    ind_x *= img.shape[1]

    ind_y = np.random.rand(1, total)
    ind_y *= img.shape[0]

    inds = [(ind_r[0][i], ind_x[0][i], ind_y[0][i]) for i in range(total)]
    return inds

def create_new_img(img):
    return np.zeros(img.shape)

def get_fitnesses(img, new, inds, total):
    errors = []
    for i in range(total): 
        updt = np.copy(new)
        draw_circle(updt, (inds[i][1], inds[i][2]), radius=inds[i][0])
        mse_updt = mse(updt, img)
        mse_new = mse(new, img)

        errors.append((mse_updt - mse_new, i))
   
    errors.sort(key = lambda s: s[0])
    return errors

def draw_k_best(circles, n, new, inds):
    k_best = []
    for i in range(n):
        index = circles[i][1]
        draw_circle(new, (inds[index][1], inds[index][2]), radius=inds[index][0])
        k_best.append((inds[index][1], inds[index][2], inds[index][0]))

    return k_best[0]

print("Choose the number of epochs")
num_epochs = int(input())

print("Choose the population size")
total_inds = int(input())

print("Choose the maximum circle size")
circle_size = int(input())

k = total_inds//10 

print("What is the name of the input image?")
image_name = input()
image_name = image_name.strip()

print("What is the name of the output image?")
otp_name = input()
otp_name = otp_name.strip()

img_obj = get_img(image_name, 0)
image = img_obj.img

new_img = create_new_img(image)
best = (0, 0, 0)

first = time.time()
epoch_time = 0
for epoch in range(num_epochs):
    print(f'Generation: {epoch}')
    print(f'Estimated time left: {(num_epochs-epoch)*(time.time() - epoch_time)/60.0} minutes')
    epoch_time = time.time()
    inds = get_individuals(image, total_inds)
    inds = np.array(inds)
    inds = np.rint(inds)
    inds = inds.astype(int)

    if best[0] and best[1] and best[2]:
        for i in range(len(inds)):
            inds[i][1] = (inds[i][1] + best[0])/2
            inds[i][2] = (inds[i][2] + best[1])/2
            inds[i][0] = (inds[i][0] + best[2])/2

    fits = get_fitnesses(image, new_img, inds, total_inds)        
    best = draw_k_best(fits, k, new_img, inds)

elapsed = time.time() - first
array_to_img(new_img)
cv.imwrite(otp_name, new_img)
print(f"It took me {num_epochs} epochs, {k * num_epochs} circles and {elapsed}s to draw your image")
