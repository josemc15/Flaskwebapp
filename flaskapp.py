from flask import Flask, render_template, request
import re
import pandas as pd
import copy
import pickle 
import joblib


model = pickle.load(open('C:/Users/mcjos/Desktop/Project/New folder/final project\labour.pkl','rb'))
impute = joblib.load('meanimpute')
winsor = joblib.load('winsor')
encoding = joblib.load('encoding')
scale = joblib.load('minmax')


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    

@app.route('/success',methods = ['POST'])
def success():
    if request.method == "POST":
        f = request.files['file']
        data_new = pd.read_excel(f)
        #data2 = copy.deepcopy(data)
        #imputation
        Employee_data_new1 = data_new.drop(['Emp_Name','Experience','Bp_per_Minute','RFID_Tag','Total Working Hours','Remaining_Working_Hours','Total Working Hours','Motion_Indication','Noise_Detection','Infrared_Sensor'], axis=1)
        numeric_features = Employee_data_new1.select_dtypes(exclude=['object']).columns
        
        #numeric_features
        
        #categorical_features = labour_new1.select_dtypes(include=['object']).columns
        
        #categorical_features
        
        impute1 = pd.DataFrame(impute.transform(Employee_data_new1),columns=numeric_features)
        
        impute[['Age','Heart_Beat', 'Temperature']] = winsor.transform(impute[['Age','Heart_Beat', 'Temperature']])

        
        clean2=pd.DataFrame(scale.transform(impute1))
        clean3=pd.DataFrame(encoding.transform(labour_new1).todense())
        clean_data=pd.concat([clean2,clean3],axis=1,ignore_index=True)
        prediction=pd.DataFrame(model.predict(clean_data),columns=['Productivity'])
        final_data=pd.concat([prediction, labour_new1],axis=1)
        
        return render_template('data.html', Y = final_data.to_html(justify='center'))
    
    
if __name__=='__main__':
    app.run(debug = True)
