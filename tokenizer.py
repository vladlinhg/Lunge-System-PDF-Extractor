import json
import spacy
import mysql.connector

from mysql_import import Database, MyDB

nlp = spacy.load("en_core_web_sm")



def resources_paragraphs(database, source_table, target_table):
    mydb = MyDB(Database())
    dir = mydb.extract_data(database, source_table, "directory")
    r_id = mydb.extract_data(database, source_table, "id")
    r_counter = 0
    for resource, id in zip(dir, r_id):
        json_path = resource[0]
        with open(json_path, 'r') as f:
            data = json.load(f)
        p_counter = 0
        id = int(''.join(filter(str.isdigit, str(id))))
        for paragraph in data["content"]:
            columns = ["frn_resource_id", "text"]
            values = [id, paragraph["text"]]
            mydb.insert_multi_data(database, target_table, columns, values)
            p_counter += 1
        print("Resource {} has {} paragraphs.".format(r_counter, p_counter))
        r_counter += 1
    print("Total number of resources: {}".format(r_counter))


def main():
    resources_paragraphs("lungesystem", "resources", "paragraphs")
    mydb = MyDB(Database())
    database = "lungesystem"
    table = "paragraphs"
    target = mydb.show_tables(database)
    data = mydb.extract_data(database, table, "text")
    p_id = mydb.extract_data(database, table, "id")
    p_counter = 0
    for paragraph, id in zip(data, p_id):
        doc = nlp(str(paragraph))
        t_counter = 0
        id = int(''.join(filter(str.isdigit, str(id))))
        for token in doc:
            columns = ["frn_paragraph_id", "text", "lemma", "pos", "tag", "dep", "head"]
            values = [id, token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.head.text]
            mydb.insert_multi_data(database, target, columns, values)
            t_counter += 1
        print("Paragraph {} has {} tokens.".format(p_counter, t_counter))
        p_counter += 1
    print("Total number of paragraphs: {}".format(p_counter))
        


if __name__ == "__main__":
    main()