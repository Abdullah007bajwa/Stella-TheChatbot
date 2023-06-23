import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

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
model = LogisticRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

# Step 7: Predict gender for new names
def lr(name):
    name = [name.lower()]
    feature = vectorizer.transform(name)
    new_prediction = model.predict(feature)
    return new_prediction[0]

