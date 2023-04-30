from flask import Flask, render_template, flash, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from datetime import datetime
from Forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3


app = Flask(__name__, template_folder='Scripts/Templates')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rentuser.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.app_context().push()

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

conn = sqlite3.connect('rentuser.db')
print("database opened")

#conn.execute("create table Users (username TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL PRIMARY KEY, password TEXT NOT NULL)")
#print("table users created")
#Testing that data added successfully
#conn.execute("INSERT INTO Users (username,email,password) VALUES ('user1','bill@gmail.com', 'password1' )")
cursor = conn.execute("SELECT username, email,password from Users")
for row in cursor:
    print("username = ", row[0])
    print("email = ", row[1])
    print("password = ", row[2])
print("Operation done successfully")
conn.close()


login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    email = db.Column(db.String(150), primary_key=True, unique=True, index=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(150))
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.email


db.create_all()



#@login_manager.user_loader
#def load_user(User_email):
#    return User.get_id()

@login_manager.user_loader
def load_user(User_email):
    return User.query.get(User_email)



@app.route('/home')
def home():
    return render_template('Homepage.html')

@app.route('/test')
def bootstraptest():
    return render_template('AccountCreationBootstrapPage.html')

@app.route('/generaltemplate')
def generaltemplate():
    return render_template('General template for all pages.html')

@app.route('/leavereview')
@login_required
def leavereview():
    return render_template('LeaveAReview.html')

#route here to input reviws to the new reviews database
#@app.route('/inputreview', methods=['POST', 'GET'])
#@login_required
#def inputreview():
#    form = ReviewForm()
#    if form.validate_on_submit():
#        currentuser = User(username=form.username.data, email=form.email.data)  #email = form.email.data
#        currentuser.set_password(form.password1.data)
#        #currentuser.set_password(currentuser.password_hash)
#        db.session.add(currentuser)
#        db.session.commit()

#        conn = sqlite3.connect('rentuser.db')
#        print("database opened to register user")
#        #conn.execute("INSERT INTO Users ( username, email, password_hash)")
#        conn.execute("INSERT INTO Users ( username, email, password) VALUES (?, ?, ?)",
#                     (form.username.data, form.email.data, currentuser.password_hash))

#        #cursor = conn.execute("SELECT * from Users")
#        #for row in cursor:
        #    print("username = ", row[0])
        #    print("email = ", row[1])
        #    print("password = ", row[2])
        #print("Operation done successfully")
#        conn.close()
#        return redirect(url_for('login'))
#    return render_template('AccountCreationBootstrapPage.html', form=form)


#need to figure out how to add these users to the database and check they are validatining against the entries in there
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        currentuser = User(username=form.username.data, email=form.email.data)  #email = form.email.data
        currentuser.set_password(form.password1.data)
        #currentuser.set_password(currentuser.password_hash)
        db.session.add(currentuser)
        db.session.commit()

        conn = sqlite3.connect('rentuser.db')
        print("database opened to register user")
        #conn.execute("INSERT INTO Users ( username, email, password_hash)")
        conn.execute("INSERT INTO Users ( username, email, password) VALUES (?, ?, ?)",
                     (form.username.data, form.email.data, currentuser.password_hash))

        #cursor = conn.execute("SELECT * from Users")
        #for row in cursor:
        #    print("username = ", row[0])
        #    print("email = ", row[1])
        #    print("password = ", row[2])
        #print("Operation done successfully")
        conn.close()
        return redirect(url_for('login'))
    return render_template('AccountCreationBootstrapPage.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get("next")
            return redirect(next or url_for('home'))
        flash('Invalid email address or Password.')
    return render_template('BootstrapLoginPage.html', form=form)


@app.route("/forbidden", methods=['GET', 'POST'])
@login_required
def protected():
    return render_template('Forbidden.html')

#Changed above from redirect to render template

@app.route("/reviews", methods=['GET', 'POST'])
def reviews():
    return render_template('Review Search Results Page Template.html')


@app.route("/logout")
# @login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
