import sqlite3

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

def change_password(username, new_pw, db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("UPDATE USERS SET PASSWORD='"+new_pw+"' WHERE NAME='"+username+"';")
    conn.commit()
    conn.close()
