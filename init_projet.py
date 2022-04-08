# Lancer ce script pour initialiser le projet.
import os
import sqlite3
os.mkdir("uploads")
os.mkdir("zips")
print("Dossiers créés")
conn = sqlite3.connect("test.db")
conn.execute("CREATE TABLE USERS(NAME CHAR(12) PRIMARY KEY, PASSWORD TEXT);")
print("table ok")
conn.commit()
print("commit ok")
conn.close()
