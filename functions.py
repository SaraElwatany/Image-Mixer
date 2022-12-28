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

    plt.imsave('static\Images\output.png',imgCombined, cmap='gray')



def mask(image,imageno,type,x1,y1,x2,y2):
    img = cv2.imread(image, 0)
    shape= np.shape(img)
    x= np.zeros(shape, dtype='uint8')
    x= cv2.rectangle(x, (x1,y1), (x2,y2),(255,255,255),-1)
    imgcropped= cv2.bitwise_and(img,img,mask=x)
    imgcropped.save(f'static/Images/masked{type}{imageno}.jpg')



def plotspectrums(img_a , magnitude_spectrum_a , phase_spectrum_a ,img_b , magnitude_spectrum_b , phase_spectrum_b):

    # plt.imsave( 'static\Images\image1.png',img_a ,cmap = 'gray' )
    plt.imsave('static\Images\magnitude1.png' ,magnitude_spectrum_a ,cmap = 'gray' )
    plt.imsave('static\Images\phase1.png',phase_spectrum_a ,cmap = 'gray' )
    # plt.imsave( 'static\Images\image2.png',img_b ,cmap = 'gray' )
    plt.imsave('static\Images\magnitude2.png' ,magnitude_spectrum_b ,cmap = 'gray' )
    plt.imsave('static\Images\phase2.png',phase_spectrum_b ,cmap = 'gray' )
