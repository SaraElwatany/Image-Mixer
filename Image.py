import numpy as np
import cv2
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter


class Image():
    def __init__(self, path):
        self.path = path
        self.img = self.readImage()
        # self.xStart = canvas_points[0]
        # self.yStart = canvas_points[1]
        # self.xEnd = canvas_points [2]
        # self.yEnd = canvas_points [3]

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


    def save(self,magnitude , phase ,number):  
        plt.imsave(f'static/Images/magnitude{number}.png' ,magnitude ,cmap = 'gray' )
        plt.imsave(f'static/Images/phase{number}.png',phase ,cmap = 'gray' )


            
    def mask(self, image,imageno,type,x1,y1,x2,y2):
        img = self.readImage(image)
        shape= np.shape(img)
        x= np.zeros(shape, dtype='uint8')
        x= cv2.rectangle(x, (x1,y1), (x2,y2),(255,255,255),-1)
        imgcropped= cv2.bitwise_and(img,img,mask=x)
        cv2.imwrite(f'static/Images/masked{type}{imageno}.png', imgcropped)
        #plt.imsave(f'static/Images/masked{type}{imageno}.png',imgcropped ,cmap = 'gray' )
        

    def and_mask(self, image1,image2,type,no):
        img1= self.readImage(image1)
        img2= self.readImage(image2)
        anded_img= cv2.bitwise_and(img1,img2)
        cv2.imwrite(f'static/Images/{type}{no}.png', anded_img)
        #plt.imsave(f'static\Images\masked{type}{imageno}.png',imgcropped ,cmap = 'gray' )


    def or_mask(self, image1,image2,type,no):
        img1= self.readImage(image1)
        img2= self.readImage(image2)
        ored_img= cv2.bitwise_or(img1,img2)
        cv2.imwrite(f'static/Images/{type}{no}.png', ored_img)
        



    def uniform_mask(self, image,imageno,type):
        img = self.readImage(image)
        shape= np.shape(img)
        new_img = np.ones(shape, dtype = np.uint8)
        uni_img = 255*new_img
        cv2.imwrite(f'static/Images/uniform{type}{imageno}.png', uni_img)
        #uni_img.save(f'static/Images/uniform{type}{imageno}.png')


class ImageProcessing(Image):
    def __init__(self, path,freq ,mag, phase):
        super().__init__(path)
        self.mag = mag
        self.phase = phase
        self.freq = freq

    def mixImages(self,freq_mag , freq_phase):
        combined = np.multiply(np.abs(freq_mag), np.exp(1j*np.angle(freq_phase)))
        imgCombined = np.real(np.fft.ifft2(combined))
        plt.imsave('static/Images/output.png',imgCombined, cmap='gray')



        


