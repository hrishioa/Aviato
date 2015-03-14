from app import application
from flask import render_template, flash, redirect, url_for, request, Response
from datetime import datetime

@application.route("/", methods=["GET", "POST"])
@application.route("/index", methods=["GET", "POST"])
def index():

    return render_template("index.html")

