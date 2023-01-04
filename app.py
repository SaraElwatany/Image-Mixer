from flask import Flask , flash, request, redirect, url_for, render_template
import numpy as np
import matplotlib.pyplot as plt
import cv2
from Image import Image
from ImageProcessing import ImageProcessing
from Mask import Mask
import json
import urllib.request
import os
import base64
from werkzeug.utils import secure_filename


app = Flask(__name__)


UPLOAD_FOLDER = 'static/Images/'
 
app.secret_key = "secret key"




 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



image1 = Image(Image.imgs[0])
image2 = Image(Image.imgs[1])





@app.route('/boxes1', methods=['POST'])
def boxes1():
    output = request.get_json()
    result1 = json.loads(output)                 #this converts the json output to a python dictionary result
    indx= list(result1.keys())[0]
    Image.no_boxes1= result1.get(indx)
    return result1



@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    result = json.loads(output)                 #this converts the json output to a python dictionary
    Image.phase,Image.magnitude,Image.croppedphase,Image.croppedmagnitude= Mask.select(img=Image.imgs[0],no_boxes=Image.no_boxes1,choice=Image.option1,value=Image.value1,result=result)
    return result



   
@app.route('/boxes2', methods=['POST'])
def boxes2():
    output= request.get_json()
    result3= json.loads(output)         
    indx= list(result3.keys())[0]
    Image.no_boxes2= result3.get(indx)
    return result3
   


@app.route('/test2', methods=['POST'])
def test2():
    output = request.get_json()
    result2 = json.loads(output)      #this converts the json output to a python dictionary
    Image.phase, Image.magnitude, Image.croppedphase, Image.croppedmagnitude= Mask.select(img = Image.imgs[1], no_boxes=Image.no_boxes2,choice=Image.option2,value=Image.value2,result=result2)
    return result2





@app.route('/choice1', methods=['POST'])
def choice1():
    output= request.get_json()
    ch1= json.loads(output)         #this converts the json output to a python dictionary
    indx= list(ch1.keys())[0]
    Image.value1= ch1.get(indx)
    return ch1



@app.route('/choice2', methods=['POST'])
def choice2():
    output= request.get_json()
    ch2= json.loads(output)         #this converts the json output to a python dictionary
    indx= list(ch2.keys())[0]
    Image.value2= ch2.get(indx)
    return ch2


@app.route('/opt1', methods=['POST'])
def opt1():
    output= request.get_json()
    opt= json.loads(output)         #this converts the json output to a python dictionary
    indx= list(opt.keys())[0]
    Image.option1= opt.get(indx)
    return opt



@app.route('/opt2', methods=['POST'])
def opt2():
    output= request.get_json()
    opt= json.loads(output)         #this converts the json output to a python dictionary
    indx= list(opt.keys())[0]
    Image.option2= opt.get(indx)
    return opt



@app.route('/', methods= ['GET','POST'])
def upload_image(): 
    if request.method == 'POST' : 
        for indx in np.arange(0,4):
            Image.options[indx] = request.form.get(f'{indx+1}')
        img1 = request.files.get('img1')
        img2 = request.files.get('img2')
        if img1:
            filename = secure_filename(img1.filename)
            img1.save(os.path.join(UPLOAD_FOLDER,filename))
            Image.imgs[0]=os.path.join(UPLOAD_FOLDER, filename)
        if img2:
            filename = secure_filename(img2.filename)
            img2.save(os.path.join(UPLOAD_FOLDER,filename))
            Image.imgs[1]=os.path.join(UPLOAD_FOLDER, filename)   
    
    freq_a , magnitude_a , phase_a = image1.getFourier()
    freq_b , magnitude_b , phase_b = image2.getFourier()
    magnitudes=[magnitude_a,magnitude_b,Image.magnitude]
    phases=[phase_a,phase_b,Image.phase]
    for count in np.arange(0,3):
        Image.save( magnitude=magnitudes[count] , phase= phases[count] , number= count+1)

    
    
 
    if Image.options[0] == "Phase1 & Magnitude2":
        ImageProcessing.mixImages(freq_mag=freq_b,freq_phase=freq_a)
    elif Image.options[1] == "Phase2 & Magnitude1":
        ImageProcessing.mixImages(freq_mag=freq_a,freq_phase=freq_b)
    elif Image.options[2] == "Select":
        ImageProcessing.combined_mask(magnitude=Image.magnitude,phase=Image.phase)
    elif Image.options[3] == "Cut":
        ImageProcessing.combined_mask(magnitude = Image.croppedmagnitude,phase = Image.croppedphase)
    return render_template('Mixture.html' , img1=Image.imgs[0] , img2=Image.imgs[1] )
  



if __name__ == '__main__':
    app.run(debug=True, port=8000)



