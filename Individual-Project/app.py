from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
config = {
  "apiKey": "AIzaSyB6aEzCB1tDsBelN6sW4yXTE8Sn_oBMJRM",
  "authDomain": "tears-8f32c.firebaseapp.com",
  "projectId": "tears-8f32c",
  "storageBucket": "tears-8f32c.appspot.com",
  "messagingSenderId": "880877485062",
  "appId": "1:880877485062:web:3e74d72f7cdaeca7f81787",
  "databaseURL":"https://tears-8f32c-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Log in-----------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def signin(): 
   bye=""  
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       maw=email.split('@')
       password =request.form['password']
       try:
         login_session['user'] = auth.sign_in_with_email_and_password(email, password)
         UID=login_session['user']['localId']
         dicthehe={'fif':maw[0]}
         db.child('Users').child('UID').update(dicthehe)
         return redirect(url_for('choose'))
       except:
        error = "Authentication failed"
   return render_template("index.html", error=error)
 
#Sign up-----------------------------------------------------------------------------------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        maw=email.split('@')
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID=login_session['user']['localId']
            dicthehe={'fif':maw[0]}
            db.child('Users').child('UID').set(dicthehe)
            return redirect(url_for('choose'))
        except:
            
            error = "Authentication failed"
    return render_template("signup.html",error=error)
#Choose Route----------------------------------------------------------------------------------------------------
@app.route('/choose')
def choose():
    wazza= db.child('Users').child('UID').get().val()['fif']
    return render_template('choose.html',wazza=wazza)
    
#Choose Comic Route----------------------------------------------------------------------------------------------------
@app.route('/choose_comic', methods=['GET', 'POST'])
def choose_comic():
    if request.method == 'POST':
        comment=request.form.get('comment')
        if comment:
            db.child("Comments").push({'comment':comment})
    comments=db.child("Comments").get().val()
    if comments is None:
        comments={}
    return render_template('choocom.html',comments=comments)

#Choose Comic Route----------------------------------------------------------------------------------------------------
@app.route('/choose_comi/<comment_id>')
def choose_comi(comment_id):
    db.child("Comments").child(comment_id).remove()
    comments=db.child("Comments").get().val()
    if comments is None:
        comments={}

    return render_template('choocom.html',comments=comments)

#History Route----------------------------------------------------------------------------------------------------
@app.route('/history')
def history():
    return render_template('history.html')


#Comic #0 Route----------------------------------------------------------------------------------------------------
@app.route('/comic0')
def comic_0():
    return render_template('comic_0.html')


#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)