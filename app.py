#This is Heroku Deployment Lectre
from flask import Flask, request, render_template
import os
import pickle

print("Test")
print(os.getcwd())
path = os.getcwd()
print()


with open('Models/Pickle_LR_Model.pkl', 'rb') as f:
    logistic = pickle.load(f)

with open('Models/Pickle_svc_Model.pkl', 'rb') as f:
    svm_model = pickle.load(f)


def get_predictions(age,sex,chest_pain_type,resting_bp,cholesterol,fasting_bloodSugar,resting_ecg,max_heartrate,exercise_induced_angina,oldpeak, slope,num_vessels,thalassemia,req_model):
    mylist = [age, sex, chest_pain_type, resting_bp, cholesterol,fasting_bloodSugar,resting_ecg,max_heartrate,exercise_induced_angina,oldpeak, slope,num_vessels,thalassemia]
    mylist = [float(i) for i in mylist]
    vals = [mylist]

    if req_model == 'Logistic':
        #print(req_model)
        return logistic.predict(vals)[0]
    elif req_model == 'SVM':
        #print(req_model)
        return svm_model.predict(vals)[0]
    else:
        return "Cannot Predict"


app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def my_form_post():
    if request.method == 'POST':
        age = request.form['age']
        sex = request.form['sex']
        chest_pain_type = request.form['cp']
        resting_bp = request.form['trestbps']
        cholesterol = request.form['chol']
        fasting_bloodSugar = request.form['fbs']
        resting_ecg = request.form['restecg']
        max_heartrate  = request.form['thalach']
        exercise_induced_angina = request.form['exang']
        oldpeak = request.form['oldpeak']
        slope = request.form['slope']
        num_vessels = request.form['ca']
        thalassemia = request.form['thal']
        req_model = request.form['req_model']


        target = get_predictions(age, sex, chest_pain_type, resting_bp, cholesterol,fasting_bloodSugar,resting_ecg,max_heartrate,exercise_induced_angina,oldpeak, slope,num_vessels,thalassemia,req_model)

        if target==1:
            string_to_display = 'High Likely chance of getting heart disease'
        else:
            string_to_display = 'Very low Likely chance of getting heart disease'

        return render_template('home.html', target = target, string_to_display = string_to_display)
    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)