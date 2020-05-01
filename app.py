from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from flask_session import Session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import datetime

app = Flask(__name__)
app.secret_key = 'wqertfy23456(&|^%-'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'diary'

# app.config['MYSQL_CHARSET'] = 'utf-8'

mysql = MySQL(app)

auth = Blueprint('auth', __name__)


# cur = mysql.connection.cursor()
# cur.connection.autocommit(True)

@app.route('/', methods=['POST', 'GET'])
def index():
    cur = mysql.connection.cursor()
    cur.connection.autocommit(True)
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    msg = ' '
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # create variable
        username = request.form['username']
        password = request.form['password']
        # check if user exists in mysql
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        # fetch one record and return result
        user = cursor.fetchone()
        if user:
            # create session data to be accesses in other routes
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            # redirect to home page
            date = str(datetime.date.today())
            return redirect(url_for('diary', date=date))
            # return  render_template('diary.html')
        else:
            msg = 'Incorrect Username/Password'
    return render_template('login.html', msg=msg)

    # cur = mysql.connection.cursor()
    # cur.execute(''' CREATE TABLE user ( id INTEGER , username VARCHAR(20) , email VARCHAR(20), password VARCHAR(20))''')
    # insert some data
    # mysql.connect.commit
    # do a mysql.connection
    # results = cur.fetchall()
    # cur.close()


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        sql = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
        val = (email, username, password)
        cur.execute(sql, val)
        # cur.execute( ' INSERT INTO users (email,username,password) VALUES (%s,%s,%s)'  % (email,username, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/diary', methods=['POST', 'GET'])
# @auth.route('/diary', methods=['POST', 'GET'])
# @login_required
def diary():
    # to call this endpoint, a date is required to fetch entries for that date
    date = request.args.get('date')
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            memory = request.form['memory']
            tag = request.form['tag']
            updated_at = ""
            cur = mysql.connection.cursor()
            # save diary entries to database
            sql = "INSERT INTO entries (entries, tag, created_at,updated_at,UserId) VALUES (%s, %s, %s, %s, %s)"
            val = (memory, tag, str(datetime.datetime.now()), updated_at, session['id'])
            cur.execute(sql, val)
            # add to memory database
            mysql.connection.commit()

            # fetch all diary entries for the date selected on the calender
            cur.execute('SELECT * FROM entries WHERE UserId = %s AND created_at >= %s', (session['id'], date))
            entries = cur.fetchall()  # entries should be a list of entry objects
            cur.close()
            print(session['id'])
            print(entries)
            return render_template('diary.html', entries=entries, username=session['username'])

        else:
            # fetch all diary entries for the date selected on the calender
            cur.execute('SELECT * FROM entries WHERE UserId = %s AND created_at >= %s', (session['id'], date))
            records = cur.fetchall()  # entries should be a list of entry objects
            cur.close()
            entries = []
            for row in records:
                entries.append(
                    {"id": row[0],
                     "entry": row[1],
                     "tag": row[2],
                     "date": str(row[3]),
                     "user_id": row[3]}
                )
            return render_template('diary.html', entries=entries, username=session['username'])

    # User is not logged in redirect to login page
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    # session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
