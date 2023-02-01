"""
    An application can extract content in pdf file into mysql server and store them
"""
import getpass
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
        self.cursor.execute("create table articles (string ")

    



def main():
    db = Database()
    mydb = MyDB(db)
    mydb.show_databases()
    mydb.create_database()


if __name__ == "__main__":
    main()