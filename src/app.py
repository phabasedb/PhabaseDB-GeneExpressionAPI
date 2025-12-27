from flask import Flask
from flask_cors import CORS
from src.gene.routes.routes import expression_bp 
from src.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(expression_bp , url_prefix="/expression")
    return app
