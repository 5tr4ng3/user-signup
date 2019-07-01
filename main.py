from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render()

@app.route("/", methods=['POST'])
def validate_user():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ""
    password_error = ""
    verify_password_error = ""
    email_error = ""

    # Check to make sure username, password and 
    # verify_password aren't empty
    if not username:
        username_error = "Username is required"
    if not password:
        password_error = "Password is required"
    if not verify_password:
        verify_password_error = "Please verify password"

    # Check to make sure username is within character bounds 
    # and doesn't contain any invalid characters
    if len(username) < 4:
        username_error = "Username must be 3-20 characters long"
    elif len(username) > 20:
        username_error = "Username must be 3-20 characters long"

    if username.find(' ') != -1:
        username_error = "Username can't contain space character"

    # Check to make sure password is within character bounds
    # and doesn't contain any invalid characters
    if len(password) < 4:
        password_error = "Password must be 3-20 characters long"
    elif len(password) > 20:
        password_error = "Password must be 3-20 characters long"

    if password.find(' ') != -1:
        password_error = "Password can't contain space character"
    
    # Check to make sure verify_password equals password
    if not (password == verify_password):
        verify_password_error = "Verify password doesn't match password"

    # If user provided an email make sure it is valid
    if email:
        if len(email) < 4:
            email_error = "Email must be 3-20 characters long"
        elif len(email) > 20:
            email_error = "Email must be 3-20 characters long"
        
        if email.find(' ') != -1:
            email_error = "Email can't contain space character"
        if email.find('@') != -1 and email.find('.') != -1:
            if email.count('@') > 1:
                email_error = "Must be a valid email"
            if email.count('.') > 1:
                email_error = "Email can only contain one '.'"
        else:
            email_error = "Must be a valid email"

    if username_error or password_error or verify_password_error or email_error:
        template = jinja_env.get_template('index.html')
        return template.render(username_error=username_error, password_error=password_error,
            verify_password_error=verify_password_error, email_error=email_error,
            username=username, email=email)
    else:
        template = jinja_env.get_template('welcome-page.html')
        return template.render(username=username)


app.run()