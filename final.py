from flask import Flask, render_template, request
import smtplib
import speech_recognition as sr
import pyttsx3
import pandas as pd

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)
            print("Unable to Recognize your voice.")
            return "None"
    return query

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    recipient_name = request.form['recipient_name']
    recipient_email = request.form['recipient_email']
    subject = request.form['subject']
    body = request.form['body']

    # Save the name and email to an Excel file
    data = {'Name': [recipient_name], 'Email': [recipient_email]}
    df = pd.DataFrame(data)
    df.to_excel('receivers.xlsx', index=False, engine='openpyxl')

    sender_email = "sp@gmail.com"
    sender_password = "xxxx  xxxx xxxx"

    message = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, message)
    server.quit()

    return 'Email sent!'

if __name__ == '__main__':
    app.run(debug=True)
