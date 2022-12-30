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

   


@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    #print(output)                   # This is the output that was stored in the JSON within the browser
    result = json.loads(output)         #this converts the json output to a python dictionary
    no_boxes= list(result.keys())[0]
    indx1= list(result.keys())[1]
    indx2= list(result.keys())[2]
    indx3= list(result.keys())[3]
    indx4= list(result.keys())[4]    
    #print("1: ", result)                       # Printing the new dictionary
    #print(type(result))                #this shows the json converted as a python dictionary
    img1 , fourier1 , mag1 , phase1 = functions.imageFourier("image1.png")
    functions.plotspectrums(img1 , mag1 , phase1 , 1)   
    #phase1= functions.readImage("static\Images\phase1.png")
    #magnitude1= functions.readImage("static\Images\magnitude1.png")
    if no_boxes== 1:
        functions.mask("phase1.png",1,"phase",result.get(indx1),result.get(indx2),result.get(indx3),result.get(indx4))
        functions.mask("magnitude1.png",1,"magnitude",result.get(indx1),result.get(indx2),result.get(indx3),result.get(indx4))

    elif no_boxes== 2:
        functions.mask("phase1.png",1,"phase",result.get(indx1),result.get(indx2),result.get(indx3),result.get(indx4))
        functions.mask("magnitude1.png",1,"magnitude",result.get(indx1),result.get(indx2),result.get(indx3),result.get(indx4))
        functions.mask("phase1.png",2,"phase",result.get(indx1),result.get(indx2),result.get(indx3),result.get(indx4))
        functions.mask("magnitude1.png",2,"magnitude",result.get(indx1),result.get(indx2),result.get(indx3),result.get(indx4))
        phas1= functions.readImage("1phase1.png")
        phas2= functions.readImage("2phase1.png")
        phase_anded= cv2.bitwise_and(phas1,phas2)
        phase_anded.save(f'static/Images/"phase1_and"')
        phase_ored= cv2.bitwise_or(phas1,phas2)
        phase_ored.save(f'static/Images/"phase1_or"')
        magnitude1= functions.readImage("1magnitude1.png")
        magnitude2= functions.readImage("2magnitude1.png")
        magnitude_anded= cv2.bitwise_and(magnitude1,magnitude2)
        magnitude_anded.save(f'static/Images/"magnitude1_and"')
        magnitude_ored= cv2.bitwise_or(magnitude1,magnitude2)
        magnitude_ored.save(f'static/Images/"magnitude1_or"')
    
    elif no_boxes==0:
        functions.uniform_mask("phase1.png",1,"phase",result.get(indx1),result.get(indx2),result.get(indx3),result.get(indx4))
        functions.uniform_mask("magnitude1.png",1,"magnitude",result.get(indx1),result.get(indx2),result.get(indx3),result.get(indx4))

    return result
   
   
   
   

@app.route('/test2', methods=['POST'])
def test2():
    output = request.get_json()
    result2 = json.loads(output)         #this converts the json output to a python dictionary
    #print("2: ", result2)                       # Printing the new dictionary
    #print(type(result2))                #this shows the json converted as a python dictionary
    no_boxes= list(result2.keys())[0]
    indx1= list(result2.keys())[1]
    indx2= list(result2.keys())[2]
    indx3= list(result2.keys())[3]
    indx4= list(result2.keys())[4]
    img2 , fourier2 , mag2 , phase2 = functions.imageFourier("image2.png")
    functions.plotspectrums(img2, mag2 , phase2, 2)
    if no_boxes== 1:
        functions.mask("phase2.png",1,"phase",result2.get(indx1),result2.get(indx2),result2.get(indx3),result2.get(indx4))
        functions.mask("magnitude2.png",1,"magnitude",result2.get(indx1),result2.get(indx2),result2.get(indx3),result2.get(indx4))

    elif no_boxes== 2:
        functions.mask("phase2.png",1,"phase",result2.get(indx1),result2.get(indx2),result2.get(indx3),result2.get(indx4))
        functions.mask("magnitude2.png",1,"magnitude",result2.get(indx1),result2.get(indx2),result2.get(indx3),result2.get(indx4))
        functions.mask("phase2.png",2,"phase",result2.get(indx1),result2.get(indx2),result2.get(indx3),result2.get(indx4))
        functions.mask("magnitude2.png",2,"magnitude",result2.get(indx1),result2.get(indx2),result2.get(indx3),result2.get(indx4))
        phas1= functions.readImage("1phase2.png")
        phas2= functions.readImage("2phase2.png")
        phase_anded= cv2.bitwise_and(phas1,phas2)
        phase_anded.save(f'static/Images/"phase2_and"')
        phase_ored= cv2.bitwise_or(phas1,phas2)
        phase_ored.save(f'static/Images/"phase2_or"')
        magnitude1= functions.readImage("1magnitude2.png")
        magnitude2= functions.readImage("2magnitude2.png")
        magnitude_anded= cv2.bitwise_and(magnitude1,magnitude2)
        magnitude_anded.save(f'static/Images/"magnitude2_and"')
        magnitude_ored= cv2.bitwise_or(magnitude1,magnitude2)
        magnitude_ored.save(f'static/Images/"magnitude2_or"')
    
    elif no_boxes==0:
        functions.uniform_mask("phase2.png",1,"phase",result2.get(indx1),result2.get(indx2),result2.get(indx3),result2.get(indx4))
        functions.uniform_mask("magnitude2.png",1,"magnitude",result2.get(indx1),result2.get(indx2),result2.get(indx3),result2.get(indx4))

    return result2



  

if __name__ == '__main__':
    app.run(debug=True, port=8000)



