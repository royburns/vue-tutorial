# encoding: utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_jwt import JWT
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# models引用必须在 db/login_manager之后，不然会循环引用
from .models import User

def authenticate(username, password):
    print 'JWT auth argvs:', username, password
    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        return user
def identity(payload):
    print 'JWT payload:', payload
    user_id = payload['identity']
    user = User.query.filter_by(id=user_id).first()
    return user_id if user is not None else None
jwt = JWT(authentication_handler=authenticate, identity_handler=identity)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
