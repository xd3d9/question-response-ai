import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

model = load_model('ams.h5')

with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('label_encoder.pkl', 'rb') as handle:
    label_encoder = pickle.load(handle)

max_len = model.input_shape[1]

def pas(user_input):
    seq = tokenizer.texts_to_sequences([user_input])
    padded_seq = pad_sequences(seq, maxlen=max_len, padding='post')
    predictions = model.predict(padded_seq)
    confidence = np.max(predictions) 
    response_index = np.argmax(predictions)
    response = label_encoder.inverse_transform([response_index])[0]
    return response, confidence

while True:
   user_input = input ("Shen: ")
   response, confidence = pas(user_input)
   print(f"Pasuxi: {response}, Tvitdajereba: {confidence * 100:.2f}%")