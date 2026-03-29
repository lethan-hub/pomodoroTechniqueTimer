import sqlite3
import os

print(os.getcwd())



def library():
# 1. Connect to a database file (it creates it if it doesn't exist)
    connection = sqlite3.connect('productivity.db')

# 2. Create a "Cursor" (This is like the 'pen' that writes the data)
    cursor = connection.cursor()

# 3. Write a command to create the "Tasks" table
# We define the "Columns" here (Name, Target, Status, etc.)

    
    try:
        cursor.execute('''
            
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            total_pomodoros INTEGER DEFAULT 1,
            completed_pomodoros INTEGER DEFAULT 0
        )
        ''')
    except Exception as e:
        print(e)


    connection.commit()
    connection.close()

library()




