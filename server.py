from flask_app import app
from flask_app.controllers import users_controller, places_controller


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)