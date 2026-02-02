from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session  
from datetime import timedelta
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'Globalmindsindia@1439'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unified_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './.flask_session/'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    
    # PDF configuration
    try:
        import pdfkit
        path_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        app.config['PDFKIT_CONFIG'] = config
    except:
        app.config['PDFKIT_CONFIG'] = None
    
    Session(app)
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "https://calculator.globalmindsindia.com",
                "https://www.globalmindsindia.com",
                "http://localhost:3000"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    }, send_wildcard=False)
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
