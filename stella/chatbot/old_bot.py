myBot = Bot()
corrector = SpellCorrectionModel(language="en")


def initialization():
    global myBot
    myBot = Bot()
    base_path = os.path.dirname(os.path.abspath(__file__))
    aiml_dir = os.path.join(base_path, "aiml_files")
    aimls = glob(os.path.join(aiml_dir, "*.aiml"))
    for aiml in aimls:
        myBot.learn_aiml(aiml)

    global corrector
    corrector = SpellCorrectionModel(language="en")
    with open('spell_training_data.txt', 'r') as file:
        data = file.readlines()

    data = [i.strip() for i in data]
    corrector.train(data)
    # corrector.save(model_save_dir)      #it will create a 'model.pkl'
    # corrector.load(model_path)          # it will load that model


def reply(prompts, user):
    responses = ''
    for prompt in sent_tokenize(prompts):
        response = myBot.respond(prompt, user)
        if response == 'unknown':
            response = correct(prompt, user)
        responses += response + '. '
    return responses[:-2]


def correct(prompt, user):
    corrected = corrector.spell_correct(prompt)
    result = myBot.respond(str(corrected), user)
    if result == 'unknown':
        result = identify_statement(str(corrected), user)
    return result


def identify_statement(prompt, user):
    if prompt.startswith('what is'):
        pass
    return prompt


# initialization()
# print(reply('Hi', 'user'))
