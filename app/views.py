from app import application
from flask import render_template, flash, redirect, url_for, request, Response
from datetime import datetime
from kartograph import Kartograph
import json
import os

@application.route("/", methods=["GET", "POST"])
@application.route("/index", methods=["GET", "POST"])
def index():
    json_data = open(os.path.dirname(os.path.realpath(__file__)) + "\worldconfig.json")
    d = json.load(json_data)
    K = Kartograph()
    K.generate(d, outfile=os.path.dirname(os.path.realpath(__file__)) + "\world_from_views.svg")
    return render_template("index.html")
