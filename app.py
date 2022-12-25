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




dimensions1=[]
dimensions2=[]
fourier1= []
fourier2= []
phase1= []
phase2= []



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
    dimensions1= result
    print("1: ", result)                       # Printing the new dictionary
    print(type(result))                #this shows the json converted as a python dictionary
    indx1= list(result.keys())[0]
    indx2= list(result.keys())[1]
    indx3= list(result.keys())[2]
    indx4= list(result.keys())[3]
    functions.cut('static/Images/train.jpg',dimensions1.get(indx1), dimensions1.get(indx2), dimensions1.get(indx3), dimensions1.get(indx4),1)
    return result


@app.route('/test2', methods=['POST'])
def test2():
    output = request.get_json()
    print(output)                   # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output)         #this converts the json output to a python dictionary
    dimensions2= result
    print("2: ", result)                       # Printing the new dictionary
    print(type(result))                #this shows the json converted as a python dictionary
    indx1= list(result.keys())[0]
    indx2= list(result.keys())[1]
    indx3= list(result.keys())[2]
    indx4= list(result.keys())[3]
    #imagename= 
    functions.cut('static/Images/train.jpg',dimensions2.get(indx1), dimensions2.get(indx2), dimensions2.get(indx3), dimensions2.get(indx4),2)
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





def combination_cropped(option1, option2):
    img1 , fourier1 , mag1 , phase1 = functions.imageFourier("cropped1.jpg")
    img2 , fourier2 , mag2 , phase2 = functions.imageFourier("cropped2.jpg")
    flat1= list(img1.flatten())
    flat2= list(img2.flatten())
    modified= flat2
    maxrows= img1.shape[0]
    maxcolumns= img1.shape[1]
    maxrows2= img2.shape[0]
    maxcolumns2= img2.shape[1]
    count=1
    diff= np.abs(maxcolumns-maxcolumns2)
    if len(flat1)  > len(flat2):  
        #print(img2)
        #print(img2.shape)
        #print("--------------------------------------------------------------------------------------")
        #print(flat2)   
        #print("--------------------------------------------------------------------------------------")
        for i in np.arange(maxcolumns2,maxcolumns2*maxrows2,maxcolumns2+diff):
            for j in np.arange(i,(maxcolumns*count)):
                flat2.insert(j, 0) 
            count+=1
        while(len(flat1) > len(flat2)):
            flat2.append(0)
        modified= np.array(flat2).reshape(img1.shape)
        #print(modified)
        fourier2 = np.fft.fft2(modified)
    if len(flat1)  < len(flat2):
        for i in np.arange(maxcolumns,maxcolumns*maxrows,maxcolumns+diff):
            for j in np.arange(i,(maxcolumns2*count)):
                flat1.insert(j, 0) 
            count+=1
        while(len(flat2) > len(flat1)):
            flat1.append(0)
        modified= np.array(flat1).reshape(img2.shape)
        fourier1 = np.fft.fft2(modified)

    if option1== True:              # first Phase and second mag
        combined = np.multiply(np.abs(fourier2), np.exp(1j*np.angle(fourier1)))
        imgCombined = np.real(np.fft.ifft2(combined))
        plt.imsave('Images\output_cropped.jpg',imgCombined, cmap='gray')

    elif option2== True:                    # first mag and second phase
        combined = np.multiply(np.abs(fourier1), np.exp(1j*np.angle(fourier2)))
        imgCombined = np.real(np.fft.ifft2(combined))
        plt.imsave('Images\output_cropped.jpg',imgCombined, cmap='gray')






if __name__ == '__main__':
    app.run(debug=True, port=8000)



