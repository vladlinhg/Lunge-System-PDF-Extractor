import mysql.connector
import json
import getpass
import os
import glob
from pathlib import Path
from tqdm import tqdm
from pdf_scraping import Directory


class JsonInput(Directory):
    """
    A class for importing JSON data from either an individual file or a directory of files.

    ...

    Attributes
    ----------
    json_files : list
        A list of file paths to the JSON files that were imported.

    Methods
    -------
    __init__():
        Initializes the class instance by prompting the user to choose between importing an individual JSON file 
        or a directory of files. If a directory is chosen, it searches for all JSON files in that directory.

    """
    def __init__(self) -> None:
        """
        Initializes a JsonInput instance.

        Prompts the user to choose between importing an individual JSON file or a directory of files.
        If a directory is chosen, it searches for all JSON files in that directory.
        """
        dir_type = input("Do you want to import from one individual json or an entire directory? (Type 'json' or 'dir') ")
        if dir_type == 'json':
            dir = input("Please enter the full json path for data input: ")
            self.json_files = [dir]
        elif dir_type == 'dir':
            dir = input("Please enter the directory path: ")
            self.json_files = tqdm(glob.glob(os.path.join(dir, '*.json')))
            if not self.json_files:
                raise Exception("No json files in the directory.")
        else:
            raise Exception("Invalid input. Please enter 'json' or 'dir'.")
        self.dir = Path(dir)



class Database:
    """
    A class for creating a database instance with user-specified connection parameters.

    ...

    Attributes
    ----------
    hostname : str
        The hostname to connect to.
    user : str
        The user to connect with.
    password : str
        The password to connect with.

    Methods
    -------
    __init__():
        Initializes a Database instance.
        Prompts the user to enter the hostname, user, and password to connect to the database.

    """
    def __init__(self) -> None:
        """
        Initializes a Database instance.

        Prompts the user to enter the hostname, user, and password to connect to the database.
        """
        # self.hostname = input("What host to connect to: ")
        # self.user = input("What user to connect with: ")
        # self.password = getpass.getpass("What password to connect with: ")

        self.hostname = "lungesystemsdb.cy9u84h2ibd2.us-west-2.rds.amazonaws.com"
        self.user = "admin"
        self.password = "AbhayGupta"



class MyDB:
    """
    A class that represents an instance of mysql.connector.

    ...

    Attributes
    ----------
    db : mysql.connector.connection_cext.CMySQLConnection
        The connection object representing the connection to the MySQL server.
    cursor : mysql.connector.cursor_cext.CMySQLCursor
        The cursor object representing the database cursor.
        
    Methods
    -------
    __init__(db):
        Initializes a MyDB instance by connecting to a MySQL server using the Database object provided.
    show_databases():
        Retrieves a list of databases on the connected MySQL server and prompts the user to choose one.
        Returns the name of the chosen database as a string.
    show_tables(database):
        Retrieves a list of tables in the given database and prompts the user to choose one.
        Returns the name of the chosen table as a string.
    insert_data(database, table, data):
        Inserts the given data into the specified table in the specified database.

    """
    def __init__(self, db: Database):
        """
        Initializes a MyDB instance by connecting to a MySQL server using the Database object provided.

        Parameters
        ----------
        db : Database
            The Database object containing the connection parameters.
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
        """
        Retrieves a list of databases on the connected MySQL server and prompts the user to choose one.

        Returns
        -------
        str
            The name of the chosen database.
        """
        self.cursor.execute("show databases")
        print("Databases:")
        print([row for row in self.cursor.fetchall()])
        choice = input("Which one of the above databases do you want to use? ")
        return choice
    
    def show_tables(self, database) -> str:
        """
        Retrieves a list of tables in the given database and prompts the user to choose one.

        Parameters
        ----------
        database : str
            The name of the database to retrieve tables from.

        Returns
        -------
        str
            The name of the chosen table.
        """
        self.cursor.execute("use {}".format(database))
        self.cursor.execute("show tables")
        print("Tables:")
        print([row for row in self.cursor.fetchall()])
        choice = input("Which one of the above tables do you want to use? ")
        return choice
    
    def insert_data(self, database, table, data) -> None:
        """
        Inserts the given data into the specified table in the specified database.

        Parameters
        ----------
        database : str
            The name of the database to insert data into.
        table : str
            The name of the table to insert data into.
        data : str
            The data to be inserted into the table.
        """
        self.cursor.execute("use {}".format(database))
        self.cursor.execute("insert into {} (text) values ('{}')".format(table, data))
        self.db.commit()
    
    def insert_multi_data(self, database, table, column, data) -> None:
        """
        Inserts the given data into the specified column in the specified table in the specified database.

        Parameters
        ----------
        database : str
            The name of the database to insert data into.
        table : str
            The name of the table to insert data into.
        column : list
            The list of columns to insert data into.
        data : list
            The data to be inserted into the table.
        """
        self.cursor.execute("use {}".format(database))
        columns = ', '.join(column)
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, data)
        self.db.commit()
    
    def extract_data(self, database, table, column) -> list:
        """
        Extracts the data from the specified column in the specified table in the specified database.

        Parameters
        ----------
        database : str
            The name of the database to extract data from.
        table : str
            The name of the table to extract data from.
        column : str
            The name of the column to extract data from.

        Returns
        -------
        list
            A list of tuples containing the data from the specified column.
        """
        self.cursor.execute("use {}".format(database))
        self.cursor.execute("select {} from {}".format(column, table))
        return self.cursor.fetchall()


def main():
    mydb = MyDB(Database())
    database = "lungesystem"
    table = "resources"
    input_json = JsonInput()
    counter = 0
    for json_file in input_json.json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
        mydb.insert_multi_data(database, table, ["url", "author", "title", "date", "directory"], [data["url"], data["author"], data["title"], data["publishing_date"], json_file])
        # for paragraph in data["content"]:
        #     mydb.insert_data(database, table, paragraph['text'])
        counter += 1
    print(f" {counter} record(s) inserted.")


if __name__ == "__main__":
    main()