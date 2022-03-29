from flask import Flask, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

try:
    os.mkdir("uploads")
except:
    print("Dossier déjà créé.")

os.chdir("uploads")
app.config["UPLOAD_FOLDER"] = os.getcwd()
default_dir = os.getcwd()

def list_files():
    #ls_f = list(filter(os.path.isfile, os.listdir(".")))
    #ls_d = list(filter(os.path.isdir, os.listdir(".")))
    return ( list(filter(os.path.isfile, os.listdir("."))), list(filter(os.path.isdir, os.listdir("."))) )

@app.route('/')
def index():
    items = list_files()
    path_show = os.getcwd().replace(default_dir, "")
    if path_show == "": path_show = "/"
    return render_template('index.html', files=items[0], folders=items[1], path=path_show)

@app.route('/add', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("files[]")
        for f in files:
            filename = secure_filename(f.filename)
            f.save(app.config['UPLOAD_FOLDER']+"/"+filename)
            file = open(app.config['UPLOAD_FOLDER']+"/"+filename,"rb")
            if True:
                content = file.read()
                file = open(os.getcwd()+"/"+filename, "wb")
                file.write(content)
                file.close()
            else:
                print("erreur lors de la lecture du fichier.")
    return redirect("/")

@app.route('/remove/<name>')
def remove_file(name):
    os.system("rm -rf "+os.getcwd()+"/"+name)
    return redirect("/")

@app.route('/download/<name>')
def download_file(name):
    return send_file(os.getcwd()+"/"+name, as_attachment = True)

@app.route('/edit/<name>')
def edit_file(name):
    try:
        file = open(os.getcwd()+"/"+name, "r")
        file_content = file.read()
        file.close()
        return render_template('editor.html', file_content=file_content, file_name=name)
    except:
        return redirect("/")

@app.route('/newfolder', methods = ["POST"])
def new_folder():
    if request.method == "POST":
        folder_name = request.form['folder_input']
        folder_name = secure_filename(folder_name)
        try:
            os.mkdir(folder_name)
        except:
            print("Erreur lors de la création du dossier.")
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
        print(search)
        res=[]
        res2=[]
        files = list_files()[0]
        folders = list_files()[1]
        for i in files:
            if search in i:
                res.append(i)
        for i in folders:
            if search in i:
                res2.append(i)
        print(res)
        return render_template('index.html', files=res, folders=res2, path=os.getcwd())
    else:
        return redirect("/")

@app.route('/goto/<folder>')
def goto_folder(folder):
    if folder in list_files()[1]:
        try:
            os.chdir(folder)
            app.config["UPLOAD_FOLDER"] = os.getcwd()
        except:
            print("Erreur, dossier inconnu.")
    return redirect("/")

@app.route('/return')
def return_folder():
    if os.getcwd() != default_dir:
        os.chdir("..")
        app.config["UPLOAD_FOLDER"] = os.getcwd()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug = True)
