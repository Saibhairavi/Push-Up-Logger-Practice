from flask import Flask

#to initialize db
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

from flask_login import LoginManager


def create_app():
    app=Flask(__name__)
    app.config['SECRETE_KEY']='secrete_key'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    db.init_app(app)

    #initialize ligin manager
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    
    #initialize userloader
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from pushups_logger.main import main as main_blueprint
    #FROM MAIN.PY IMPORT BLUEPRINT AND REGISTER IT
    app.register_blueprint(main_blueprint)

    from pushups_logger.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #registr blue print so we can run main.py
    return app