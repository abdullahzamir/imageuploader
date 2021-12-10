from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filenam
import os
app=Flask(__name__)

upload_folder = '/home/gc/Desktop/project/imageuploader/'
allowed_ext = {'png','jpeg','jpg'}
app.config['upload_folder']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext

@app.route('/')
def hello_world():
    return "hello, world1"

@app.route('/uploads', methods=['POST'])
def uploads():
    file = request.files['file']    
    if not file:
        return "no file uploaded" , 400
    if file and allowed_file(file.filename):
        filename= secure_filenam(file.filename)
        file.save(os.path.join(app.config['upload_folder'],filename))
            



