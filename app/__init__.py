from flask import Flask
from flask_migrate import Migrate
from .database import db
from .auth_routes import auth

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'TheBestTeachinMdule' 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main
    from .course_routes import courses
    from .material_routes import materials

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(courses, url_prefix='/courses')
    app.register_blueprint(materials, url_prefix='/materials')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
