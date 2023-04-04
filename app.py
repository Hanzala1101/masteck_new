from flask import Flask, render_template, request, redirect, url_for, flash
from model import model_fun
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import speech_recognition as sr
import base64
import tempfile
from pydub import AudioSegment
import librosa
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



@app.route('/')
def index():
    return render_template('register.html')


@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    predict = model_fun()
    person_metadata = UserId.query.filter_by(id=predict)
    return render_template('home.html',person_metadata=person_metadata[0].name)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    audioData = base64.b64decode(data['audio'])
    # audio_array, sr = librosa.load(io.BytesIO(audioData), sr=41000)
    with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as audioFile:
        audioFile.write(audioData)
        audioFile.flush()
        audio = AudioSegment.from_file(audioFile.name, format='webm')
        wavAudio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        audio.export(wavAudio.name, format='wav')
        recognizer = sr.Recognizer()
        audio = sr.AudioFile(wavAudio.name)
        with audio as source:
            audioData = recognizer.record(source)
        text = recognizer.recognize_sphinx(audioData)
    # model_fun(audio_array)
    return text

if __name__ == "__main__":
    app.run(debug=True)