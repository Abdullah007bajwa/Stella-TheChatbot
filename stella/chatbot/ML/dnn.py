import pickle, os, pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout


def learn_dnn():
    # Step 1: Load the labeled dataset
    data = pd.read_csv(r'C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\ML\names_dataset.csv')

    # Step 2: Preprocess the data
    data['name'] = data['name'].str.lower()  # Convert names to lowercase
    data['gender'] = data['gender'].map({'M': 0, 'F': 1})  # Map gender labels to 0 and 1

    # Step 3: Feature extraction
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 3))
    features = vectorizer.fit_transform(data['name'])

    # Step 4: Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(features, data['gender'], test_size=0.1, random_state=42)

    # Step 5: Build the DNN model
    model_dnn = Sequential()
    model_dnn.add(Dense(128, activation='relu', input_dim=X_train.shape[1]))
    model_dnn.add(Dropout(0.5))
    model_dnn.add(Dense(64, activation='relu'))
    model_dnn.add(Dropout(0.5))
    model_dnn.add(Dense(1, activation='sigmoid'))

    model_dnn.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Step 6: Train the model
    model_dnn.fit(X_train.toarray(), y_train, epochs=10, batch_size=32)

    # Step 7: Evaluate the model
    predictions_dnn = model_dnn.predict(X_test.toarray())
    predictions_dnn = [1 if pred >= 0.5 else 0 for pred in predictions_dnn]
    accuracy_dnn = accuracy_score(y_test, predictions_dnn)
    print(f"DNN Accuracy: {accuracy_dnn}")
    #save the model
    with open('trained_models/dnn.pkl', 'wb') as file:
        pickle.dump((model_dnn, vectorizer), file)


# Step 8: Predict gender for new names
def dnn(name):
    path = r"C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\ML\trained_models\dnn.pkl"
    if os.path.exists(path):
        print('trained dnn available')
    else:
        print('learning dnn')
        learn_dnn()
    with open(path, 'rb') as file:
        model_dnn, vectorizer = pickle.load(file)
    name = [name.lower()]
    feature = vectorizer.transform(name)
    new_prediction = model_dnn.predict(feature.toarray())
    new_prediction = [1 if pred >= 0.5 else 0 for pred in new_prediction]
    return new_prediction[0]

# learn_dnn()
# print(dnn('ayesha'))
# print(dnn('ahmer'))
