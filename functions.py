import numpy as np
import cv2
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter


def imageFourier(file):
    img = cv2.imread(file, 0)
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    phase_spectrum = np.angle(fshift)

    return img , f , magnitude_spectrum , phase_spectrum




def plotspectrums(img_a , magnitude_spectrum_a , phase_spectrum_a ,img_b , magnitude_spectrum_b , phase_spectrum_b):
    # plt.subplot(121),plt.imshow(img, cmap = 'gray')
    # plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
    # plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    # plt.subplot(123),plt.imshow(phase_spectrum, cmap = 'gray')
    # plt.title('Phase Spectrum'), plt.xticks([]), plt.yticks([])
    # plt.show()
    # fig, (ax1, ax2,ax3) = plt.subplots(1, 3)
    # fig.suptitle('Image')
    plt.imsave( 'D:\Edu\DSP\Tasks\Task4\DSP_Task_4\static\Images\image1.png',img_a ,cmap = 'gray' )
    plt.imsave('D:\Edu\DSP\Tasks\Task4\DSP_Task_4\static\Images\magnitude1.png' ,magnitude_spectrum_a ,cmap = 'gray' )
    plt.imsave('D:\Edu\DSP\Tasks\Task4\DSP_Task_4\static\Images\phase1.png',phase_spectrum_a ,cmap = 'gray' )
    plt.imsave( 'D:\Edu\DSP\Tasks\Task4\DSP_Task_4\static\Images\image2.png',img_b ,cmap = 'gray' )
    plt.imsave('D:\Edu\DSP\Tasks\Task4\DSP_Task_4\static\Images\magnitude2.png' ,magnitude_spectrum_b ,cmap = 'gray' )
    plt.imsave('D:\Edu\DSP\Tasks\Task4\DSP_Task_4\static\Images\phase2.png',phase_spectrum_b ,cmap = 'gray' )