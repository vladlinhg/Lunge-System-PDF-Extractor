"""
    An application can extract content in pdf file into mysql server and store them
"""
import getpass
from pathlib import Path
import pdfplumber
import mysql.connector


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
            print("Connect successfully.")

            self.db = res
            self.cursor = self.db.cursor()

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
    
    def show_databases(self) -> None:
        self.cursor.execute("show databases")
        print([row for row in self.cursor.fetchall()])

    def create_database(self) -> None:
        self.cursor.execute("create database lunge_test")
        print("Database 'lunge_test' created in the server")
    
    def create_table(self) -> None:
        self.cursor.execute("use lunge_test")
        pass

class Directory:
    def __init__(self) -> None:
        dir = input("Please Enter the directory in /xx/xx/xx or c:/xxx/xxx: ")
        self.dir = Path(dir)

class DirInput(Directory):
    def __init__(self) -> None:
        super().__init__()

class DirOutput(Directory):
    def __init__(self) -> None:
        super().__init__()

    



def main():
    dirinput = DirInput()
    diroutput = DirOutput()
    with pdfplumber.open(dirinput.dir) as pdf:
        for page in pdf.pages:
            text = page.extract_words(x_tolerance=3, y_tolerance=3, keep_blank_chars=False, use_text_flow=False, horizontal_ltr=True, vertical_ttb=True, extra_attrs=[], split_at_punctuation=False)
            print(text)




if __name__ == "__main__":
    main()