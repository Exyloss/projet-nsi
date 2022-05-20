# Projet de NSI
Dépendances :
 - python
 - pip
 - flask
 - gunicorn

Installer les dépendances :
pip install flask flask-bcrypt gunicorn

Lancer le projet en mode développement :
flask run

Sinon :
sudo gunicorn --workers 3 --bind 0.0.0.0:80 app:app
