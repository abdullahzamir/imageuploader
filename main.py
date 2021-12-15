from flask import Flask, flash, request, redirect, url_for, render_template
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
import subprocess as sp
import os
app=Flask(__name__)

allowed_ext = {'png','jpeg','jpg'}
upload_folder = 'images'
app.config['upload_folder'] = upload_folder


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext



@app.route('/', methods=['GET','POST'])
def uploads():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename= secure_filename(file.filename)
            file.save(os.path.join(app.config['upload_folder'],filename))
    return render_template('index.html')



@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['upload_folder'],name)

@app.route('/images.php')
def images():
    out = sp.run(["php","img.php"], stdout=sp.PIPE)
    return out.stdout

