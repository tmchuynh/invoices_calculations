from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import secrets

load_dotenv()  # Load environment variables

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Configure the SQLAlchemy part of the app
    db_url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.secret_key = os.getenv('SECRET_KEY') or secrets.token_hex(48)
    
    # Initialize SQLAlchemy and Flask-Migrate
    db.init_app(app)
    migrate = Migrate(app, db)
    
    def get_session():
        return db.session
            
    app.get_session = get_session
    
    # Register blueprints
    from flask_app.controllers.general_controller import bp as general_bp
    
    app.register_blueprint(general_bp)

    return app

def get_database_url():
    app = create_app()
    return app.config['SQLALCHEMY_DATABASE_URI']