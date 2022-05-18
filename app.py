from flask import Flask, render_template, request, send_file, redirect, session, flash
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
import chemin
import bdd
import subprocess
from files_rec import *
from size import convert_octets

app = Flask(__name__)
bcrypt = Bcrypt(app)

try:
    os.mkdir("uploads")
except:
    print("Dossier uploads déjà créé.")

app.secret_key = "123"

db_path = os.getcwd()+"/test.db"
zip_dir = os.getcwd()+"/zips/"
os.system("rm "+zip_dir+"* 2>/dev/null")
os.chdir("uploads")
default_dir = os.getcwd()

def correct_username(un):
    """
    un: nom d'utilisateur (str)
    fonction renvoyant True si le nom d'utilisateur peut être créé, sinon renvoie pourquoi il ne peut pas être créé.
    """
    good_char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    if bdd.exists(un, db_path):
        return "Erreur, le nom d'utilisateur est déjà prit."
    if len(un) > 12:
        return "Erreur, le nom d'utilisateur est trop long."

    for i in un:
        if not i in good_char:
            return "Erreur, vous avez saisi des caractères invalides."
    return True

def file_ext(filename):
    return filename.split(".")[-1]

def list_files(chemin):
    """
    chemin: chemin à explorer (str)
    fonction renvoyant un tuple contenant les fichiers en indice 0
    et les dossiers en indice 1 présents dans le répertoire chemin.
    """
    os.chdir(chemin)
    return ( list(filter(os.path.isfile, os.listdir(chemin))), list(filter(os.path.isdir, os.listdir(chemin))) )

@app.route('/')
def index():
    """
    fonction permettant l'affichage de la page index.html à l'aide de la fonction flask render_template.
    """
    if 'username' in session:
        path_show = session["chemin"].replace(session["default_dir"], "")
        items = list_files(session["chemin"])
        size_list=[convert_octets(os.path.getsize(session["chemin"]+"/"+i)) for i in items[0]]
        if path_show == "": path_show = "/"
        return render_template('index.html', files=items[0], folders=items[1], path=path_show, size_list=size_list)
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Fonction vérifiant si les informations renseignées par l'utilisateur sont correctes
    et le connecte.
    """
    if "username" in session:
        return redirect("/logout")
    if request.method == "POST":
        pw_hash = bdd.get_password(request.form["username"], db_path)
        if pw_hash != None and bcrypt.check_password_hash(pw_hash, request.form["password"]):
            session["username"] = request.form["username"]
            session["chemin"] = chemin.chdir(default_dir, session["username"])
            session["default_dir"] = chemin.chdir(default_dir, session["username"])
            return redirect("/")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if correct_username(request.form["username"]) == True:
            if request.form["password"] == "":
                flash("Erreur, le champ mot de passe ne peut pas être vide.")
                return render_template("login.html")
            try:
                os.mkdir(default_dir+"/"+request.form["username"])
            except:
                print("Erreur lors de la création du dossier.")
                return render_template("login.html")
            session["username"] = request.form["username"]
            pw_hash = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
            bdd.insert(session["username"], pw_hash, db_path)
            session["chemin"] = chemin.chdir(default_dir, session["username"])
            session["default_dir"] = chemin.chdir(default_dir, session["username"])
            return redirect("/")
        else:
            flash("Nom d'utilisateur déjà utilisé ou invalide.")
    return render_template("login.html")

@app.route('/logout')
def logout():
    """
    Supprime les informations de la session
    """
    session.pop('username', None)
    session.pop('chemin', None)
    session.pop('default_dir', None)
    return redirect("/")

@app.route('/add', methods = ['GET', 'POST'])
def upload_file():
    """
    écrit les fichiers renseignés avec la méthode POST dans le chemin actuel
    de l'utilisateur.
    """
    if "username" in session:
        if request.method == 'POST':
            files = request.files.getlist("files[]")
            for f in files:
                if f.filename == "":
                    return redirect("/")
                filename = secure_filename(f.filename)
                f.save(session["chemin"]+"/"+filename)
                file = open(session["chemin"]+"/"+filename,"rb")
                try:
                    content = file.read()
                    file = open(session["chemin"]+"/"+filename, "wb")
                    file.write(content)
                    file.close()
                except:
                    print("erreur lors de la lecture du fichier.")
                    flash("Erreur lors de la lecture du fichier.")
    return redirect("/")

@app.route('/remove/<name>')
def remove_file(name):
    """
    Supprime les dossiers/fichiers à l'aide de la command unix rm.
    """
    os.system("rm -rf "+session["chemin"]+"/"+name)
    return redirect("/")

@app.route('/download')
def download_file():
    """
    utilise la fonction send_file intégrée dans flask afin de
    permettre à l'utilisateur final de télécharger le fichier sélectionné.
    """
    file = request.args.get("path")
    if "username" in session:
        return send_file(session["chemin"]+"/"+file, as_attachment = True)
    else:
        return redirect("/")

@app.route('/folder_dl')
def download_folder():
    """
    Fonction permettant de télécharger un dossier en le zippant.
    """
    folder = request.args.get("path")
    folder_name = secure_filename(folder)
    if "username" not in session:
        return redirect("/")
    try:
        process = os.system("cd "+session["chemin"]+" && zip -r "+zip_dir+folder_name+".zip"+" "+folder+" && cd -")
        return send_file(zip_dir+folder_name+".zip", as_attachment = True)
    except:
        flash("Erreur lors du zipage")
        return redirect("/")


@app.route('/edit/<name>')
def edit_file(name):
    """
    Fonction ouvrant l'éditeur de texte avec le fichier que
    l'utilisateur souhaite visionner
    """
    if "username" not in session:
        return redirect("/")
    if file_ext(name) not in ["jpg", "png", "pdf", "mp4", "mp3", "svg", "zip"]:
        try:
            file = open(session["chemin"]+"/"+name, "r")
            file_content = file.read()
            file.close()
            return render_template('editor.html', file_content=file_content, file_name=name)
        except:
            flash("Erreur lors de la lecture du fichier.")
            return redirect("/")
    else:
        return redirect("/")

@app.route('/newfolder', methods = ["POST"])
def new_folder():
    if "username" not in session:
        return redirect("/")
    if request.method == "POST":
        folder_name = request.form['folder_input']
        folder_name = secure_filename(folder_name)
        try:
            os.mkdir(session["chemin"]+"/"+folder_name)
        except:
            flash("Erreur lors de la création du nouveau dossier.")
    return redirect("/")

@app.route('/save/<name>', methods = ["POST"])
def save_file(name):
    if "username" not in session:
        return redirect("/")
    if request.method == "POST":
        content = request.form['ta']
        file = open(session["chemin"]+"/"+name, "w")
        file.write(content)
        file.close()
        return render_template('editor.html', file_name=name, file_content=content)

@app.route('/search', methods = ["POST"])
def search_file():
    if "username" not in session:
        return redirect("/")
    if request.method == "POST":
        search = request.form['sb']
        res=[]
        res2=[]
        [folders, files] = files_rec(session["chemin"], default_dir+"/"+session["username"]+"/")
        for i in files:
            if search in i:
                res.append(i)
        for i in folders:
            if search in i:
                res2.append(i)
        path_show = session["chemin"].replace(session["default_dir"], "")
        if path_show == "": path_show = "/"
        size_list=[convert_octets(os.path.getsize(session["chemin"]+"/"+i)) for i in files]
        return render_template('index.html', files=res, folders=res2, path=path_show, username=session["username"], size_list=size_list)
    else:
        return redirect("/")

@app.route('/goto')
def goto_folder():
    folder = request.args.get("path")
    process = os.popen("find "+session["chemin"]+" -type d")
    folders = process.read().split("\n")
    process.close()
    folders.pop()
    if default_dir+"/"+session["username"] not in session["chemin"]:
        return redirect("/logout")
    if "username" not in session:
        return redirect("/")
    if session["chemin"]+"/"+folder in folders:
        session["chemin"] = chemin.chdir(session["chemin"], folder)
    else:
        print("Erreur, dossier inconnu.")
        flash("Erreur, dossier inconnu.", "warning")
    return redirect("/")

@app.route('/return')
def return_folder():
    if "username" not in session:
        return redirect("/")
    if session["chemin"] != default_dir+"/"+session["username"]:
        session["chemin"] = chemin.previous(session["chemin"])
    return redirect("/")

@app.route('/rename/<name>', methods=["POST", "GET"])
def rename(name):
    if "username" not in session:
        return redirect("/")
    if request.method == "POST":
        files = list_files(session["chemin"])
        newname = secure_filename(request.form["new_name"])
        if newname not in files[0] and newname not in files[1]:
            os.system("mv "+session["chemin"]+"/"+name+" "+session["chemin"]+"/"+newname)
        else:
            flash("Erreur, un fichier/dossier ayant comme nom "+name+" existe déjà.")
    return redirect("/")

@app.route('/account')
def account():
    return render_template("account.html", user=session["username"])

@app.route('/change_password', methods=["POST", "GET"])
def new_password():
    if "username" not in session:
        return redirect("/")
    if request.method == "POST":
        if bcrypt.check_password_hash(bdd.get_password(session["username"], db_path), request.form["current_password"]):
            pw_hash = bcrypt.generate_password_hash(request.form["new_password"]).decode("utf-8")
            bdd.change_password(session["username"], pw_hash, db_path)
    return redirect("/logout")

@app.route('/delete_account', methods=["POST", "GET"])
def delete_account():
    if "username" not in session:
        return redirect("/")
    if request.method == "POST":
        if bcrypt.check_password_hash(bdd.get_password(session["username"], db_path), request.form["password"]):
            bdd.delete(session["username"], db_path)
            os.system("rm -rf "+default_dir+"/"+session["username"])
    return redirect("/logout")

@app.errorhandler(404)
def not_found(e):
    return "<h1>Erreur, page inconnue</h1>"

if __name__ == "__main__":
    app.run(debug = True, threaded=True)
