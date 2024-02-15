Assalam-u-alaikum
Its Abdullah Faisal student of BS (AI) in UMT, Lahore.
Its my first time uploading a project to github
# Stella Chatbot

Stella Chatbot is a Django-based chatbot project that utilizes AIML, machine learning, web scraping, and Prolog to provide interactive conversations and knowledge retrieval. The chatbot is designed to communicate with users, answer questions, and perform various tasks based on the provided functionality.

## File Structure
`
chatbot
├── chatbot (Django's default)
└── stella (custom app)
    ├── chatbot (bot functionality)
    │   ├── aiml_files (AIML files)
    │   ├── ML (machine learning models)
    │   ├── bot.py (main bot file)
    │   ├── knowledge.pkl (Prolog knowledge)
    │   ├── my_neo4j.py (Neo4j interaction)
    │   ├── prolog.py (Prolog implementation)
    │   ├── scraping.py (Wikipedia web scraping)
    │   └── spell_training_data.txt (spell training data)
    ├── migrations (Django migrations)
    ├── static
    │   ├── css (web page styles)
    │   ├── js (web page scripts)
    │   ├── pics (images used in the project)
    │   └── profile_pics (user profile pictures)
    ├── templates (HTML templates)
    ├── decorators.py (Django decorators)
    ├── models.py (Django models)
    ├── urls.py (URL configurations)
    ├── views.py (Django views)
    └── manage.py (Django management script)
venv (virtual environment)
`
## Features

### Sign-In
- Users can sign in if they are already registered.
- Validations are performed to check if the email is registered and if the password is correct.
- Successful sign-in stores the user's ID, name, and email in the Django session.

### Sign-Up
- Users can sign up to create a new account.
- Neo4j database is used to create a new node for the user using Django-Neomodel.
- Validations are performed to check if the email is already registered and if the password matches the confirm password field.

### Profile Picture
- During sign-up, users are prompted to upload a profile picture.
- If the user chooses to skip uploading, a default picture based on their gender is set.
- Profile pictures are saved in the [stella/static/profile_pics](stella/static/profile_pics) directory.

### Decorators
- Django decorators are used to restrict users from accessing the chatbot without logging in through the URL.
- Sessions are checked, and if a session is set, the user is redirected to the chat screen without requiring login credentials.
- If the user is not logged in, they will be redirected to the sign-in screen.

### Chat Screen
- After logging in or signing up, users can chat with Stella.
- The chat screen consists of a chatbox div on the left and user information on the right.

### AIML
- AIML (Artificial Intelligence Markup Language) is used for basic chat functionality.
- PyAIML21 is the Python module used for implementing AIML.
- AIML files are stored in the [stella/chatbot/aiml_files](stella/chatbot/aiml_files) directory.

### GET/SET Predicate
- AIML get/set predicates are used to determine when to respond with AIML, Wikipedia, or Prolog knowledge base.

### Spell Checker
- A customized spell checker called Spello is used instead of traditional spell checkers like TextBlob.
- Spello is trained on the type of texts expected to be received based on the AIML files.

### Web Scraping
- Wikipedia is scraped using Beautiful Soup for retrieving basic information.
- Additional information such as birth date, death date, nationality, and spouse(s) are retrieved for people.
- For organizations, headquarters location, founding date, founder, and website information are also retrieved.
- Scraped data is stored in Neo4j for efficient retrieval.
- Neo4j is queried for subsequent requests instead of re-scraping.

### Prolog
- Prolog is implemented using the Pytholog library.
- A list of rules for relationships is included.
- Additional facts provided by the user are used for inference.
- The knowledge list is updated and saved in a pickle file.
- Relationships and facts are also stored in Neo4j.

### Machine Learning
- Machine learning models are used to predict gender during Prolog relationship creation.
- Five models (Logistic Regression, Multinomial Naïve Bayes, SVM SVC, Recurrent Neural Network, and Deep Neural Network) are implemented using TensorFlow and scikit-learn.
- Models, vectorizers, and tokenizers are saved in pickle files for efficient learning and inference.

## Usage

1. Clone the repository:
```git clone https://github.com/pmchohan/stella.git```

2. Set up a virtual environment:
```python -m venv venv```

3. Activate the virtual environment:
- On Windows: `venv\Scripts\activate`
- On Linux/macOS: `source venv/bin/activate`
4. Install the dependencies:
```pip install -r requirements.txt```

5. Set up the Neo4j database and configure the connection in the Django settings.
   
6. Run migrations:
```python manage.py migrate```

7. Start the Django development server:
```python manage.py runserver```

## Contributing
Contributions are welcome! If you find any issues or want to add new features, please submit an issue or create a pull request.

## Credits
I've surely taken a lot of help from internet
Special thanks to [@m-hussain](https://github.com/m-hussain) for guiding throughout the project
ChatGPT is also a great tool for beginners like me to get things done
Watched Code With Harry on YouTube for Django basics
