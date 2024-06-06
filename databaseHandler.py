import sqlite3 as sql
import random

class DataBaseHandler:
    def __init__(self, name):
        self.name = name

    def connect(self):
        self.connection = sql.connect(self.name)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()

    def buildTables(self):
        self.connect()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS user (
                            username TEXT PRIMARY KEY,
                            password TEXT NOT NULL
                                );""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS task (
                            taskID INTEGER PRIMARY KEY,
                            description TEXT NOT NULL,
                            date TEXT NOT NULL,
                            username TEXT NOT NULL,
                            FOREIGN KEY(username) REFERENCES user(username)
        );""")
        
        self.disconnect()

    def addUser(self, username, password):
        self.connect()
        self.cursor.execute("""INSERT INTO user 
                            (username, password)
                            VALUES
                            (?,?);
                                """, (username, password))
        self.connection.commit()
        self.disconnect()

    def addTask(self, desc, username):
        id = len(self.selectAllTasks())+1
        date = str(random.randint(1, 30))+"/15/2024"

        self.connect()
        self.cursor.execute("""INSERT INTO task 
                            (taskID, description, date, username)
                            VALUES
                            (?,?,?,?);
                                """, (id, desc, date, username))
        self.connection.commit()
        self.disconnect()

    def authenticate(self, username, password):
        global currentUser
        self.connect()
        self.cursor.execute("""SELECT username FROM user WHERE username = ? AND password = ?;""", (username, password))

        result = self.cursor.fetchone()
        
        self.disconnect()
        
        
        if result != None:
            currentUser = result[0]
            return True
        else:
            return False
        
    def selectAllData(self):
        self.connect()
        self.cursor.execute("""SELECT * FROM user""")
        print(self.cursor.fetchall())
        self.cursor.execute("""SELECT * FROM task""")
        print(self.cursor.fetchall())
        self.disconnect()

    def deleteRecordInUserByUsername(self, username):
        self.connect()
        self.cursor.execute("""DELETE FROM user WHERE username=?;""", (username,))
        self.connection.commit()
        self.disconnect()
        

    def deleteRecordInTaskByUsername(self, username):
        self.connect()
        self.cursor.execute("""DELETE FROM task WHERE username=?;""", (username,))
        self.connection.commit()
        self.disconnect()
        self.resetIDsforTasks()

    def deleteRecordInTaskById(self, id):
        self.connect()
        self.cursor.execute("""DELETE FROM task WHERE taskID=?;""", (id,))
        self.connection.commit()
        self.disconnect()
        self.resetIDsforTasks()

    def selectAllTasksByUser(self, username):
        self.connect()
        self.cursor.execute("""SELECT * FROM task WHERE username = ?;""", (username,))
        result = self.cursor.fetchall()
        self.disconnect()
        return result
    
    def selectAllTasks(self):
        self.connect()
        self.cursor.execute("""SELECT * FROM task ;""")
        result = self.cursor.fetchall()
        self.disconnect()
        return result

    def resetIDsforTasks(self):
        self.connect()
        self.cursor.execute("SELECT COUNT(*) FROM task;")
        num_of_records = self.cursor.fetchone()[0]
        
        for row in range(0, num_of_records):
            self.cursor.execute("SELECT taskID FROM task LIMIT 1 OFFSET ?", (row, ))
            currentRecord = self.cursor.fetchone()
            if currentRecord[0] != row:
                self.cursor.execute("UPDATE task SET taskID=:newid WHERE taskID=:currentid", {"newid": row+1, "currentid": currentRecord[0]})

        
        self.connection.commit()  
        self.disconnect()

    def delete_tables(self):
        self.connect()
        self.cursor.execute("""DROP TABLE task""")
        self.connection.commit()
        self.cursor.execute("""DROP TABLE user""")
        self.connection.commit()
        self.disconnect()
     