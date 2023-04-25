from flask import Flask, render_template, request, redirect, url_for, flash
# from model import model_fun
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import speech_recognition as spr
import base64
import tempfile
from pydub import AudioSegment
# import librosa 
import io

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userId.db'
app.config['SECRET_KEY'] = 'userId'
db = SQLAlchemy(app)

app.app_context().push()

class UserId(db.Model, UserMixin):
    number = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    name = db.Column(db.String(100))

# Prediction = 0

@app.route('/',methods=['POST','GET'])
def index():
    if request.method =='POST':
        return redirect('/login')
    else:
        return render_template('register.html')


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        return redirect('/home')
    else:
        return render_template('login.html')


@app.route('/home',methods=['POST','GET'])
def home():
    # Prediction = model_fun()
    person_metadata = UserId.query.filter_by(id=0)
    return render_template('home.html',person_metadata=person_metadata[0].name)

@app.route('/convert', methods=['POST'])
def convert():
    # global Prediction
    # print(Prediction)
    data = request.get_json()
    audioData = base64.b64decode(data['audio'])
    audio1 = AudioSegment.from_file(io.BytesIO(audioData))
    audio1.export('audio.wav', format='wav')
    # print(audioData)
    # audio_array, sr = librosa.load(io.BytesIO(audioData), sr=44000)
    # print(audio_array)
    # Prediction = model_fun(audioData)
    with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as audioFile:
        audioFile.write(audioData)
        audioFile.flush()
        audio = AudioSegment.from_file(audioFile.name, format='webm')
        wavAudio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        audio.export(wavAudio.name, format='wav')
        recognizer = spr.Recognizer()
        audio = spr.AudioFile(wavAudio.name)
        with audio as source:
            audioData = recognizer.record(source)
        text = recognizer.recognize_sphinx(audioData)
    
    
    return text

if __name__ == "__main__":
    app.run(debug=True)