
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from os import system

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads/"

def list_files():
    ls_c = system("ls uploads/")
    ls_c.split(" ")
    return ls_c


@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/display', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(app.config['UPLOAD_FOLDER'] + filename)

        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()
        system("echo \""+content+"\" > "+"uploads/"+filename)
        print(list_files())


    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug = True)

