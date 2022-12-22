from flask_app import app
from flask_app.controllers import users_controller, places_controller

if __name__ == "__main__":
    app.run(debug=True) #this runs the app initialized in our init