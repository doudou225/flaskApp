from flask import render_template, redirect, url_for, flash, request
from mysite.form import RegistrationForm, LoginForm
from mysite.model import User
from flask_login import login_user, current_user, login_required, logout_user
from mysite import app, db, bcrypt

@app.route("/")
def home():
    return render_template('index.html', title="AppSolutionly - Home")

@app.route("/contact/")
def contact():
    return render_template('contact.html', title="AppSolutionly - Contact US!")

@app.route("/portfolio/")
@login_required
def portfolio():
    return render_template('portfolio.html', title="AppSolutionly - Our Portfolio!")

@app.route("/register/", methods=['GET', 'POST'])
def register():
    # If user is already authenticated and try to register, send them to the home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # To make sure user don't use existing username or email, we'll do the check in the registration model instead of setting a check agains the DB here
    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password = hashed_password
        )
        db.session.add(user)
        db.session.commit()

        # for the flash message to show up, we need to update our template. Layout.html would be easier
        flash('Account created successfully! You can now log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register today!", form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    # If user is already authenticated and try to register, send them to the home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # if user exist and stored password == form provided password, the log him/her in!
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            # if next parameter exist in the url, grab it and send user to the desired page
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
            
    return render_template('login.html', title="Sign In!", form=form)


# @login_required should be underneath the route definition to work.
@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route("/account/")
@login_required
def account():
    return render_template('account.html', title="Account settings")

@app.route("/members/")
@login_required
def members():
    return render_template('members.html', title="Explore!")



    