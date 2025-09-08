import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models.user import db
from src.routes.auth import auth_bp
from src.routes.dogs import dogs_bp
from src.routes.walks import walks_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "super-secret-key")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key")

CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(dogs_bp, url_prefix="/api")
app.register_blueprint(walks_bp, url_prefix="/api")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Backend is healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


