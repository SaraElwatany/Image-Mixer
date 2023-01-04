import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from Image import Image

class ImageProcessing(Image):
    def __init__(self, path,freq ,mag, phase, croppedMagnitude, croppedPhase):
        super().__init__(path)
        self.mag = mag
        self.phase = phase
        self.freq = freq
        self.croppedMagnitude = croppedMagnitude
        self.croppedPhase = croppedPhase

    def mixImages(freq_mag , freq_phase):
        combined = np.multiply(np.abs(freq_mag), np.exp(1j*np.angle(freq_phase)))
        imgCombined = np.real(np.fft.ifft2(combined))
        plt.imsave('static/Images/output.png',imgCombined, cmap='gray')


    def combined_mask(magnitude, phase):
        combined = np.multiply(np.exp(magnitude/20), np.exp(1j*phase))
        combined= np.fft.ifftshift(combined)
        imgCombined = np.real(np.fft.ifft2(combined))
        plt.imsave('static/Images/output.png',imgCombined, cmap='gray')
        return imgCombined