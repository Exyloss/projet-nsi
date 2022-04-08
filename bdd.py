import sqlite3

def initialize(db_path):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("DROP TABLE USERS;")
    except:
        print("pas de table users.")
    conn.execute("CREATE TABLE USERS(NAME CHAR(12) PRIMARY KEY, PASSWORD TEXT);")
    print("table ok")
    conn.commit()
    print("commit ok")
    conn.close()
    return None

def insert(name, password, db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("INSERT INTO USERS (NAME, PASSWORD) VALUES ('"+name+"', '"+password+"');")
    conn.commit()
    conn.close()

def is_correct(name, password, db_path):
    query = (name, password)
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT * FROM USERS;")
    for line in cursor:
        if line == query:
            return True
    conn.close()
    return False

def exists(username, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT NAME FROM USERS;")
    for i in cursor:
        if i[0] == username:
           return True
    return False

def delete(username, db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("DELETE FROM USERS WHERE NAME='"+username+"';")
    conn.commit()
    conn.close()

def show_values(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT * FROM USERS;")
    for i in cursor:
        print(i)
    conn.close()

def get_password(username, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT PASSWORD FROM USERS WHERE NAME='"+username+"';")
    for i in cursor:
        return i[0]
