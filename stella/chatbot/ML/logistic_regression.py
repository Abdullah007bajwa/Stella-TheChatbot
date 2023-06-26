import os, pickle, pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


def learn_lr():
    # Step 1: Load the labeled dataset
    data = pd.read_csv(r'C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\ML\names_dataset.csv')

    # Step 2: Preprocess the data
    data['name'] = data['name'].str.lower()  # Convert names to lowercase
    data['gender'] = data['gender'].map({'M': 0, 'F': 1})  # Map gender labels to 0 and 1

    # Step 3: Feature extraction
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 3))
    features = vectorizer.fit_transform(data['name'])

    # Step 5: Train the model
    model = LogisticRegression()
    model.fit(features, data['gender'])

    # save the model
    with open('trained_models/lr.pkl', 'wb') as file:
        pickle.dump((model, vectorizer), file)


# Step 7: Predict gender for new names
def lr(name):
    path = r"C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\ML\trained_models\lr.pkl"
    if os.path.exists(path):
        print('trained lr available')
    else:
        print('learning lr')
        learn_lr()
    with open(path, 'rb') as file:
        model, vectorizer = pickle.load(file)
    name = [name.lower()]
    feature = vectorizer.transform(name)
    new_prediction = model.predict(feature)
    return new_prediction[0]

# learn_lr()
# print(lr('ali'))
# print(lr('ayesha'))
