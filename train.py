import json
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

with open('resp.json',encoding="utf8") as f:
    data = json.load(f)
messages = [item['msg'] for item in data]
responses = [item['resp'] for item in data]

tokenizer = Tokenizer()
tokenizer.fit_on_texts(messages)
sequences = tokenizer.texts_to_sequences(messages)

max_len = max(len(seq) for seq in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

label_encoder = LabelEncoder()
encoded_responses = label_encoder.fit_transform(responses)
num_classes = len(label_encoder.classes_)
one_hot_responses = tf.keras.utils.to_categorical(encoded_responses, num_classes=num_classes)


model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=100, input_length=max_len),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy',tf.keras.metrics.BinaryAccuracy(),tf.keras.metrics.FalseNegatives()])
model.summary()
model.fit(padded_sequences, one_hot_responses, epochs=500, batch_size=32, validation_split=0.2)

model.save('ams.h5')

import pickle
with open('tokenizer.pkl', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('label_encoder.pkl', 'wb') as handle:
    pickle.dump(label_encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)