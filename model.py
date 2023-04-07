import numpy as np
from joblib import load
import librosa
# import pickle
# import tensorflow as tf
# import onnxruntime as rt

def model_fun(audio_array):
    y, sr = librosa.load(audio_array, mono=True, duration=30)
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
        X_test = X_test.append(np.mean(e))



    # # Load the saved model joblib
    model = load('model.joblib')

    # Load the saved model pickle
    # with open('model.pkl', 'rb') as f:
    #     model = pickle.load(f)

    # Load the saved model tensorflow
    # model = tf.keras.models.load_model('saved_model')

    # Load the saved model onnx
    # sess = rt.InferenceSession("model.onnx")

    # Prepare the input data
    # input_data = np.array(X_test)


    # X_test=np.array([ 0.85275789, -0.37961011, -0.63409832, -0.33713756, -0.22513153,
    #     1.54746638,  1.00586545, -1.60632633,  0.39062666, -1.01592356,
    #     0.384919  , -1.75974197,  1.65954197, -0.7531705 , -0.07506431,
    #     1.55249769, -1.51177434,  0.75661294, -0.64443755,  0.54278893,
    #    -1.0614548 ,  0.26971105, -1.30321085,  0.12935729,  0.18081706])


    # Use the loaded model for predictions
    predjob = np.argmax(model.predict(X_test), axis=-1)
    # predpkl = np.argmax(model.predict(X_test), axis=-1)
    # predtensor = np.argmax(model.predict(X_test), axis=-1)
    # Run the model to get predictions onnx
    # predonnx = sess.run(None, {"input": X_test})[0]

    return predjob[0] #, perdonnx[0], predpkl[0], predtensor[0]
