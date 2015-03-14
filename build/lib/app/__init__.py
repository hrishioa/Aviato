from flask import Flask

application == Flask(__name__)

if __name__ == "__main__":
    application.run(host="0.0.0.0")

#Last line to avoid import errors
#No models in this project
from app import views
