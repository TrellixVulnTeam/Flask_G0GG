from flask import render_template, url_for, flash, redirect, request
from app2.forms import RegistrationForm, LoginForm
from app2 import app, db, bcrypt
from app2.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author':'Piotr Łakomiec',
        'title': 'FrioArte',
        'content':'First post content',
        'date_posted':'April 20,2018'
    },
{
        'author':'Marcin Grabarczyk',
        'title': 'Post number 2 ',
        'content':'Second post content',
        'date_posted':'April 21,2018'
    },
{
        'author':'Chuck Noris',
        'title': 'War in Wietnam',
        'content':'War war war',
        'date_posted':'April 20,1956'
    }
]

@app.route("/")
@app.route("/home")
def home():

    return render_template("home.html", posts=posts)


@app.route("/about")
def about():

    return render_template("about.html", title='About')

@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:#wyłączenie strony rejestracji jeżeli użytkownik jest zalogowany
        return redirect(url_for('home'))
    form = RegistrationForm()#stworzenie instancji formularze na podstawie stworzonego formularze rejestracji

    if form.validate_on_submit():#czy formularz został zvalidowany podczas przesyłania(submit)

        #Tworzenie użytkownika, zapisywanie w DB
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')# kodowanie hasła w formie UTD-8
        user = User(username=form.username.data, email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated: #wyłączenie strony logowania jeżeli użytkownik jest zalogowany
        return redirect(url_for('home'))
    form = LoginForm()#stworzenie instancji formularze na podstawie stworzonego formularza logowania

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()# sprawdzanie czy użytkownik o podanym emailu jest w bazie
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data )
            next_page = request.args.get('next') #jeżeli chcemy przejsc do strony wymagajacej logowania w URL przy next zapisany jest adres, do którego chcielismy przejsc. Zapisujemy go w zmiennej
            return redirect(next_page) if next_page else redirect(url_for('home')) #Jeżeli istnieje next_page przejscie do adresu z next_page, inaczej przejscie do home
        else:
            flash('Login Unsuccessful. Please check email and password','danger')

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required #dekorator stawiający wymaganie zalogowania się - jeżeli spróbujemy wejsć na ten adres bez logowania, przekieruje do widoku logowania
def account():
    return render_template('account.html', title='Account')