from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import pyodbc

db = SQLAlchemy()

# DB_USERNAME = "DESKTOP-1HCAB3I"
# DB_DATABASE = "BrainBuster"

DB_USERNAME = "raspberry"
DB_PASSWORD = "123321123"
DB_SERVER = " 192.168.178.79,1433"
DB_DATABASE = "BrainBuster"




def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://{DB_USERNAME}/{DB_DATABASE}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Questions, Variants
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app