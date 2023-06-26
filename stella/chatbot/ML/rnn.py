import pickle, os, pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense


def learn_rnn():
    # Step 1: Load the labeled dataset
    data = pd.read_csv(r'C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\ML\names_dataset.csv')

    # Step 2: Preprocess the data
    data['name'] = data['name'].str.lower()  # Convert names to lowercase
    data['gender'] = data['gender'].map({'M': 0, 'F': 1})  # Map gender labels to 0 and 1

    # Step 3: Feature extraction - convert characters to numerical representation (indexes)
    tokenizer = tf.keras.preprocessing.text.Tokenizer(char_level=True)
    tokenizer.fit_on_texts(data['name'])
    sequences = tokenizer.texts_to_sequences(data['name'])

    # Step 5: Train the model
    max_sequence_length = max(len(seq) for seq in sequences)
    input_dim = len(tokenizer.word_index) + 1

    X_train_rnn = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_sequence_length)

    model_rnn = Sequential()
    model_rnn.add(Embedding(input_dim, 64, input_length=max_sequence_length))
    model_rnn.add(LSTM(64))
    model_rnn.add(Dense(1, activation='sigmoid'))

    model_rnn.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model_rnn.fit(X_train_rnn, data['gender'], epochs=10, batch_size=32)

    # save the model
    with open('trained_models/rnn.pkl', 'wb') as file:
        pickle.dump((model_rnn, tokenizer, max_sequence_length), file)


# Step 7: Predict gender for new names
def rnn(name):
    name = name.lower()
    path = r"C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\ML\trained_models\rnn.pkl"
    if os.path.exists(path):
        print('trained rnn available')
    else:
        print('learning rnn')
        learn_rnn()
    with open(path, 'rb') as file:
        model_rnn, tokenizer, max_sequence_length = pickle.load(file)
    new_sequence = tokenizer.texts_to_sequences(name)
    new_sequence_padded = tf.keras.preprocessing.sequence.pad_sequences(new_sequence, maxlen=max_sequence_length)
    new_prediction = model_rnn.predict(new_sequence_padded)
    new_prediction = [1 if pred >= 0.5 else 0 for pred in new_prediction]
    return new_prediction[0]

# learn_rnn()
# print(rnn('Imran'))
# print(rnn('Ayesha'))
