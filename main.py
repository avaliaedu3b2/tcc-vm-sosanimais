import os

from flask import render_template, Flask

app = Flask(__name__)


@app.route("/")
def index():
    nome = "SOSanimais.com.br"
    return render_template("index.html", site=nome)


@app.route("/login")
def login():
    return render_template("login/login.html")


@app.route("/login/orgaos")
def login_orgaos():
    return render_template("login/loginorgao.html")


@app.route("/register")
def register():
    return render_template("login/register.html")


@app.route("/dashboard")
def dashboard():
    nome = "SOSanimais.com.br"
    return render_template("dashboard/dashboard.html", site=nome)


def main():
    app.run(host="0.0.0.0", port = int(os.environ.get("PORT", 10000)))

# aha
   app.run(host="0.0.0.0", port = int(os.environ.get("PORT", 10000)))
if __name__ == "__main__":
    main()
