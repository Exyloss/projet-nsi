from flask import Flask, render_template, request, send_file, redirect, session
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
import chemin
import bdd
import subprocess

app = Flask(__name__)
bcrypt = Bcrypt(app)

try:
    os.mkdir("uploads")
except:
    print("Dossier déjà créé.")

app.secret_key = "123"

db_path = os.getcwd()+"/test.db"
zip_dir = os.getcwd()+"/zips/"
os.popen("rm "+zip_dir+"*")
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


def list_files(chemin):
    """
    chemin: chemin à explorer (str)
    fonction renvoyant un tuple contenant les fichiers en indice 0
    et les dossiers en indice 1 présents dans le répertoire
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
        if path_show == "": path_show = "/"
        return render_template('index.html', files=items[0], folders=items[1], path=path_show, username=session["username"], show_rename="")
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
    if request.method == 'POST':
        files = request.files.getlist("files[]")
        for f in files:
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
    return redirect("/")

@app.route('/remove/<name>')
def remove_file(name):
    """
    Supprime les dossiers/fichiers à l'aide de la command unix rm.
    """
    os.system("rm -rf "+session["chemin"]+"/"+name)
    return redirect("/")

@app.route('/download/<name>')
def download_file(name):
    """
    utilise la fonction send_file intégrée dans flask afin de
    permettre à l'utilisateur final de télécharger le fichier sélectionné.
    """
    return send_file(session["chemin"]+"/"+name, as_attachment = True)

@app.route('/folder_dl/<folder>')
def download_folder(folder):
    """
    Fonction permettant de télécharger un dossier en le zippant.
    """
    try:
        process = subprocess.Popen(["zip","-r",zip_dir+folder+".zip",session["chemin"]+"/"+folder])
        while process.wait() != 0:
            continue
        return send_file(zip_dir+folder+".zip", as_attachment = True)
    except:
        print("erreur lors du zipage")
        return redirect("/")


@app.route('/edit/<name>')
def edit_file(name):
    """
    Fonction ouvrant l'éditeur de texte avec le fichier que
    l'utilisateur souhaite visionner
    """
    try:
        file = open(session["chemin"]+"/"+name, "r")
        file_content = file.read()
        file.close()
        return render_template('editor.html', file_content=file_content, file_name=name, username=session["username"])
    except:
        return redirect("/")

@app.route('/newfolder', methods = ["POST"])
def new_folder():
    if request.method == "POST":
        folder_name = request.form['folder_input']
        folder_name = secure_filename(folder_name)
        try:
            os.mkdir(session["chemin"]+"/"+folder_name)
        except:
            print("Erreur")
    return redirect("/")

@app.route('/save/<name>', methods = ["POST"])
def save_file(name):
    if request.method == "POST":
        content = request.form['ta']
        print(content)
        file = open("uploads/"+name, "w")
        file.write(content)
        file.close()
        return render_template('editor.html', file_name=name, file_content=content)

@app.route('/search', methods = ["POST"])
def search_file():
    if request.method == "POST":
        search = request.form['sb']
        res=[]
        res2=[]
        files = list_files(session["chemin"])[0]
        folders = list_files(session["chemin"])[1]
        for i in files:
            if search in i:
                res.append(i)
        for i in folders:
            if search in i:
                res2.append(i)
        path_show = session["chemin"].replace(session["default_dir"], "")
        if path_show == "": path_show = "/"
        return render_template('index.html', files=res, folders=res2, path=path_show, username=session["username"])
    else:
        return redirect("/")

@app.route('/goto/<folder>')
def goto_folder(folder):
    if folder in list_files(session["chemin"])[1]:
        try:
            session["chemin"] = chemin.chdir(session["chemin"], folder)
        except:
            print("Erreur, dossier inconnu.")
    return redirect("/")

@app.route('/return')
def return_folder():
    if session["chemin"] != default_dir+"/"+session["username"]:
        session["chemin"] = chemin.previous(session["chemin"])
    return redirect("/")

@app.route('/rename/<name>', methods=["POST", "GET"])
def rename(name):
    if request.method == "POST":
        files = list_files(session["chemin"])
        newname = secure_filename(request.form["new_name"])
        if newname not in files[0] and newname not in files[1]:
            os.popen("mv "+session["chemin"]+"/"+name+" "+session["chemin"]+"/"+newname)
    return redirect("/")

@app.route('/account')
def account():
    return render_template("account.html", user=session["username"], username=session["username"])

@app.route('/change_password', methods=["POST", "GET"])
def new_password():
    if request.method == "POST":
        if bcrypt.check_password_hash(bdd.get_password(session["username"], db_path), request.form["current_password"]):
            pw_hash = bcrypt.generate_password_hash(request.form["new_password"]).decode("utf-8")
            bdd.change_password(session["username"], pw_hash, db_path)
    return redirect("/logout")

@app.route('/delete_account', methods=["POST", "GET"])
def delete_account():
    if request.method == "POST":
        if bcrypt.check_password_hash(bdd.get_password(session["username"], db_path), request.form["password"]):
            bdd.delete(session["username"], db_path)
            os.system("rm -rf "+default_dir+"/"+session["username"])
    return redirect("/logout")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug = True, threaded=True)
