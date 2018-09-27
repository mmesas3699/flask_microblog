from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config

# Instancia de la aplicación
app = Flask(__name__)

# Objeto de configuración
app.config.from_object(Config)

# Base de datos
db = SQLAlchemy(app)

# Migraciones
migrate = Migrate(app, db)

# Login
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
