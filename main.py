from flask import Flask, flash, request, redirect, url_for, render_template
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
import subprocess as sp
from datetime import datetime
import os
import mysql.connector as mysql
from hashlib import md5
from flask import session
import shutil
app=Flask(__name__)
app.secret_key = b's3cr3t_k3y'
allowed_ext = {'png','jpeg','jpg','pdf'}
upload_folder = 'images'
app.config['upload_folder'] = upload_folder
chk = "397a39d6700eaa41be9aee2dc4c89b90"
con = mysql.connect(user='root', password='XSa7xBou1CNy', database='mydb')


start_time = ""

def query(query):
    cur = con.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        con.commit()
        print(rows)
        return rows
    except Exception as e:
        print(e)
        con.rollback()
        return e

error = ""


@app.route('/register', methods=['POST','GET'])
def register():
    global error
    if request.method == 'POST':
        error =""
        name = request.form['name']
        username = request.form['username']
        if(len(username)==0):
            return redirect(url_for('register'))
        password = request.form['password']
        
        if(len(username)>25 and len(password)>45 and len(name)>25):
            error = "username or password or name is too long"
            return redirect(url_for('register'))
                    
        if("'" in username or "'" in password):
            return redirect(url_for('register'))
        gender = request.form['gender']
        if gender not in ['M','F']:
            error = "choose a correct gender"
            return redirect(url_for('register'))
        password_hash = md5(password.encode("utf8")).hexdigest()
        try:
            os.mkdir(username)
        except Exception as e:
            return '''
            username already exists
            '''
        query(f"INSERT INTO mydb.user (name,username,password,gender) VALUES ('{name}','{username}','{password_hash}','{gender}')")
        return redirect(url_for('login'))
    return render_template('register.html',error = error)


@app.route('/admin_panel', methods=['GET','POST'])
def admin_panel():
    if "username" in session:
        if session['username'] == "admin":
            if request.method == 'POST':
                q = request.form['query']
                rows = query(q)
                try:
                    return render_template('admin_panel.html',rows=rows)
                except Exception as e:
                    print(e)
                    return render_template('admin_panel.html',error = e)
            else:
                return render_template('admin_panel.html')
        else:
            return redirect(url_for('uploads'))
    else:
        return redirect(url_for('login'))
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
                now = datetime.now()
                formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
                filename= secure_filename(file.filename)
                print(filename)
                upload_folder = username
                file_type = filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(upload_folder,filename))
                query(f"INSERT INTO mydb.image (username,file_name,image_type,upload_time) VALUES ('{username}','{filename}','{file_type}','{formatted_date}')")     
        return render_template('index.html',upload = 'Poor man Uploader',user = session['username'], upload_url = 'quiz')
   
    else:
        return redirect(url_for('login'))



@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['upload_folder'],name)

@app.route('/images.php')
def images():
    if "username" in session:   
        out = sp.run(["php","img.php",session['username']], stdout=sp.PIPE,shell=True)
        return out.stdout
    else:
        return redirect(url_for('login'))


@app.route('/', methods=['POST','GET'])
def login():
    global start_time
    if "username" in session:
        if("'" in session['username'] or "'" in session['password']):
            session.pop('username', None)
            session.pop('password', None)
            return redirect(url_for('login'))
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        if("'" in session['username'] or "'" in session['password']):
            return redirect(url_for('login'))
        flag = verify(session['username'],session['password'])
        if flag:
            now = datetime.now()
            start_time = now.strftime('%Y-%m-%d %H:%M:%S')
            query('INSERT INTO mydb.session (username,session_start) VALUES ("'+session['username']+'","'+start_time+'")')
            return redirect(url_for('uploads'))
    return render_template('login.html')


def verify(username,password):
    user = session['username']
    password = session['password']
    chk = query('''SELECT password FROM mydb.user WHERE username = '%s' ''' % user)
    print(len(chk))
    if len(chk) == 0:
        return False
    chk = str(chk[0]).replace("('","").replace("',)","")
    password_hash = md5(password.encode("utf8")).hexdigest()
    print(password_hash)
    if user==username and chk==password_hash:
        return True
    else:
        return False   

@app.route('/logout')
def logout():
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    query(f"UPDATE mydb.session SET session_end = \'{formatted_date}\' WHERE username = \'{session['username']}\' and session_start = \'{start_time}\'")
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))


@app.route('/search' , methods=['POST','GET'])
def search():
    print("search")
    print(request.method)
    print(session['username'])
    if "username" in session:
        print("username in session")    
        if request.method == 'POST':
            print("search")
            search = request.form['search']
            if search == "":
                return redirect(url_for('uploads'))
            search = search.replace("'","")
            images = []
            rows = query(f"SELECT file_name FROM mydb.image WHERE username = \'{session['username']}\' and (file_name like \'%{search}%\' or image_type like \'%{search}%\')")
            print(rows)
            for row in rows:
                images.append(row[0])
            array_string = ' '.join(images)
            print(array_string)
            out = sp.run(["php","search.php",array_string,session['username']], stdout=sp.PIPE,shell=True)
            return out.stdout
    else:
        return redirect(url_for('search'))
    return '''
    <a href="http://127.0.0.1:5000/index">Home</a>
    <p> Search </p>
    <form method="post">
        <p>Search: <input type=text name=search>
        <p><input type=submit value=submit>
    </form>
    '''
@app.route('/delete', methods=['POST','GET'])
def delete():
    if "username" in session:
        if request.method == 'POST':
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            print("delete")
            file_name = request.form['file_name']
            print(file_name)
            query(f"DELETE FROM mydb.image WHERE username = \'{session['username']}\' and file_name = \'{file_name}\'")
            query(f"INSERT INTO mydb.deleted (username,file_name,date) VALUES (\'{session['username']}\',\'{file_name}\',\'{formatted_date}\' )")
            os.remove(session['username']+"/"+file_name)
            return redirect(url_for('uploads'))
    else:
        return redirect(url_for('login'))
    return '''
    <a href="http://127.0.0.1:5000/index">Home</a>
    <p> Delete </p>
    <form method="post">
        <p> Enter file to delete: </p>
        <p>Delete: <input type=text name=file_name>
        <p><input type=submit value=submit>
    </form>
    '''


@app.route('/backup', methods=['POST','GET'])
def backup():
    if "username" in session:
        if session['username'] == "admin":        
            images = query("select username,file_name from mydb.image")
            print(images)
            for image in images:
                print(image[0],image[1])
                query(f"INSERT INTO mydb.backups (username,file_name) VALUES (\'{image[0]}\',\'{image[1]}\')")
                shutil.copy(image[0]+"/"+image[1],"./backup/"+image[1])
            return redirect(url_for('admin_panel'))
        return redirect(url_for('uploads'))    
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run('localhost',port=5000,debug=True)

