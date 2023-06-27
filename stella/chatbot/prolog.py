from pytholog import KnowledgeBase, Expr
from pyaiml21 import Kernel
from .my_ML import predict_gender
from .my_neo4j import create_fact, create_relation
import os, pickle

# instantiating
bot = Kernel()
uid = ''
knowledge_base = KnowledgeBase('KB')
knowledge = ['father(X, Y):- parent(X, Y), male(X)',
             'mother(X, Y):- parent(X, Y), female(X)',
             'kid(X, Y):- parent(Y, X)',
             'sibling(X, Y):- parent(Z, X), parent(Z, Y)',
             'brother(X, Y):- sibling(X, Y), male(X)',
             'sister(X, Y):- sibling(X, Y), female(X)',
             'husband(X, Y):- parent(X, Z), parent(Y, Z), male(X)',
             'wife(X, Y):- mother(X, Z), father(Y, Z)',
             'spouse(X, Y):- parent(X, Z), parent(Y, Z)',
             'nana(X, Y):- father(X, Z), mother(Z, Y)',
             'nani(X, Y):- mother(X, Z), mother(Z, Y)',
             'dada(X, Y):- father(X, Z), father(Z, Y)',
             'dadi(X, Y):- mother(X, Z), father(Z, Y)',
             'son(X, Y):- male(X), parent(Y, X)',
             'daughter(X, Y):- female(X), parent(Y, X)',
             'taya(X, Y):- brother(X, Z), father(Z, Y)',
             'chachu(X, Y):- taya(X, Y)',
             'phupho(X, Y):- sister(X, Z), father(Z, Y)',
             'khala(X, Y):- sister(X, Z), mother(Z, Y)',
             'mamoo(X, Y):- brother(X, Z), mother(Z, Y)',
             'saas(X, Y):- mother(X, Z), husband(Z, Y)',
             'susar(X, Y):- father(X, Z), husband(Z, Y)',
             'bhabhi(X, Y):- wife(X, Z), brother(Z, Y)',
             'nand(X, Y):- bhabhi(Y, X)',
             'uncle(X, Y):- taya(X, Y); mamoo(X, Y)',
             'aunty(X, Y):- khala(X, Y); phupho(X, Y)',
             'pota(X, Y):- dada(Y, X); dadi(Y, X), male(X)',
             'poti(X, Y):- dada(Y, X); dadi(Y, X), female(X)',
             'nawasa(X, Y):- nana(Y, X); nani(Y, X), male(X)',
             'nawasi(X, Y):- nana(Y, X); nani(Y, X), female(X)',
             'bhanja(X, Y):- male(X), mamoo(Y, X); khala(Y, X)',
             'bhanji(X, Y):- female(X), mamoo(Y, X); khala(Y, X)',
             'bhateeja(X, Y):- male(X), taya(Y, X); phupho(Y, X)',
             'bhateeji(X, Y):- female(X), taya(Y, X); phupho(Y, X)',
             'cousin(X, Y):- kid(X, Z), sibling(Z, A), parent(A, Y)',
             'person(X):- male(X)',
             'person(X):- female(X)']

path = r'C:\Users\abdul\PycharmProjects\chatbot\chatbot\stella\chatbot\knowledge.pkl'
if os.path.exists(path):
    print('knowledge base found, learning')
    with open(path, 'rb') as file:
        knowledge = pickle.load(file)
else:
    print('knowledge base not found, writing rules')
    with open(path, 'wb') as file:
        pickle.dump(knowledge, file)

knowledge_base(knowledge)


def set_fact(fact, value, value2=None):
    fact = fact.lower()
    v1 = value.lower().replace(' ', '_')
    if value2:
        v2 = value2.lower().replace(' ', '_')
        # checking if person2 exists in knowledge base
        result = knowledge_base.query(Expr(f'person({v2})'))
        print('result of check on value2:', result)
        if result[0] == 'No':
            gender = predict_gender(value2)
            new_fact = gender + '(' + v2 + ')'
            if new_fact not in knowledge:
                create_fact(v2, gender, uid)
                knowledge.insert(0, new_fact)
        # checking if person1 exists in knowledge base
        result = knowledge_base.query(Expr(f'person({v1})'))
        print('result of check on value:', result)
        if result[0] == 'No':
            gender = predict_gender(value)
            new_fact = gender + '(' + v1 + ')'
            if new_fact not in knowledge:
                create_fact(v1, gender, uid)
                knowledge.insert(0, new_fact)
        new_fact = fact + '(' + v1 + ',' + v2 + ')'
        if new_fact not in knowledge:
            create_relation(v1, fact, v2, uid)
            knowledge.insert(0, new_fact)
    else:
        new_fact = fact + '(' + v1 + ')'
        if new_fact not in knowledge:
            create_fact(v1, fact, uid)
            knowledge.insert(0, new_fact)
    # updating knowledge pickle file
    with open(path, 'wb') as file:
        pickle.dump(knowledge, file)
    knowledge_base(knowledge)
    print(knowledge[:10])
    bot.respond('reset facts', uid)


def query_kb(relation, value):
    relation = relation.lower().strip()
    bot.respond('reset questions', uid)
    query = relation + '(X,' + value.lower().strip().replace(' ', '_') + ')'
    print(query)
    result = knowledge_base.query(Expr(query))
    print('result of query:', result, type(result))
    if isinstance(result[0], str):
        print('result of query is str:', result[0])
        return None
    else:
        response = []
        for value in result:
            response.append(value['X'].title().replace('_', ' '))
        response = list(set(response))
        response = ", ".join(response)
        return response


# function to check predicates
def check_predicates(mybot, user_id):
    global bot, uid
    bot = mybot
    uid = user_id
    male = bot.getPredicate('male', uid)
    female = bot.getPredicate('female', uid)
    parent = bot.getPredicate('parent', uid)
    relation = bot.getPredicate('relation', uid)
    child = bot.getPredicate('child', uid)
    who_is = bot.getPredicate('who_is', uid)
    who_is_of = bot.getPredicate('who_is_of', uid)

    result = None

    if male != 'unknown':
        set_fact('male', male)
    elif female != 'unknown':
        set_fact('female', female)
    elif relation != 'unknown':
        set_fact(relation, parent, child)
    elif who_is != 'unknown':
        result = query_kb(who_is, who_is_of)
        if result:
            result = who_is.lower() + ' of ' + who_is_of + ' is/are ' + result

    return result
