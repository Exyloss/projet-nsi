from flask import Flask, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename
import os
from pathpy import Path

app = Flask(__name__)

try:
    os.mkdir("uploads")
except:
    print("Dossier déjà créé.")

app.config["UPLOAD_FOLDER"] = "uploads/"
path = Path()

def list_files(d="uploads/"):
    ls_f = os.popen("find "+d+"* -maxdepth 0 -type f | awk -F '/' '{print $NF}'").read()
    ls_f = ls_f.split("\n")
    ls_f.pop()
    ls_d = os.popen("find "+d+"* -maxdepth 0 -type d | awk -F '/' '{print $NF}'").read()
    ls_d = ls_d.split("\n")
    ls_d.pop()
    print(ls_d)
    return [ls_f, ls_d]

@app.route('/')
def index():
    #path.reset()
    #app.config["UPLOAD_FOLDER"] = path.show()
    return render_template('index.html', files=list_files(path.show())[0], folders=list_files(path.show())[1], path=path.show())

@app.route('/add', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("files[]")
        for f in files:
            filename = secure_filename(f.filename)
            f.save(app.config['UPLOAD_FOLDER'] + filename)
            file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
            try:
                content = file.read()
                os.system("echo \""+content+"\" > "+"uploads/"+filename)
            except:
                print("erreur lors de la lecture du fichier.")
    #return render_template('index.html', files=list_files())
    return redirect("/")

@app.route('/remove/<name>')
def remove_file(name):
    os.system("rm -rf "+path.show()+name)
    #return render_template('index.html', files=list_files())
    return redirect("/")

@app.route('/download/<name>')
def download_file(name):
    return send_file(path.show()+name, as_attachment = True)

@app.route('/edit/<name>')
def edit_file(name):
    print(name)
    file = open(path.show()+name, "r")
    file_content = file.read()
    file.close()
    return render_template('editor.html', file_content=file_content, file_name=name)

@app.route('/newfolder', methods = ["POST"])
def new_folder():
    if request.method == "POST":
        folder_name = request.form['folder_input']
        folder_name = secure_filename(folder_name)
        try:
            os.mkdir("uploads/"+folder_name)
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
        files = list_files(path.show())[0]
        folders = list_files(path.show())[1]
        for i in files:
            if search in i:
                res.append(i)
        for i in folders:
            if search in i:
                res2.append(i)
        print(res)
        return render_template('index.html', files=res, folders=res2, path=path.show())
    else:
        return redirect("/")

@app.route('/goto/<folder>')
def goto_folder(folder):
    if folder in list_files()[1]:
        path.add(folder)
        app.config["UPLOAD_FOLDER"] = path.show()
    #return render_template('index.html', files=list_files(path.show())[0], folders=list_files(path.show())[1])
    return redirect("/")

@app.route('/return')
def return_folder():
    path.up()
    app.config["UPLOAD_FOLDER"] = path.show()
    return redirect("/")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)
