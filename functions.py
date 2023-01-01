import numpy as np
import cv2
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from PIL import Image



def readImage(file):
    img = cv2.imread(file,0)
    return img


def imageFourier(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    phase_spectrum = np.angle(fshift)
    return f , magnitude_spectrum , phase_spectrum


def combined(freq_mag, freq_phase):
    combined = np.multiply(np.abs(freq_mag), np.exp(1j*np.angle(freq_phase)))
    imgCombined = np.real(np.fft.ifft2(combined))
    plt.imsave('static/Images/output.png',imgCombined, cmap='gray')


    
def mask(image,imageno,type,x1,y1,x2,y2):
    img = readImage(image)
    shape= np.shape(img)
    x= np.zeros(shape, dtype='uint8')
    x= cv2.rectangle(x, (x1,y1), (x2,y2),(255,255,255),-1)
    imgcropped= cv2.bitwise_and(img,img,mask=x)
    cv2.imwrite(f'static/Images/masked{type}{imageno}.png', imgcropped)
    #plt.imsave(f'static/Images/masked{type}{imageno}.png',imgcropped ,cmap = 'gray' )
    

def and_mask(image1,image2,type,no):
    img1= readImage(image1)
    img2= readImage(image2)
    anded_img= cv2.bitwise_and(img1,img2)
    cv2.imwrite(f'static/Images/{type}{no}.png', anded_img)
    #plt.imsave(f'static\Images\masked{type}{imageno}.png',imgcropped ,cmap = 'gray' )


def or_mask(image1,image2,type,no):
    img1= readImage(image1)
    img2= readImage(image2)
    ored_img= cv2.bitwise_or(img1,img2)
    cv2.imwrite(f'static/Images/{type}{no}.png', ored_img)
    



def uniform_mask(image,imageno,type):
    img = readImage(image)
    shape= np.shape(img)
    new_img = np.ones(shape, dtype = np.uint8)
    uni_img = 255*new_img
    cv2.imwrite(f'static/Images/uniform{type}{imageno}.png', uni_img)
    #uni_img.save(f'static/Images/uniform{type}{imageno}.png')
    

    
    
def plotspectrums(magnitude_spectrum_a , phase_spectrum_a ,number):  
    plt.imsave(f'static/Images/magnitude{number}.png' ,magnitude_spectrum_a ,cmap = 'gray' )
    plt.imsave(f'static/Images/phase{number}.png',phase_spectrum_a ,cmap = 'gray' )
