import os

from flask import render_template, Flask

app = Flask(__name__)

@app.route("/")
def index():
    nome  = 'SOSanimais.com.br'
    return render_template('index.html', site = nome)

@app.route("/login")
def login():
    return render_template("login/login.html")

@app.route("/login/orgaos")
def login_orgaos():
    return render_template("login/loginorgao.html")

@app.route("/register")
def register():
    return render_template("login/register.html")

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()