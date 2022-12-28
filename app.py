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

dimensions1=[]
dimensions2=[]
fourier1= []
fourier2= []


UPLOAD_FOLDER = 'static/Images/'
 
app.secret_key = "secret key"

 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
imgs = ['static\Images\image1.png' , 'static\Images\image2.png']

@app.route('/', methods= ['GET','POST'])

def upload_image():
    if request.method == 'POST' :

        
        img1 = request.files['img1']
        img2 = request.files['img2']
        if img1:
            filename = secure_filename(img1.filename)
            img1.save(os.path.join(UPLOAD_FOLDER,filename))
            imgs[0]=os.path.join(UPLOAD_FOLDER, filename)
    
        
        if img2:
            filename = secure_filename(img2.filename)
            img2.save(os.path.join(UPLOAD_FOLDER,filename))
            imgs[1]=os.path.join(UPLOAD_FOLDER, filename)

   
        # for file in files:
        #     if file and allowed_file(file.filename):
        #         filename = secure_filename(file.filename)
        #         file_names.append(filename)
        #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     else:
        #         flash('Allowed image types are -> png, jpg, jpeg, gif')
        #         return redirect(request.url)
 
        # img_a = functions.readImage(file=os.path.join(app.config['UPLOAD_FOLDER'],file_names[0]))
        # img_b = functions.readImage(file=os.path.join(app.config['UPLOAD_FOLDER'],file_names[1]))

        # freq_a , magnitude_spectrum_a , phase_spectrum_a = functions.imageFourier(img=img_a)
        # freq_b , magnitude_spectrum_b , phase_spectrum_b = functions.imageFourier(img=img_b)

        # functions.plotspectrums(img_a , magnitude_spectrum_a , phase_spectrum_a , img_b , magnitude_spectrum_b , phase_spectrum_b)

        # if np.size(img_b) != np.size(img_a) :
        #     new_height, new_width = np.shape(img_a)
        #     img_b = cv2.resize(img_b, dsize=[new_width,new_height])
        #     freq_b = np.fft.fft2(img_b)


        # combined = np.multiply(np.abs(freq_a), np.exp(1j*np.angle(freq_b)))
        # imgCombined = np.real(np.fft.ifft2(combined))

        # plt.imsave('static\Images\output.png',imgCombined, cmap='gray')
        return render_template('Mixture.html' , img1=imgs[0] , img2=imgs[1] )


    return render_template('Mixture.html' , img1=imgs[0] , img2=imgs[1] )

   

@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    #print(output)                   # This is the output that was stored in the JSON within the browser
    result = json.loads(output)         #this converts the json output to a python dictionary
    dimensions1= result
    print("1: ", result)                       # Printing the new dictionary
    #print(type(result))                #this shows the json converted as a python dictionary
    return result

   

@app.route('/test2', methods=['POST'])
def test2():
    output = request.get_json()
    result = json.loads(output)         #this converts the json output to a python dictionary
    dimensions2= result
    print("2: ", result)                       # Printing the new dictionary
    print(type(result))                #this shows the json converted as a python dictionary
    return result



@app.route('/imageMixing')
def combination_cropped(option1, option2):
    indx1= list(dimensions1.keys())[0]
    indx2= list(dimensions1.keys())[1]
    indx3= list(dimensions1.keys())[2]
    indx4= list(dimensions1.keys())[3]

    pos1= list(dimensions1.keys())[0]
    pos2= list(dimensions1.keys())[1]
    pos3= list(dimensions1.keys())[2]
    pos4= list(dimensions1.keys())[3]
    img1 , fourier1 , mag1 , phase1 = functions.imageFourier("image1.png")
    img2 , fourier2 , mag2 , phase2 = functions.imageFourier("image2.png")
    functions.plotspectrums(img1 , mag1 , phase1, img2, mag2 , phase2)
 
    if option1== True:                    # first Phase and second mag    
        functions.mask("phase1.png",1,"phase",dimensions1.get(indx1),dimensions1.get(indx2),dimensions1.get(indx3),dimensions1.get(indx4))
        functions.mask("magnitude2.png",2,"magnitude",dimensions2.get(pos1),dimensions2.get(pos2),dimensions2.get(pos3),dimensions2.get(pos4))
        crop1 , four_crop1 , mag_crop1 , phase_crop1 = functions.imageFourier("maskedphase1.jpg")
        crop2 , four_crop2 , mag_crop2 , phase_crop2 = functions.imageFourier("maskedmagnitude2.jpg")


        combined = np.multiply(np.abs(four_crop2), np.exp(1j*np.angle(four_crop1)))
        imgCombined = np.real(np.fft.ifft2(combined))
        plt.imsave('Images\output_cropped.png',imgCombined, cmap='gray')
        

    elif option2== True:                    # first mag and second phase
        functions.mask("magnitude1.png",1,"magnitude",dimensions1.get(indx1),dimensions1.get(indx2),dimensions1.get(indx3),dimensions1.get(indx4))
        functions.mask("phase2.png",2,"phase",dimensions2.get(pos1),dimensions2.get(pos2),dimensions2.get(pos3),dimensions2.get(pos4))
        crop1 , four_crop1 , mag_crop1 , phase_crop1 = functions.imageFourier("maskedmagnitude1.jpg")
        crop2 , four_crop2 , mag_crop2 , phase_crop2 = functions.imageFourier("maskedphase2.jpg")


        combined = np.multiply(np.abs(four_crop1), np.exp(1j*np.angle(four_crop2)))
        imgCombined = np.real(np.fft.ifft2(combined))
        plt.imsave('Images\output_cropped.png',imgCombined, cmap='gray')


    return render_template("Mixture.html")

  

if __name__ == '__main__':
    app.run(debug=True, port=8000)



