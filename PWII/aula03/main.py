from flask import Flask, render_template, request
import math
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/listprodutos")
def listprodutos():
    return render_template("listprodutos.html")

@app.route("/cadprodutos")
def cadprodutos():
    return render_template("cadproduto.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    a = request.form.get("nome")
    b = request.form.get("senha")
    if a == "admin" and b == "admin":
        return render_template("dashboard.html")
    else:
        return render_template("index.html", error="Credenciais inválidas")

if ( __name__ == "__main__"):
    app.run(debug=True, port=5001)