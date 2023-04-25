import numpy as np
import librosa

def model_fun():
    y, sr = librosa.load('audio.wav', mono=True, duration=30)
    # remove leading and trailing silence
    y, index = librosa.effects.trim(y)
    rmse = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    X_test = [np.mean(rmse), np.mean(spec_cent) ,np.mean(spec_bw), np.mean(rolloff), np.mean(zcr)]
    for e in mfcc:
        X_test.append(np.mean(e))
    # pd.read_a(X_test)
    X_test = np.array([X_test])
    print(X_test)
    return X_test

# def Predict(X_text):
#     # # Load the saved model joblib
#     model = load('model.joblib')


#     X_test=np.array([[ 0.85275789, -0.37961011, -0.63409832, -0.33713756, -0.22513153,
#         1.54746638,  1.00586545, -1.60632633,  0.39062666, -1.01592356,
#         0.384919  , -1.75974197,  1.65954197, -0.7531705 , -0.07506431,
#         1.55249769, -1.51177434,  0.75661294, -0.64443755,  0.54278893,
#        -1.0614548 ,  0.26971105, -1.30321085,  0.12935729,  0.18081706]])


#     # Use the loaded model for predictions
#     predjob = np.argmax(model.predict(X_test), axis=-1)
    
#     print(predjob[0])
#     return predjob[0]
