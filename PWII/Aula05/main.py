from flask import Flask, render_template, request
import math
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from weasyprint import HTML, CSS
from sqlalchemy.exc import DataError, PendingRollbackError

engine = create_engine("mysql+pymysql://root:root@localhost/pw2")
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Usuario(Base):
    __tablename__ ='usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(20), nullable = False)
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

@app.route("/user/update/<int:id>")
def update_user(id):
    session = Session()
    user = session.query(Usuario).filter(Usuario.id == id).first()
    return render_template("updateuser.html", user=user)

@app.route("/user/delete/<int:id>" , methods=["GET"])
def delete_user(id):
    session = Session()
    user = session.query(Usuario).filter(Usuario.id == id).first()
    session.delete(user)
    session.commit()
    return list_user(msg="Usuário deletado com sucesso!");
 
@app.route("/user/update", methods=["POST"])
def update_user_do():
    try:
        session = Session()
        id = request.form.get("id");
        nome = request.form.get("nome")
        senha = request.form.get("senha")
        login = request.form.get("login")

        user = session.query(Usuario).filter(Usuario.id == id).first()
        user.nome = nome
        user.senha = senha
        user.login = login
        session.commit()
        return list_user(msg="Usuário atualizado com sucesso!");
    except DataError as e:
        print("Erro de transação pendente. Realizando rollback.")
        session.rollback()
    except PendingRollbackError  as e:
        print("Erro de transação pendente. Realizando rollback.")
    return render_template("updateuser.html", user=user, error="Dados inválidos. Por favor, tente novamente.")

@app.route("/user/list")
def list_user(msg=None):
    list = Session().query(Usuario).all();
    return render_template("userlist.html", list=list, msg=msg)

@app.route("/user/save", methods=["POST"])
def save_user():
    msg = None
    try:
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
        msg = "Usuário cadastrado com sucesso!"
    except DataError as e:
        msg = "Erro ao cadastrar usuário. Verifique os dados e tente novamente."
        session.rollback()
    except PendingRollbackError  as e:
        msg = "Erro ao cadastrar usuário. Verifique os dados e tente novamente."
    return render_template("newuser.html", error=msg)

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