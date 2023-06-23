import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Step 1: Load the labeled dataset
data = pd.read_csv(r'C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\names_dataset.csv')

# Step 2: Preprocess the data
data['name'] = data['name'].str.lower()  # Convert names to lowercase
data['gender'] = data['gender'].map({'M': 0, 'F': 1})  # Map gender labels to 0 and 1

# Step 3: Feature extraction
vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 3))
features = vectorizer.fit_transform(data['name'])

# Step 4: Split the dataset
X_train, X_test, y_train, y_test = train_test_split(features, data['gender'], test_size=0.1, random_state=42)

# Step 5: Train the model
model_nb = MultinomialNB()
model_nb.fit(X_train.toarray(), y_train)

# Step 6: Evaluate the model
predictions_nb = model_nb.predict(X_test.toarray())
accuracy_nb = accuracy_score(y_test, predictions_nb)
print(f"Naive Bayes Accuracy: {accuracy_nb}")

# new names
def nb(name):
    name = [name.lower()]
    feature = vectorizer.transform(name)
    new_prediction = model_nb.predict(feature.toarray())
    return new_prediction[0]
