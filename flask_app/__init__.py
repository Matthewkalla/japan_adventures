from flask import Flask
import os

API_KEY = os.getenv("API_KEY")
DATABASE = os.getenv("DATABASE")
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

