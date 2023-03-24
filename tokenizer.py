import json
import spacy
import mysql.connector

from mysql_import import Database, MyDB

nlp = spacy.load("en_core_web_sm")



def resources_paragraphs(database, source_table, target_table):
    mydb = MyDB(Database())
    # extract the data from the resources table
    dir = mydb.extract_data(database, source_table, "directory")
    # extract the id from the resources table
    r_id = mydb.extract_data(database, source_table, "id")
    r_counter = 0
    # iterate over the directory and id
    for resource, id in zip(dir, r_id):
        json_path = resource[0]
        with open(json_path, 'r') as f:
            data = json.load(f)
        p_counter = 0
        id = int(''.join(filter(str.isdigit, str(id))))
        for paragraph in data["content"]:
            # get placeholder for the data
            columns = ["frn_resource_id", "text"]
            # get values for the data
            values = [id, paragraph["text"]]
            # insert the data into the paragraphs table
            mydb.insert_multi_data(database, target_table, columns, values)
            p_counter += 1
        # print the number of paragraphs for each resource
        print("Resource {} has {} paragraphs.".format(r_counter, p_counter))
        r_counter += 1
    # print the total number of resources
    print("Total number of resources: {}".format(r_counter))


def main():
    resources_paragraphs("lungesystem", "resources", "paragraphs")
    mydb = MyDB(Database())
    database = "lungesystem"
    table = "paragraphs"
    target = mydb.show_tables(database)
    # extract the data from the paragraphs table
    data = mydb.extract_data(database, table, "text")
    # extract the id from the paragraphs table
    p_id = mydb.extract_data(database, table, "id")
    p_counter = 0
    for paragraph, id in zip(data, p_id):
        # tokenize the paragraph
        doc = nlp(str(paragraph))
        t_counter = 0
        # get the id of the paragraph
        id = int(''.join(filter(str.isdigit, str(id))))
        for token in doc:
            # get placeholder for the data
            columns = ["frn_paragraph_id", "text", "lemma", "pos", "tag", "dep", "head"]
            # get values for the data
            values = [id, token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.head.text]
            # insert the data into the tokens table
            mydb.insert_multi_data(database, target, columns, values)
            t_counter += 1
        # print the number of tokens for each paragraph
        print("Paragraph {} has {} tokens.".format(p_counter, t_counter))
        p_counter += 1
    # print the total number of paragraphs
    print("Total number of paragraphs: {}".format(p_counter))
        


if __name__ == "__main__":
    main()