import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from Image import Image

class Mask():
    def __init__(self, path):
        super().__init__(path)

    def mask(image,x1,y1,x2,y2): 
        shape= np.shape(image)
        x= np.zeros(shape, dtype='uint8')
        x= cv2.rectangle(x, (x1,y1), (x2,y2),(255,255,255),-1)
        imgcropped= cv2.bitwise_and(image,image,mask=x)
        return imgcropped



    def and_mask(image1,image2):
        anded_img= cv2.bitwise_and(image1,image2)
        return anded_img


    def or_mask(image1,image2):
        ored_img= cv2.bitwise_or(image1,image2)
        return ored_img
        

    def uniform_mask(image):
        shape= np.shape(image)
        uni_img= np.full(shape=shape,fill_value=255)
        return uni_img
        

    def cut(image1,image2):
        imgcropped= np.subtract(image1,image2) 
        return imgcropped
        



    def select(img,no_boxes,choice,value,result):
        img_indx=[5]
        box_no_indx= list(result.keys())[0]       
        box_no= result.get(box_no_indx)
        if no_boxes!=0:
            for index in np.arange(1,5):
                img_indx.append(list(result.keys())[index])
        if box_no==0:
            Image.img_box1= result
        elif box_no==1:
            Image.img_box2= result
        imageR = Image(img)
        freq , magnitude_spectrum , phase_spectrum = imageR.getFourier()  
        if choice== "1":
            if no_boxes==2:
                mask1= Mask.mask(phase_spectrum,Image.img_box1.get(img_indx[1]),Image.img_box1.get(img_indx[2]),Image.img_box1.get(img_indx[3]),Image.img_box1.get(img_indx[4]))
                mask2= Mask.mask(phase_spectrum,Image.img_box2.get(img_indx[1]),Image.img_box2.get(img_indx[2]),Image.img_box2.get(img_indx[3]),Image.img_box2.get(img_indx[4]))
                if value== "AND":
                    Image.phase= Mask.and_mask(mask1,mask2)
                elif value== "OR":
                    Image.phase= Mask.or_mask(mask1,mask2)              
            if no_boxes==1: 
                Image.phase= Mask.mask(phase_spectrum,result.get(img_indx[1]),result.get(img_indx[2]),result.get(img_indx[3]),result.get(img_indx[4]))                
            elif no_boxes==0:
                Image.phase= Mask.uniform_mask(phase_spectrum)
            Image.croppedphase=  Mask.cut(phase_spectrum,Image.phase)              
        elif choice== "2":
            if no_boxes==2:
                mask1= Mask.mask(magnitude_spectrum,Image.img_box1.get(img_indx[1]),Image.img_box1.get(img_indx[2]),Image.img_box1.get(img_indx[3]),Image.img_box1.get(img_indx[4]))
                mask2= Mask.mask(magnitude_spectrum,Image.img_box2.get(img_indx[1]),Image.img_box2.get(img_indx[2]),Image.img_box2.get(img_indx[3]),Image.img_box2.get(img_indx[4]))
                if value== "AND": 
                    Image.magnitude=  Mask.and_mask(mask1,mask2)
                elif value== "OR":
                    Image.magnitude= Mask.or_mask(mask1,mask2)
            if no_boxes==1: 
                Image.magnitude=  Mask.mask(magnitude_spectrum,result.get(img_indx[1]),result.get(img_indx[2]),result.get(img_indx[3]),result.get(img_indx[4]))
            elif no_boxes==0:
                Image.magnitude=  Mask.uniform_mask(magnitude_spectrum)
            Image.croppedmagnitude=  Mask.cut(magnitude_spectrum,Image.magnitude)   
        return Image.phase,Image.magnitude,Image.croppedphase,Image.croppedmagnitude