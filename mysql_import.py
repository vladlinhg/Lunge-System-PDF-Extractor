import mysql.connector
import json
import getpass
import os
import glob
from pathlib import Path
from tqdm import tqdm
from pdf_scraping import Directory


class JsonInput(Directory):
    def __init__(self) -> None:
        dir_type = input("Do you want to import from one individual json or an entire directory? (Type 'json' or 'dir') ")
        if dir_type == 'json':
            dir = input("Please enter the full json path for data input: ")
            self.json_files = [dir]
        elif dir_type == 'dir':
            dir = input("Please enter the directory path: ")
            self.json_files = tqdm(glob.glob(os.path.join(dir, '*.json')))
            if not self.json_files:
                raise Exception("No PDF files in the directory.")
        else:
            raise Exception("Invalid input. Please enter 'json' or 'dir'.")
        self.dir = Path(dir)


class Database:
    def __init__(self) -> None:
        self.hostname = input("What host to connect to: ")
        self.user = input("What user to connect with: ")
        self.password = getpass.getpass("What password to connect with: ")


class MyDB:
    def __init__(self, db: Database):
        """
            MyDB is a class represent an instance of mysql.connector

        Args:
            db (Database): Database is the class stored information to login into specific MySQL server 
        """    
        try:
            res = mysql.connector.connect(
                host=str(db.hostname),
                user=str(db.user),
                password=str(db.password)
            )
            print("Connected successfully.")

            self.db = res
            self.cursor = self.db.cursor()

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
    
    def show_databases(self) -> str:
        self.cursor.execute("show databases")
        print("Databases:")
        print([row for row in self.cursor.fetchall()])
        choice = input("Which one of the above databases do you want to use? ")
        return choice
    
    def show_tables(self, database) -> None:
        self.cursor.execute("use {}".format(database))
        self.cursor.execute("show tables")
        print("Tables:")
        print([row for row in self.cursor.fetchall()])

def main():
    mydb = MyDB(Database())
    mydb.show_databases()
    input_json = JsonInput()
    input_json.init()
    for json_file in input_json.json_files:
        with open(input_json.json_path, 'r') as f:
            data = json.load(f)
        


if __name__ == "__main__":
    main()