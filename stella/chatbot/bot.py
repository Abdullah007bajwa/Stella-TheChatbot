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
    # bot initialization
    global myBot
    myBot = Kernel()
    aimls = glob(r"C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\aiml_files\*")
    for aiml in aimls:
        print(aiml)
        myBot.learn(aiml)
    # resetting predicates
    myBot.respond('remove what predicate', u_id)
    myBot.setPredicate('username', username, sessionID=u_id)
    myBot.respond('reset questions', u_id)
    myBot.respond('reset facts', u_id)
    spell_checker()


def spell_checker():
    # spell checker/corrector initialization
    global corrector
    corrector = SpellCorrectionModel(language="en")
    with open(r'C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\spell_training_data.txt', 'r') as file:
        data = file.readlines()

    data = [i.strip() for i in data]
    corrector.train(data)


def reply(prompts, u_id):
    u_id = str(u_id)
    global myBot, corrector
    responses = ''
    for prompt in sent_tokenize(prompts):
        print('user entered:', prompt)
        response = myBot.respond(prompt, u_id)
        if response.lower() == 'unknown':
            prompt1 = corrector.spell_correct(prompt)
            response = myBot.respond(prompt1['spell_corrected_text'], u_id)
            print('user prompt corrected:', prompt1['spell_corrected_text'])
        result = check_predicates(myBot, u_id)
        if result:
            print('entered prolog')
            response = result
        asked_about = myBot.get_predicate('what', u_id)
        if asked_about != 'unknown':
            response = what_is(asked_about)
            myBot.respond('remove what predicate', u_id)
        asked_about_person = myBot.get_predicate('who', u_id)
        if asked_about_person != 'unknown':
            response = what_is(asked_about_person, 'person')
            myBot.respond('remove who predicate', u_id)
        responses += response + '. '
        print('response:', responses)
    return responses[:-2]


def what_is(word, type=None):
    response = scrap(word, type)
    if response:
        return response

    data = wordnet.synsets(word)
    if len(data) == 0:
        response = 'cannot say anything'
    else:
        response = word.title() + ' is a/an ' + data[0].definition()
        if len(data[0].examples()) != 0:
            response += '\nExample is: ' + data[0].example()[0]

    return response
