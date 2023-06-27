from py2neo import Graph

graph = Graph('bolt://localhost:7687', auth=("neo4j", 'password'))


def upload_org_neo4j(url, definition, headquarter, founded, founder, website, context):
    query = """Merge (:KnowledgeBase {title:$context, definition:$defi, url:$url, headquarter:$hq, 
    founded_on:$founded, founder:$founder, website:$web})"""
    graph.run(query, context=context, defi=definition, url=url, hq=headquarter, founded=founded, founder=founder,
              web=website)


def upload_person_neo4j(url, definition, born_date, died_date, nationality, spouses, context):
    query = """Merge (:KnowledgeBase {title:$context, definition:$defi, url:$url, born_on:$dob, died_on:$died, 
    nationality:$nationality, spouse:$spouse})"""
    graph.run(query, context=context, defi=definition, url=url, dob=born_date, died=died_date, nationality=nationality,
              spouse=spouses)


def upload_to_neo4j(url, definition, context):
    query = """Merge (:KnowledgeBase {title:$context, definition:$defi, url:$url})"""
    graph.run(query, context=context, defi=definition, url=url)


def get_from_neo(context):
    query = """Match (kb:KnowledgeBase {title:$context}) return kb.definition, kb.url"""
    result = graph.run(query, context=context).data()
    return result


def create_fact(person, gender, uid):
    query = """
    MATCH (n:BotUsers) where id(n)=$uid
    MERGE (n)-[:Knows]->(:Person {name:$name, gender:$gender});
    """
    graph.run(query, name=person, gender=gender, uid=int(uid))


def create_relation(person1, relation, person2, uid):
    query = """
    MATCH (n:BotUsers) where id(n)={uid}
    MATCH (p1:Person {{name:"{name1}"}})<-[:Knows]-(n)-[:Knows]->(p2:Person {{name:"{name2}"}})
    MERGE (p1)-[r:{relation}]->(p2);
    """
    graph.run(query.format(uid=uid, name1=person1, name2=person2, relation=relation.lower()+'_of'))
