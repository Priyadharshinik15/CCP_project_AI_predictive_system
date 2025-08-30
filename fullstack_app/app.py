from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'some_random_secret_key'  # Change this to a strong, random key

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Priya@1'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'user_db'

mysql = MySQL(app)


@app.route("/")
def enter():
    return render_template("enter.html")

@app.route("/home")
def home():
    return render_template("home.html")

# ------------------ LOGIN / REGISTER ------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):  # user[3] = password
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            session['email'] = user[2]
            return redirect(url_for('predictive_form'))
        else:
            msg = 'Incorrect email/password!'
    
    return render_template('login.html', msg=msg)





@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s OR email = %s', (username, email))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not username or not password or not email:
            msg = 'Please fill out all fields!'
        else:
            cursor.execute(
                'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                (username, email, hashed_password)
            )
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out all fields!'
    return render_template('register.html', msg=msg)
def dashboard():
    return "<h1>Welcome to your Dashboard!</h1><p>You have successfully logged in.</p><p><a href='/'>Go back home</a></p>"


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/help")
def help():
    return render_template("help.html")



# ------------------ PATIENT FORM ------------------
@app.route('/predictive_form', methods=['GET', 'POST'])
def predictive_form():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        memory_loss = request.form['memory_loss']
        behaviour = request.form['behaviour']
        tremors = request.form['tremors']
        coordination = request.form['coordination']
        seizures = request.form['seizures']
        vision = request.form['vision']
        copper = request.form['copper']

        return render_template("result.html",
                               name=name, age=age, gender=gender,
                               memory_loss=memory_loss, behaviour=behaviour,
                               tremors=tremors, coordination=coordination,
                               seizures=seizures, vision=vision, copper=copper)
    return render_template("predictive_form.html")

@app.route('/logout')
def logout():
    # Clear the session (remove user data)
    session.clear()
    # Redirect back to login page
    return render_template("logout.html")



if __name__ == "__main__":
    app.run(debug=True)

 
