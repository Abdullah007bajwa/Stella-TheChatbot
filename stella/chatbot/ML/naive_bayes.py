import os, pickle, pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def learn_nb():
    # Step 1: Load the labeled dataset
    data = pd.read_csv(r'C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\ML\names_dataset.csv')

    # Step 2: Preprocess the data
    data['name'] = data['name'].str.lower()  # Convert names to lowercase
    data['gender'] = data['gender'].map({'M': 0, 'F': 1})  # Map gender labels to 0 and 1

    # Step 3: Feature extraction
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 3))
    features = vectorizer.fit_transform(data['name'])

    # Step 5: Train the model
    model_nb = MultinomialNB()
    model_nb.fit(features.toarray(), data['gender'])

    # save the model
    with open('trained_models/nb.pkl', 'wb') as file:
        pickle.dump((model_nb, vectorizer), file)


# new names
def nb(name):
    path = r"C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\ML\trained_models\nb.pkl"
    if os.path.exists(path):
        print('trained nb available')
    else:
        print('learning nb')
        learn_nb()
    with open(path, 'rb') as file:
        model_nb, vectorizer = pickle.load(file)
    name = [name.lower()]
    feature = vectorizer.transform(name)
    new_prediction = model_nb.predict(feature.toarray())
    return new_prediction[0]

# learn_nb()
# print(nb('ali'))
# print(nb('ayesha'))
