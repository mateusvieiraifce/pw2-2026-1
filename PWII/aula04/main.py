from flask import Flask, render_template, request
import math
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("mysql+pymysql://root:@localhost/pw2")
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Usuario(Base):
    __tablename__ ='usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(10), nullable = False)
    senha = Column(String(10), nullable = False)
    nome = Column(String(50), nullable = False)
Base.metadata.create_all(engine)

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

@app.route("/user/new")
def new_user():
    return render_template("newuser.html")

@app.route("/user/save", methods=["POST"])
def save_user():
    session = Session()
    nome = request.form.get("nome")
    senha = request.form.get("senha")
    login = request.form.get("login")
    user = Usuario()
    user.nome = nome
    user.senha = senha
    user.login = login
    session.add(user)
    session.commit()

    return render_template("newuser.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session = Session()
    a = request.form.get("nome")
    b = request.form.get("senha")
    user = session.query(Usuario).filter(Usuario.login==a,
     Usuario.senha==b).first()
    print(user)
    if user:
        return render_template("dashboard.html")
    else:
        return render_template("index.html", error="Credenciais inválidas")

if ( __name__ == "__main__"):
    app.run(debug=True, port=5001)