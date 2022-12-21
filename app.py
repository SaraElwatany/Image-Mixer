from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import cv2
import functions
import json
# import sys, asyncio

# if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = Flask(__name__)




@app.route("/")
def index():
    message = "Hello to test page"
    return render_template("Mixture.html" , msg = message)



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



@app.route('/imageMixing')
def imageMixing():

    img_a , freq_a , magnitude_spectrum_a , phase_spectrum_a = functions.imageFourier("moonknight1.jpg")
    img_b , freq_b , magnitude_spectrum_b , phase_spectrum_b = functions.imageFourier("train.jpg")
    

    # print(np.shape(freq_a))
    # print(np.shape(freq_b))


    
    functions.plotspectrums(img_a , magnitude_spectrum_a , phase_spectrum_a , img_b , magnitude_spectrum_b , phase_spectrum_b)


    combined = np.multiply(np.abs(freq_a), np.exp(1j*np.angle(freq_b)))
    imgCombined = np.real(np.fft.ifft2(combined))

    plt.imsave('D:\Edu\DSP\Tasks\Task4\DSP_Task_4\static\Images\output.png',imgCombined, cmap='gray')



    return render_template("Mixture.html")




if __name__ == '__main__':
    app.run(debug=True, port=8000)

