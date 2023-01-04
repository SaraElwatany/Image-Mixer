import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter









class Image():


    phase= np.full(shape=(230,440),fill_value=255)
    magnitude= np.full(shape=(230,440),fill_value=255)
    croppedphase= np.full(shape=(230,440),fill_value=0)
    croppedmagnitude= np.full(shape=(230,440),fill_value=0)
    img_box1,img_box2= dict(), dict() 
    no_boxes1, no_boxes2= 0, 0
    imgs = ['static\Images\image1_440x230.png' , 'static\Images\image2_440x230.png']
    options = ["A","B","C","E"]
    option1,option2,value1,value2= "5", "5","N","N"


    def __init__(self, path):
        self.path = path
        self.img = self.readImage()


    def readImage(self):
        img = cv2.imread( self.path ,0)
        return img


    def getFourier(self):
        f = np.fft.fft2(self.img)
        fshift = np.fft.fftshift(f)
        magnitude = 20*np.log(np.abs(fshift))
        phase = np.angle(fshift)
        return f , magnitude , phase


    def resizeImage(self,img_a,img_b):
        new_height, new_width = np.shape(img_a)
        img_b = cv2.resize(img_b, dsize=[new_width,new_height])
        return img_b


    def save(magnitude , phase ,number):  
        plt.imsave(f'static/Images/magnitude{number}.png' ,magnitude ,cmap = 'gray' )
        plt.imsave(f'static/Images/phase{number}.png',phase ,cmap = 'gray' )

