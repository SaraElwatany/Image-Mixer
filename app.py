from flask import Flask , flash, request, redirect, url_for, render_template
import numpy as np
import matplotlib.pyplot as plt
import cv2
import functions
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
imgs = ['static\Images\image1.png' , 'static\Images\image2.png']
options = ["A","B"]
option1= "5"
option2= "5"
value1= "N"
value2= "N"

@app.route('/', methods= ['GET','POST'])

def upload_image():

    print(request.method)

    if request.method == 'POST' :
   
        options[0] = request.form.get('1')
        options[1] = request.form.get('2')
        img1 = request.files.get('img1')
        img2 = request.files.get('img2')
        print(img1)
        print(img2)
        print(options[0])
        print(options[1])

        if img1:
            filename = secure_filename(img1.filename)
            img1.save(os.path.join(UPLOAD_FOLDER,filename))
            imgs[0]=os.path.join(UPLOAD_FOLDER, filename)

        if img2:
            filename = secure_filename(img2.filename)
            img2.save(os.path.join(UPLOAD_FOLDER,filename))
            imgs[1]=os.path.join(UPLOAD_FOLDER, filename)
          
   
    img_a = functions.readImage(imgs[0])
    img_b = functions.readImage(imgs[1])
    print(img_a)
    print(img_b)

    if np.size(img_b) != np.size(img_a) :
        new_height, new_width = np.shape(img_a)
        img_b = cv2.resize(img_b, dsize=[new_width,new_height])


    freq_a , magnitude_spectrum_a , phase_spectrum_a = functions.imageFourier(img=img_a)
    freq_b , magnitude_spectrum_b , phase_spectrum_b = functions.imageFourier(img=img_b)

    functions.plotspectrums(magnitude_spectrum_a , phase_spectrum_a ,1)
    functions.plotspectrums(magnitude_spectrum_b , phase_spectrum_b ,2)

    if options[0] == "Phase1 & Magnitude2":
        functions.combined(freq_mag=freq_b,freq_phase=freq_a)
        print("Phase1Magnitude2")
    elif options[1] == "Phase2 & Magnitude1":
        functions.combined(freq_mag=freq_a,freq_phase=freq_b)
        print("Phase2Magnitude1")
    else:
        functions.combined(freq_mag=freq_b,freq_phase=freq_a)
        print("defaultChoice")
        


    return render_template('Mixture.html' , img1=imgs[0] , img2=imgs[1] )

   


@app.route('/boxes1', methods=['POST'])
def boxes1():
    global no_boxes1
    
    output = request.get_json()
    result = json.loads(output)                 #this converts the json output to a python dictionary result
    indx= list(result.keys())[0]
    no_boxes1= result.get(indx)
    #print("Number of Boxes for first image: ", no_boxes1) 
    return result




@app.route('/test', methods=['POST'])
def test():
    global img1_box1
    global img1_box2
    global result
    if no_boxes1!=0:
        box_no_indx= list(result.keys())[0]
        img1_indx1= list(result.keys())[1]
        img1_indx2= list(result.keys())[2]
        img1_indx3= list(result.keys())[3]
        img1_indx4= list(result.keys())[4]
        box_no= result.get(box_no_indx)
        if box_no==0:
          img1_box1= result 
        elif box_no==1:
          img1_box2= result 
    output = request.get_json()
    result = json.loads(output)         #this converts the json output to a python dictionary
    #print("Result: ", result) 
    #print("Box Number: ", box_no)
    if option1== "1":
        if no_boxes1==2:
            print(value1)
            print('-------------------------------------------------------------')
            print(option1) 
            functions.mask("static\Images\phase1.png",11,"phase",img1_box1.get(img1_indx1),img1_box1.get(img1_indx2),img1_box1.get(img1_indx3),img1_box1.get(img1_indx4))
            functions.mask("static\Images\phase1.png",12,"phase",img1_box2.get(img1_indx1),img1_box2.get(img1_indx2),img1_box2.get(img1_indx3),img1_box2.get(img1_indx4))
            if value1== "AND":
                phase1= functions.and_mask('static\Images\maskedphase11.png','static\Images\maskedphase12.png',"phase_out",1)
            elif value1== "OR":
                phase1= functions.or_mask('static\Images\maskedphase11.png','static\Images\maskedphase12.png',"phase_out",1)
        elif no_boxes1==1: 
            functions.mask("static\Images\phase1.png",11,"phase",img1_box1.get(img1_indx1),img1_box1.get(img1_indx2),img1_box1.get(img1_indx3),img1_box1.get(img1_indx4))
        elif (no_boxes1==0 and no_boxes2==1) or (no_boxes1==0 and no_boxes2==2):
            functions.uniform_mask("static\Images\phase1.png",11,"phase")
    
        
    elif option1== "2":
        if no_boxes1==2:
            print(value1)
            print('-------------------------------------------------------------')
            print(option1) 
            functions.mask("static\Images\magnitude1.png",11,"magnitude",img1_box1.get(img1_indx1),img1_box1.get(img1_indx2),img1_box1.get(img1_indx3),img1_box1.get(img1_indx4))
            functions.mask("static\Images\magnitude1.png",12,"magnitude",img1_box2.get(img1_indx1),img1_box2.get(img1_indx2),img1_box2.get(img1_indx3),img1_box2.get(img1_indx4))
            if value1== "AND": 
                mag1= functions.and_mask('static\Images\maskedmagnitude11.png','static\Images\maskedmagnitude12.png'"magnitude_out",1)
            elif value1== "OR":
                mag1= functions.or_mask('static\Images\maskedmagnitude11.png','static\Images\maskedmagnitude12.png'"magnitude_out",1)
        elif no_boxes1==1: 
            functions.mask("static\Images\phase1.png",11,"phase",img1_box1.get(img1_indx1),img1_box1.get(img1_indx2),img1_box1.get(img1_indx3),img1_box1.get(img1_indx4))
        elif (no_boxes1==0 and no_boxes2==1) or (no_boxes1==0 and no_boxes2==2):
            functions.uniform_mask("static\Images\magnitude1.png",11,"magnitude")    
    return result


   
@app.route('/boxes2', methods=['POST'])
def boxes2():
    global no_boxes2
    
    output= request.get_json()
    result= json.loads(output)         #this converts the json output to a python dictionary
    indx= list(result.keys())[0]
    no_boxes2= result.get(indx)
   # print("Number of boxes for second image: ", no_boxes2) 
    return result
   



@app.route('/test2', methods=['POST'])
def test2():
    global img2_box1
    global img2_box2
    global result2
    if no_boxes2!=0:
        box_no_indx= list(result2.keys())[0]
        img2_indx1= list(result2.keys())[1]
        img2_indx2= list(result2.keys())[2]
        img2_indx3= list(result2.keys())[3]
        img2_indx4= list(result2.keys())[4]
        box_no= result2.get(box_no_indx)
        if box_no==0:
            img2_box1= result2 
        elif box_no==1:
            img2_box2= result2
    output = request.get_json()
    result2 = json.loads(output)         #this converts the json output to a python dictionary
    if option2== "1":
        if no_boxes2==2:
            print(value1)
            print('-------------------------------------------------------------')
            print(option1) 
            functions.mask("static\Images\phase2.png",21,"phase",img2_box1.get(img2_indx1),img2_box1.get(img2_indx2),img2_box1.get(img2_indx3),img2_box1.get(img2_indx4))
            functions.mask("static\Images\phase2.png",22,"phase",img2_box2.get(img2_indx1),img2_box2.get(img2_indx2),img2_box2.get(img2_indx3),img2_box2.get(img2_indx4))
            if value1== "AND":
                phase1= functions.and_mask('static\Images\maskedphase21.png','static\Images\maskedphase22.png',"phase_out",2)
            elif value1== "OR":
                phase1= functions.or_mask('static\Images\maskedphase21.png','static\Images\maskedphase22.png',"phase_out",2)
        elif no_boxes2==1: 
            functions.mask("static\Images\phase2.png",21,"phase",img2_box1.get(img2_indx1),img2_box1.get(img2_indx2),img2_box1.get(img2_indx3),img2_box1.get(img2_indx4))
        elif (no_boxes2==0 and no_boxes1==1) or (no_boxes2==0 and no_boxes1==2):
            functions.uniform_mask("static\Images\phase2.png",21,"phase")
    
        
    elif option2== "2":
        if no_boxes2==2:
            print(value1)
            print('-------------------------------------------------------------')
            print(option1) 
            functions.mask("static\Images\magnitude2.png",21,"magnitude",img2_box1.get(img2_indx1),img2_box1.get(img2_indx2),img2_box1.get(img2_indx3),img2_box1.get(img2_indx4))
            functions.mask("static\Images\magnitude2.png",22,"magnitude",img2_box2.get(img2_indx1),img2_box2.get(img2_indx2),img2_box2.get(img2_indx3),img2_box2.get(img2_indx4))
            if value1== "AND": 
                mag1= functions.and_mask('static\Images\maskedmagnitude21.png','static\Images\maskedmagnitude22.png'"magnitude_out",2)
            elif value1== "OR":
                mag1= functions.or_mask('static\Images\maskedmagnitude21.png','static\Images\maskedmagnitude22.png'"magnitude_out",2)
        elif no_boxes2==1: 
            functions.mask("static\Images\phase2.png",21,"phase",img2_box1.get(img2_indx1),img2_box1.get(img2_indx2),img2_box1.get(img2_indx3),img2_box1.get(img2_indx4))
        elif (no_boxes2==0 and no_boxes1==1) or (no_boxes2==0 and no_boxes1==2):
            functions.uniform_mask("static\Images\magnitude2.png",21,"magnitude")
    return result2
   
    


@app.route('/choice1', methods=['POST'])
def choice1():
    global value1
    output= request.get_json()
    ch1= json.loads(output)         #this converts the json output to a python dictionary
    indx= list(ch1.keys())[0]
    value1= ch1.get(indx)
    return ch1



@app.route('/choice2', methods=['POST'])
def choice2():
    global value2
    output= request.get_json()
    ch2= json.loads(output)         #this converts the json output to a python dictionary
    indx= list(ch2.keys())[0]
    value2= ch2.get(indx)
    return ch2


@app.route('/opt1', methods=['POST'])
def opt1():
    global option1
    output= request.get_json()
    opt= json.loads(output)         #this converts the json output to a python dictionary
    indx= list(opt.keys())[0]
    option1= opt.get(indx)
    #print(option1)
    return opt



@app.route('/opt2', methods=['POST'])
def opt2():
    global option2
    output= request.get_json()
    opt= json.loads(output)         #this converts the json output to a python dictionary
    indx= list(opt.keys())[0]
    option2= opt.get(indx)
    return opt



  

if __name__ == '__main__':
    app.run(debug=True, port=8000)



