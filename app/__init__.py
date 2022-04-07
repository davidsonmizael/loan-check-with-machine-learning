from flask import Flask
from core.database import db

def init_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../assets/credit_analysis_db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    with app.app_context():

        from app.blueprints import bp_credit_analysis

        app.register_blueprint(bp_credit_analysis, url_prefix='/api/ca/')

        db.init_app(app)
        db.create_all()
    
    return app