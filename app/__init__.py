from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    ma.init_app(app)

    #ToDo: Import routes after initializing db and ma
    from .routes import bp as api_bp
    app.register_blueprint(api_bp)


    with app.app_context():
        from . import routes  # Import routes to register them
        db.create_all()  # Create database tables

    return app