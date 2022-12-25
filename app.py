from flask import Flask , flash, request, redirect, url_for, render_template
import numpy as np
import matplotlib.pyplot as plt
import cv2
import functions
import json
import urllib.request
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER = 'static/Images/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('Mixture.html')



@app.route('/', methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_names.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
 
    img_a , freq_a , magnitude_spectrum_a , phase_spectrum_a = functions.imageFourier(file=os.path.join(app.config['UPLOAD_FOLDER'],file_names[0]))
    img_b , freq_b , magnitude_spectrum_b , phase_spectrum_b = functions.imageFourier(file=os.path.join(app.config['UPLOAD_FOLDER'],file_names[1]))

    functions.plotspectrums(img_a , magnitude_spectrum_a , phase_spectrum_a , img_b , magnitude_spectrum_b , phase_spectrum_b)

    

    combined = np.multiply(np.abs(freq_a), np.exp(1j*np.angle(freq_b)))
    imgCombined = np.real(np.fft.ifft2(combined))

    plt.imsave('static\Images\output.png',imgCombined, cmap='gray')


    return render_template('Mixture.html')



# @app.route('/')
# def imageMixing():



#     img_a , freq_a , magnitude_spectrum_a , phase_spectrum_a = functions.imageFourier("static\Images\moonknight1.jpg")
#     img_b , freq_b , magnitude_spectrum_b , phase_spectrum_b = functions.imageFourier("static\Images\\train.jpg")
    

    
#     functions.plotspectrums(img_a , magnitude_spectrum_a , phase_spectrum_a , img_b , magnitude_spectrum_b , phase_spectrum_b)


#     # combined = np.multiply(np.abs(freq_a), np.exp(1j*np.angle(freq_b)))
#     # imgCombined = np.real(np.fft.ifft2(combined))

#     # plt.imsave('static\Images\output.png',imgCombined, cmap='gray')



#     return render_template("Mixture.html")



@app.route('/test', methods=['POST'])
def test():
    output = request.get_json()
    print(output)                   # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output)         #this converts the json output to a python dictionary
    print(result)                       # Printing the new dictionary
    print(type(result))                #this shows the json converted as a python dictionary
    indx1= list(result.keys())[0]
    indx2= list(result.keys())[1]
    indx3= list(result.keys())[2]
    indx4= list(result.keys())[3]
    functions.cut('static/Images/sky.jpg',result.get(indx1), result.get(indx2), result.get(indx3), result.get(indx4))
    return result





if __name__ == '__main__':
    app.run(debug=True, port=8000)

