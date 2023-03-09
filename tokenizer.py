import spacy
import mysql.connector

from mysql_import import Database, MyDB

nlp = spacy.load("en_core_web_sm")


def main():
    mydb = MyDB(Database())
    database = mydb.show_databases()
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
            columns = ["paragraph_id", "text", "lemma", "pos", "tag", "dep", "head"]
            values = [id, token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.head.text]
            mydb.insert_multi_data(database, target, columns, values)
            t_counter += 1
        print("Paragraph {} has {} tokens.".format(p_counter, t_counter))
        p_counter += 1
    print("Total number of paragraphs: {}".format(p_counter))
        


if __name__ == "__main__":
    main()