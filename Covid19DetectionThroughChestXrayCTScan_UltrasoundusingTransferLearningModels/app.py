from keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename


import os, sys, glob, re

app = Flask(__name__)

model_path1 = "cxr_model.h5"
model_path2 = "ct_model.h5"
model_path3 = "ultra_model.h5"

CXR = load_model(model_path1)
CTS = load_model(model_path2)
USI = load_model(model_path3)

classes1 = {1:"NONCOVID19",0:"COVID-19",2:"PNEUMONIA"}
classes2 = {1:"NONCOVID19",0:"COVID-19"}
classes3 = {1:"NONCOVID19",0:"COVID-19",2:"PNEUMONIA"}


def model_predict1(image_path,model):
    print("Predicted")
    image = load_img(image_path,target_size=(224,224))
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image,axis=0)
    
    result = np.argmax(model.predict(image))
    prediction = classes1[result]  
    
    if result == 0:
        print("COVID-19")
        return "COVID-19", "cxr1.html" 

        
    elif result == 1:
         print("NORMAL")
         return "NORMAL","cxr2.html"
    
    elif result == 2:
         print("PNEUMONIA")
         return "PNEUMONIA","cxr3.html"
        
        
def model_predict2(image_path,model):
    print("Predicted")
    image = load_img(image_path,target_size=(224,224))
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image,axis=0)
    
    result = np.argmax(model.predict(image))
    prediction = classes2[result]  
    
    if result == 0:
        print("COVID-19")
        return "COVID-19", "ct1.html" 

        
    elif result == 1:
         print("NORMAL")
         return "NORMAL","ct2.html"

def model_predict3(image_path,model):
    print("Predicted")
    image = load_img(image_path,target_size=(224,224))
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image,axis=0)
    
    result = np.argmax(model.predict(image))
    prediction = classes3[result]  
    
    if result == 0:
        print("COVID-19")
        return "COVID-19", "us1.html" 

        
    elif result == 1:
         print("NORMAL")
         return "NORMAL","us2.html"
    
    elif result == 2:
         print("PNEUMONIA")
         return "PNEUMONIA","us3.html"


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict1',methods=['GET','POST'])
def predict1():
    print("Entered")
    if request.method == 'POST':
        print("Entered here")
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)

        print("@@ Predicting class......")
        pred, output_page = model_predict1(file_path,CXR)
              
        return render_template(output_page, pred_output = pred, user_image = file_path)
    


        
        

@app.route('/index1',methods=['GET'])
def index1():
    return render_template('index1.html')

@app.route('/predict2',methods=['GET','POST'])
def predict2():
    print("Entered")
    if request.method == 'POST':
        print("Entered here")
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)

        print("@@ Predicting class......")
        pred, output_page = model_predict2(file_path,CTS)
              
        return render_template(output_page, pred_output = pred, user_image = file_path)
    

@app.route('/index3',methods=['GET'])
def index3():
    return render_template('index2.html')

@app.route('/predict3',methods=['GET','POST'])
def predict3():
    print("Entered")
    if request.method == 'POST':
        print("Entered here")
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)

        print("@@ Predicting class......")
        pred, output_page = model_predict3(file_path,USI)
              
        return render_template(output_page, pred_output = pred, user_image = file_path)
    
if __name__ == '__main__':
    app.run()
    
