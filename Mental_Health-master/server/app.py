# from flask import Flask
# from extensions import db, bcrypt, jwt
# from flask_migrate import Migrate
# from models.user import User
# from auth import auth_bp  # Import the auth blueprint
# import os

# # Initialize the Migrate object
# migrate = Migrate()

# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'app.db')}"
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['JWT_SECRET_KEY'] = 'super-secret-key'

#     # Initialize extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
#     bcrypt.init_app(app)
#     jwt.init_app(app)

#     # Register blueprints
#     app.register_blueprint(auth_bp)  # Register the auth blueprint

#     # Define routes directly in the app
#     @app.route('/')
#     def home():
#         return "Hello, Flask!"
#     @app.route('/about')
#     def about():
#         return "This is the About page!"

#     @app.route('/contact')
#     def contact():
#         return "This is the Contact page!"

#     @app.route('/test')
#     def test():
#         return "This is the Test page!"

#     @app.route('/sign_up')
#     def sign_up():
#         return "This is the Sign Up page!"

#     @app.route('/success')
#     def success():
#         return "You have successfully signed up!"

#     @app.route('/appointment')
#     def appointment():
#         return "This is the Appointment page!"

#     @app.route('/journal')
#     def journal():
#         return "This is the Journal page!"

#     @app.route('/mood')
#     def mood():
#         return "This is the Mood page!"

#     @app.route('/treatment')
#     def treatment():
#         return "This is the Treatment page!"

#     @app.route('/message')
#     def message():
#         return "This is the Message page!"

#     @app.route('/testimonials')
#     def testimonials():
#         return "This is the Testimonials page!"

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(port = 5555, debug=True)


from flask import Flask
from extensions import db, bcrypt, jwt
from flask_migrate import Migrate
from models.user import User
from auth import auth_bp  # Import the auth blueprint
from treatment_route import treatment_bp #import the treatment blueprint

import os

# Initialize the Migrate object
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)  # Register the auth blueprint
    app.register_blueprint(treatment_bp)  # Register the treatment blueprint
    

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

