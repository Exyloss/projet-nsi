from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from wtforms import SubmitField
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads/"

def list_files():
    ls_c = os.popen("ls -1 uploads/").read()
    ls_c = ls_c.split("\n")
    ls_c.pop()
    return ls_c


@app.route('/')
def upload_file():
    return render_template('index.html', files=list_files())


@app.route('/add', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(app.config['UPLOAD_FOLDER'] + filename)

        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
        try:
            content = file.read()
        except:
            content = "Contenu impossible à afficher."

        os.system("echo \""+content+"\" > "+"uploads/"+filename)

    return render_template('index.html', files=list_files())

@app.route('/remove/<name>')
def remove_file(name):
    os.system("rm uploads/"+name)
    return render_template('index.html', files=list_files())

@app.route('/download/<name>')
def download_file(name):
    return send_file('uploads/'+name, as_attachment = True)

@app.route('/edit/<name>')
def edit_file(name):
    print(name)
    file = open("uploads/"+name, "r")
    file_content = file.read()
    file.close()
    return render_template('editor.html', file_content=file_content, file_name=name)

@app.route('/save/<name>', methods = ["POST"])
def save_file2(name):
    if request.method == "POST":
        content = request.form['ta']
        print(content)
        file = open("uploads/"+name, "w")
        file.write(content)
        file.close()
        return render_template('editor.html', file_name=name, file_content=content)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)

