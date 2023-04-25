from flask import Flask, render_template, request, redirect, url_for, flash
from model import model_fun
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import speech_recognition as spr
import base64
import tempfile
from pydub import AudioSegment
import librosa 
import io
from joblib import load
import numpy as np

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userId.db'
app.config['SECRET_KEY'] = 'userId'
db = SQLAlchemy(app)

app.app_context().push()

class UserId(db.Model, UserMixin):
    number = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    name = db.Column(db.String(100))

Prediction = 0

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
    model = load('model.joblib')
    # X_test=Prediction

    # X_test=np.array([[ 0.85275789, -0.37961011, -0.63409832, -0.33713756, -0.22513153,
    #     1.54746638,  1.00586545, -1.60632633,  0.39062666, -1.01592356,
    #     0.384919  , -1.75974197,  1.65954197, -0.7531705 , -0.07506431,
    #     1.55249769, -1.51177434,  0.75661294, -0.64443755,  0.54278893,
    #    -1.0614548 ,  0.26971105, -1.30321085,  0.12935729,  0.18081706]])
    X_test=np.array([[-0.72013587,  0.38045696,  1.54045918,  0.35124128, -0.27128323, -0.29233769,
    -0.5589013,   1.95605096, -0.54049407,  0.7983433,   1.3172201,   1.31148187,
    1.34208737,  0.00822181,  0.73655096,  1.0327014,   1.28354878, -0.17713967,
    1.02298488, -0.46944338,  0.52470179,  1.03536361,  1.602792,   -0.0228931,
    1.4161949 ]])

    # Use the loaded model for predictions
    predjob = np.argmax(model.predict(X_test), axis=-1)
    # Prediction = model_fun()
    print(predjob[0])
    person_metadata = UserId.query.filter_by(id=int(predjob[0]))
    print(person_metadata)
    return render_template('home.html',person_metadata=person_metadata[0].name)

@app.route('/convert', methods=['POST'])
def convert():
    global Prediction
    # print(Prediction)
    data = request.get_json()
    audioData = base64.b64decode(data['audio'])
    audio1 = AudioSegment.from_file(io.BytesIO(audioData))
    audio1.export('audio.wav', format='wav')
    # print(audioData)
    audio_array, sr = librosa.load(io.BytesIO(audioData), sr=44000)
    print(audio_array)
    Prediction = model_fun(audioData)
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