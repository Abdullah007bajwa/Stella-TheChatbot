from bs4 import BeautifulSoup
import requests, re
import spacy
from .my_neo4j import *
from .my_neo4j import get_from_neo

nlp = spacy.load('en_core_web_sm')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}

context = ''


def identify_word_category(word):
    doc = nlp(word)

    for entity in doc.ents:
        if entity.label_ == 'PERSON':
            return 'person'
        elif entity.label_ == 'ORG':
            return 'company'

    return 'other'


def remove_d(text):
    start, end = "", ""
    try:
        start = text.index('[')
    except ValueError:
        return text
    else:
        end = text.index(']')
        return remove_d(text[:start] + text[end + 1:])


def company_table(soup):
    try:
        header = soup.find('th', string='Headquarters')
        headquarters = header.find_next('td').get_text(strip=True)
        headquarters = remove_d(headquarters)
    except AttributeError:
        headquarters = "Don't Know about headquarters of " + context
    try:
        header = soup.find('th', string='Founded')
        Founded = header.find_next('td').get_text(strip=True)
        Founded == remove_d(Founded)
    except AttributeError:
        Founded = "Don't Know about founding date of " + context
    try:
        header = soup.find('th', string='Founder')
        Founder = header.find_next('td').get_text(strip=True)
        Founder = remove_d(Founder)
    except AttributeError:
        Founder = "Don't Know about founders of " + context
    try:
        header = soup.find('th', string='Founders')
        Founders = header.find_next('td').get_text(strip=True)
        Founders = remove_d(Founders)
    except AttributeError:
        Founders = "Don't Know about founders of " + context
    try:
        header = soup.find('th', string='Website')
        Website = header.find_next('td').get_text(strip=True)
        Website = remove_d(Website)
    except AttributeError:
        Website = "Don't Know about website of " + context

    founder = ''
    if Founder == "Don't Know about founders of " + context:
        founder = Founders
    else:
        founder = Founder

    return headquarters, Founded, founder, Website


def person_table(soup):
    try:
        header = soup.find('th', string='Born')
        Born = header.find_next('td').get_text(strip=True)
        born = re.findall("(\d+ [a-zA-Z]+ \d{4}|[a-zA-Z]+ \d+, \d{4})", Born)[0]
    except AttributeError:
        born = "Don't Know about birthdate of " + context

    try:
        header = soup.find('th', string='Died')
        Died = header.find_next('td').get_text(strip=True)
        Died = re.findall("(\d+ [a-zA-Z]+ \d{4} \(\D+ \d+\))", Died)[0]
    except AttributeError:
        Died = context + " is still alive"

    try:
        header = soup.find('th', string='Nationality')
        Nationality = header.find_next('td').get_text(strip=True)
    except AttributeError:
        try:
            pattern = "([a-zA-Z]+ \d\d, \d{4}\(age \d+\))(.+)"
            values = re.findall(pattern, Born)
            print(values)
            Nationality = values[0][1]
            print(Nationality)
        except IndexError:
            Nationality = 'No knowledge about nationality of ' + context

    try:
        header = soup.find('th', string='Spouse')
        Spouse = header.find_next('td').get_text(strip=True)
    except AttributeError:
        try:
            header = soup.find('th', string='Spouses')
            Spouse = header.find_next('td').get_text(strip=True)
        except AttributeError:
            Spouse = "no knowledge about marital status of " + context

    return born, Died, Nationality, Spouse


def scrap(word):
    type_of = identify_word_category(word)
    global context
    word = word.title()
    context = word
    result = get_from_neo(context)
    if len(result) > 0:
        final = result[0]['kb.definition']
        url = result[0]['kb.url']
        return final + '\nvisit <a href="' + url + '" target="_blank">WikiPedia</a> for more information'
    a = word.split()
    word = "_".join(a)

    url = 'https://en.wikipedia.org/wiki/' + word
    # print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup.prettify())
    # real work starts below

    para = soup.select('div.mw-parser-output')
    paras = []
    for element in para:
        paragraphs = element.find_all('p', class_=False)
        paras.extend(paragraphs)

    try:
        data = paras[0].text
    except IndexError:
        return None

    final = remove_d(data)
    if final == '\n':
        return None

    if type_of == 'company':
        headquarter, founded, founder, website = company_table(soup)
        upload_org_neo4j(url, final, headquarter, founded, founder, website, context)
    elif type_of == 'person':
        born_date, died_date, nationality, spouses = person_table(soup)
        upload_person_neo4j(url, final, born_date, died_date, nationality, spouses, context)
    else:
        upload_to_neo4j(url, final, context)

    return final+'\nvisit <a href="'+url+'" target="_blank">WikiPedia</a> for more information'
