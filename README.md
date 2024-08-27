# Stella Chatbot

Stella Chatbot is your friendly, AI-powered companion, designed to assist in daily conversations and tasks. Built on a robust Django framework, Stella combines AIML, machine learning, web scraping, and Prolog to offer an intuitive and engaging chat experience. Whether you need a friend to chat with, information at your fingertips, or help with tasks, Stella is here to make your day easier and more enjoyable.

## 🌟 Key Features

### 🚪 **User Authentication:**
- **Sign-In:** Quick and secure login for registered users, with validations to ensure the correct email and password.
- **Sign-Up:** Seamlessly create a new account, complete with Neo4j integration for user nodes and robust validations for email and password matching.
- **Profile Picture:** Customize your profile with an uploaded image or choose a default based on gender.

### 🛡️ **Secure Access with Decorators:**
- Protects chat access by ensuring users are logged in. If authenticated, users are directed straight to the chat; otherwise, they're prompted to sign in.

### 💬 **Interactive Chat Screen:**
- A sleek chat interface allows users to converse with Stella while viewing their profile details, making the experience personal and engaging.

### 🧠 **AIML-Powered Conversations:**
- Leverages AIML (Artificial Intelligence Markup Language) for basic chat functionalities, powered by PyAIML21. AIML files are centrally stored and easily managed.

### 🎯 **Smart GET/SET Predicates:**
- Determines the best response source (AIML, Wikipedia, or Prolog knowledge base) based on user queries, making interactions more relevant.

### ✨ **Advanced Spell Checker:**
- Utilizes "Spello," a custom-trained spell checker, ensuring accurate responses tailored to Stella's specific knowledge base.

### 🌐 **Web Scraping with Wikipedia Integration:**
- Retrieves and stores rich information (like personal and organizational details) from Wikipedia, optimizing future interactions by saving data in Neo4j.

### 🔍 **Prolog Knowledge Base:**
- Implements a robust Prolog system using Pytholog, allowing Stella to infer new knowledge from user-provided facts and relationships. This knowledge is preserved in a pickle file and integrated into Neo4j.

### 🤖 **Machine Learning Models:**
- Employs cutting-edge models (Logistic Regression, Multinomial Naïve Bayes, SVM SVC, RNN, DNN) for predictive tasks like gender inference during Prolog relationship creation. These models ensure Stella evolves with each interaction, thanks to efficient learning and inference.

## 🚀 Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/pmchohan/stella.git
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - On Windows: `venv\Scripts\activate`
   - On Linux/macOS: `source venv/bin/activate`

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Neo4j:**
   - Set up your Neo4j database and adjust the connection settings in your Django configuration.

6. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Modify Paths for AIML and Spell Checker:**
   - To make the chatbot fully active, update the paths in the code where AIML files and spell training data are referenced. For example:

   ```python
   from pyaiml21 import Kernel
   from glob import glob
   from spello.model import SpellCorrectionModel
   from nltk.tokenize import sent_tokenize
   from nltk.corpus import wordnet
   from .scrapping import scrap
   from .prolog import check_predicates

   myBot = Kernel()
   corrector = SpellCorrectionModel(language="en")

   def initialization(username, u_id):
       u_id = str(u_id)
       global myBot
       myBot = Kernel()
       aimls = glob(r"C:\Users\YourUsername\YourProjectPath\chatbot\stella\chatbot\aiml_files\*")
       for aiml in aimls:
           print(aiml)
           myBot.learn(aiml)
       myBot.respond('remove what predicate', u_id)
       myBot.setPredicate('username', username, sessionID=u_id)
       myBot.respond('reset questions', u_id)
       myBot.respond('reset facts', u_id)
       spell_checker()

   def spell_checker():
       global corrector
       corrector = SpellCorrectionModel(language="en")
       with open(r'C:\Users\YourUsername\YourProjectPath\chatbot\stella\chatbot\spell_training_data.txt', 'r') as file:
           data = file.readlines()

       data = [i.strip() for i in data]
       corrector.train(data)
   ```

   - Replace `C:\Users\YourUsername\YourProjectPath` with the appropriate path on your machine.

8. **Launch the Development Server:**
   ```bash
   python manage.py runserver
   ```

## 🤝 Contributing

We welcome contributions! Whether you spot an issue or have a fantastic new feature idea, please submit an issue or create a pull request. Let's build Stella together!

---
