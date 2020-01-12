from flask import Flask, render_template,request,redirect

app = Flask(__name__ ,  static_url_path='/static')
@app.route('/', methods=['POST','GET'])
def index():
        return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def login():
        return render_template('login.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
        return render_template('signup.html')

@app.route('/diary', methods=['POST','GET'])
def diary():
        return render_template('diary.html')


if __name__ == "__main__":
    app.run(debug=True)