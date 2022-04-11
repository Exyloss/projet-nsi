# Lancer ce script pour initialiser le projet.
import os
import sqlite3
try:
    os.mkdir("uploads")
except:
    print("dossier uploads deja existant")
try:
    os.mkdir("zips")
except:
    print("dossier zips deja existant")
print("Dossiers créés")
conn = sqlite3.connect("test.db")
conn.execute("CREATE TABLE USERS(NAME CHAR(12) PRIMARY KEY, PASSWORD TEXT);")
print("table ok")
conn.commit()
print("commit ok")
conn.close()
