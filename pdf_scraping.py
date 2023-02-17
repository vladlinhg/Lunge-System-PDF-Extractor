"""
    An application can extract content in pdf file into mysql server and store them
"""
import getpass
from pathlib import Path
import pdfplumber
#import mysql.connector
import json
import os
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
    def init(self) -> None:
        dir = input()
        self.dir = Path(dir)

class DirInput(Directory):
    def init(self) -> None:
        input_type = input("To scan one pdf, enter 'pdf'. To scan an entire directory, enter 'dir'." )
        if input_type == 'pdf':
            dir = input("Please enter the full pdf path for data input: ")
        elif input_type == 'dir':
            dir = input("Please enter the full directory path:")
            self.pdf_dir = [f for f in os.listdir(dir) if f.endswith('.pdf')]
        else:
            raise Exception("Invalid input type, please enter 'dir' or 'pdf'.")
        self.dir = Path(dir)

class DirOutput(Directory):
    def init(self) -> None:
        dir = input("Please enter the full .json / .    txt path for output: ")
        self.dir = Path(dir)
    
def extract_data(pdf_path):
    #function to extract data from pdf.
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        #extracting text with pdfplumber, initialize full text variable to extract to.
        for page in pdf.pages:
            full_text += page.extract_text(
                x_tolerance=3,
                y_tolerance=3,
                keep_blank_chars=False,
                use_text_flow=False,
                horizontal_ltr=True,
                vertical_ttb=True,
                extra_attrs=[],
                split_at_punctuation=False
            )
        #Split string with newline seperator
        paragraphs = full_text.split("\n")
        #Initialize paragraph count and variable
        current_paragraph = ""
        paragraph_number = 1
        content = []
        for paragraph in paragraphs:
            #Strip whitespace
            if paragraph.strip() == "":
                #Check if paragraph is empty. If it is, clear string and add paragraph count, append text
                if current_paragraph != "":
                    content.append({"paragraph_number": paragraph_number, "text": current_paragraph})
                    current_paragraph = ""
                    paragraph_number += 1
            else:
                #Append current paragraph to paragraph
                current_paragraph += " " + paragraph
        if current_paragraph != "":
            #Once all paragraphs are processed, append to the content list
            content.append({"paragraph_number": paragraph_number, "text": current_paragraph})
        return content

def main():
    dirinput = DirInput()
    dirinput.init()
    diroutput = DirOutput()
    diroutput.init()
    content = []
    #Check to see if the input has attribute to scan entire directory
    if hasattr(dirinput, 'pdf_dir'):
        for pdf_file in dirinput.pdf_dir:
            pdf_path = os.path.join(dirinput.dir, pdf_file)
            content += extract_data(pdf_path)
    else:
    #If no attribute, read pdf as usual
        content = extract_data(dirinput.dir)
    jsonString = json.dumps(content)
    jsonFile = open(diroutput.dir, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

if __name__ == "__main__":
    main()

