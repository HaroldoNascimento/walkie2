import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdf#FGSgvasgf$5$WGT"
CORS(app, origins="*")

@app.route("/api/test", methods=["GET"])
def test_route():
    return jsonify({"message": "Backend está funcionando!"}), 200

@app.route("/api/login", methods=["POST"])
def login():
    return jsonify({"message": "Login realizado com sucesso!", "user": {"id": 1, "email": "teste@walkie.com"}}), 200

@app.route("/api/register", methods=["POST"])
def register():
    return jsonify({"message": "Usuário registrado com sucesso!", "user": {"id": 1, "email": "teste@walkie.com"}}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5008)


