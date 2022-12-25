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


def cut(path,x,y,w,h,image):
    location= (x,y,w,h)
    img= Image.open(path)
    imgcropped= img.crop(box= (x,y,w,h))
    imgcropped.save(f'static/Images/cropped{image}.jpg')
    #imgc, f, mag, phase= imageFourier('static/Images/cropped.jpg')
    #img.paste(imgcropped, location)



def plotspectrums(img_a , magnitude_spectrum_a , phase_spectrum_a ,img_b , magnitude_spectrum_b , phase_spectrum_b):

    plt.imsave( 'static\Images\image1.png',img_a ,cmap = 'gray' )
    plt.imsave('static\Images\magnitude1.png' ,magnitude_spectrum_a ,cmap = 'gray' )
    plt.imsave('static\Images\phase1.png',phase_spectrum_a ,cmap = 'gray' )
    plt.imsave( 'static\Images\image2.png',img_b ,cmap = 'gray' )
    plt.imsave('static\Images\magnitude2.png' ,magnitude_spectrum_b ,cmap = 'gray' )
    plt.imsave('static\Images\phase2.png',phase_spectrum_b ,cmap = 'gray' )
