import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Step 1: Load the labeled dataset
data = pd.read_csv(r'C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\names_dataset.csv')

# Step 2: Preprocess the data
data['name'] = data['name'].str.lower()  # Convert names to lowercase
data['gender'] = data['gender'].map({'M': 0, 'F': 1})  # Map gender labels to 0 and 1

# Step 3: Feature extraction - convert characters to numerical representation (indexes)
tokenizer = tf.keras.preprocessing.text.Tokenizer(char_level=True)
tokenizer.fit_on_texts(data['name'])
sequences = tokenizer.texts_to_sequences(data['name'])

# Step 4: Split the dataset
X_train, X_test, y_train, y_test = train_test_split(sequences, data['gender'], test_size=0.1, random_state=42)

# Step 5: Train the model
max_sequence_length = max(len(seq) for seq in sequences)
input_dim = len(tokenizer.word_index) + 1

X_train_rnn = tf.keras.preprocessing.sequence.pad_sequences(X_train, maxlen=max_sequence_length)
X_test_rnn = tf.keras.preprocessing.sequence.pad_sequences(X_test, maxlen=max_sequence_length)

model_rnn = Sequential()
model_rnn.add(Embedding(input_dim, 64, input_length=max_sequence_length))
model_rnn.add(LSTM(64))
model_rnn.add(Dense(1, activation='sigmoid'))

model_rnn.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model_rnn.fit(X_train_rnn, y_train, epochs=10, batch_size=32, validation_data=(X_test_rnn, y_test))

# Step 6: Evaluate the model
_, accuracy_rnn = model_rnn.evaluate(X_test_rnn, y_test)
print(f"RNN Accuracy: {accuracy_rnn}")

# Step 7: Predict gender for new names
def rnn(name):
    name = [name.lower()]
    new_sequence = tokenizer.texts_to_sequences(name)
    new_sequence_padded = tf.keras.preprocessing.sequence.pad_sequences(new_sequence, maxlen=max_sequence_length)
    new_prediction = model_rnn.predict(new_sequence_padded)
    new_prediction = [1 if pred >= 0.5 else 0 for pred in new_prediction]
    return new_prediction[0]
