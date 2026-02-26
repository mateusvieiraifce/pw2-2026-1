from flask import Flask, render_template, request
import math
app = Flask(__name__)

@app.route("/")
def index():
    return "ola mundo"

@app.route("/soma/<a>/<b>")
def soma(a, b):
    try:
        a1 = float(a)
        b1 = float(b)
        return "a soma é:" + str(a1+b1)
    except :
        return "a soma é:" + str(a+b)

@app.route("/imc",methods=['POST'])
def imc():
    try:
        a1 = float(request.form.get("peso"))
        b1 = float(request.form.get("altura"))
        imc = a1/(b1*b1)
        
        return render_template("home.html", imchtml=f"{imc:.2f}")
    except :
        return "nao oi possivel calcular o imc"

@app.route("/home")
def home():
    return render_template("home.html")

if ( __name__ == "__main__"):
    app.run(debug=True, port=500)