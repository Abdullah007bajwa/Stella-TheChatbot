# Stella Chatbot

Stella Chatbot is your friendly, AI-powered companion, designed to assist in daily conversations and tasks. Built on a robust Django framework, Stella combines AIML, machine learning, web scraping, and Prolog to offer an intuitive and engaging chat experience. Whether you need a friend to chat with, information at your fingertips, or help with tasks, Stella is here to make your day easier and more enjoyable.

## 🌟 Key Features

### 🚪 **User Authentication:**
- **Sign-In:** Experience quick and secure login for registered users, with robust validations ensuring the correct email and password.
- **Sign-Up:** Seamlessly create a new account, complete with Neo4j integration for user nodes and strong validations for email and password matching.
- **Profile Picture:** Personalize your profile with an uploaded image or a default avatar based on gender.

### 🛡️ **Secure Access with Decorators:**
- Protects chat access by ensuring users are logged in. If authenticated, users are directed straight to Stella’s chat; otherwise, they're prompted to sign in.

### 💬 **Interactive Chat Screen:**
- A sleek chat interface that allows users to converse with Stella while viewing their profile details, making interactions personal and engaging.

### 🧠 **AIML-Powered Conversations:**
- Stella is powered by AIML (Artificial Intelligence Markup Language) for natural and responsive chat functionalities, driven by PyAIML21.

### 🎯 **Smart GET/SET Predicates:**
- Stella intelligently selects the best response source (AIML, Wikipedia, or Prolog knowledge base) based on user queries, ensuring relevant and informative conversations.

### ✨ **Advanced Spell Checker:**
- Stella features "Spello," a custom-trained spell checker, ensuring accurate responses tailored to her specific knowledge base.

### 🌐 **Web Scraping with Wikipedia Integration:**
- Retrieves and stores rich information from Wikipedia, enhancing future interactions by saving data in Neo4j.

### 🔍 **Prolog Knowledge Base:**
- Stella utilizes a robust Prolog system via Pytholog, allowing her to infer new knowledge from user-provided facts and relationships, with data stored securely in Neo4j.

### 🤖 **Machine Learning Models:**
- Stella evolves with each interaction, employing advanced models (Logistic Regression, Multinomial Naïve Bayes, SVM SVC, RNN, DNN) for predictive tasks like gender inference during Prolog relationship creation.

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
   - Ensure paths for AIML files and spell training data are correctly set up for full chatbot functionality.

8. **Launch the Development Server:**
   ```bash
   python manage.py runserver
   ```

## 🤝 Contributing

Join the development of Stella! Whether you spot an issue or have a new feature idea, we welcome your contributions through issues or pull requests. Let’s enhance Stella together!

---