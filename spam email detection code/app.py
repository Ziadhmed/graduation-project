import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import re
import nltk
from nltk.corpus import stopwords
from model import cv
import requests

#create flask app
app = Flask(__name__, template_folder='template')
#load the pickle model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def index():
    return render_template('mail.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        mail = request.form.get('freeform')
        if (predict_mail(mail) == 1):
            result = "This message is classified as phishing message.X"
        else:
            result = "This message is classified as legitimate message.√"

    return render_template("mail.html", prediction_text=result)

@app.route("/emails", methods=['GET'])
def get_emails():
    response = requests.get('http://localhost:5000/emails')  # Assuming Flask is running on localhost:5000
    email_data = response.json() #json() for getting json content
    return jsonify(email_data) #converts output to a JSON response object

def predict_mail(mail):
    stopwords = nltk.corpus.stopwords.words('english')
    mail = re.sub(r"http\S+", "", mail)
    mail = re.sub("[^a-zA-Z0-9]", " ", mail)
    mail = mail.lower()
    mail = nltk.word_tokenize(mail)
    mail = [word for word in mail if word not in stopwords]
    mail = " ".join(mail)
    vector = cv.transform([mail])
    prediction = model.predict(vector.toarray())
    return prediction[0]

if __name__ == "__main__":
    app.run(debug=True,port=5001)
