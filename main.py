from flask import Flask, flash, request, redirect, url_for, render_template
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
import subprocess as sp
import os
from hashlib import md5
from flask import session
app=Flask(__name__)
app.secret_key = b's3cr3t_k3y'
allowed_ext = {'png','jpeg','jpg','pdf'}
upload_folder = 'images'
app.config['upload_folder'] = upload_folder
chk = "397a39d6700eaa41be9aee2dc4c89b90"

f=open("database.txt","r")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext



@app.route('/index', methods=['GET','POST'])
def uploads():
    if "username" in session:
        if request.method == 'POST':
            username = session['username']
            print("uploads")
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename= secure_filename(file.filename)
                upload_folder = username
                file.save(os.path.join(upload_folder,filename))        
        return render_template('index.html',upload = 'Poor man Uploader',user = session['username'], upload_url = 'quiz')
    else:
        return redirect(url_for('login'))



@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['upload_folder'],name)

@app.route('/images.php')
def images():
    if "username" in session:    
        out = sp.run(["php","img.php"], stdout=sp.PIPE)
        return out.stdout
    else:
        return redirect(url_for('login'))

# @app.route('/')
#     if 'username' and 'password' in session:
#         render_template('index.html')
#     return redirect(url_for('login'))  


@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        flag = verify(session['username'],session['password'])
        if flag:
            return redirect(url_for('uploads'))
    return '''
    <p> Login </p>
    <form method="post">
        <p>Username: <input type=text name=username>
        <p>Password: <input type=text name=password>
        <p><input type=submit value=login>
    </form>
    '''
def verify(username,password):
    user = 'abdullah'
    password_hash = md5(password.encode("utf8")).hexdigest()
    if user==username and chk==password_hash:
        return True
    else:
        return False   

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/<user>/<upload_folder>',methods = ['GET','POST'])
def upload_quiz(user,upload_folder):
    if "username" in session:
        if request.method == 'POST':
            username = session['username']
            print("uploads")
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename= secure_filename(file.filename)
                upload_folder = 'quiz'
                file.save(os.path.join(username+"/"+upload_folder,filename))        
        return render_template('index.html',upload = upload_folder,user=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/quiz.php')
def quiz_gallery():
    if "username" in session:    
        out = sp.run(["php","quizimg.php"], stdout=sp.PIPE)
        return out.stdout
    else:
        return redirect(url_for('login'))



