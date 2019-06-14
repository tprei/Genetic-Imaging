import cv2 as cv
import numpy as np

class Image:
    def __init__(self, img_name, flag=1):
        try:
            self.img = cv.imread(img_name, flag)
            self.img_name = img_name
            self.type = flag
        except:
            print("There was a failure trying to open the image. Is it in the same directory as this file?")
            exit()

    def display(self):
        cv.imshow(self.img_name, self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()

def array_to_img(array):
    cv.imshow('', array)
    cv.waitKey(0)
    cv.destroyAllWindows()

