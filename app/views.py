from app import application
from flask import render_template, flash, redirect, url_for, request, Response
from datetime import datetime
from kartograph import Kartograph
from .forms import SearchForm
import json
import os
import httplib2
import pycountry
from aviato import *

#Used as the filtering function
def southeastAsia(record):
    thai = record['ISO_3_CODE'] == "THA"
    viet = record['ISO_3_CODE'] == "VNM"
    phil = record['ISO_3_CODE'] == "PHL"
    khm = record['ISO_3_CODE'] == "KHM"
    lao = record['ISO_3_CODE'] == "LAO"
    mys = record['ISO_3_CODE'] == "MYS"
    sgp = record['ISO_3_CODE'] == "SGP"
    idn = record['ISO_3_CODE'] == "IDN"

    return thai | viet | phil | khm | lao | mys | sgp | idn

#Generate the svg file
def generate():
    path = os.path.dirname(os.path.realpath(__file__))
    script_dir = os.path.dirname(__file__)
    rel_path="c:/users/seansaito/dev/aviato/app/sample/world_countries_boundary_file_world_2002.shp"
    abs_path = os.path.join(script_dir, rel_path)
    d = {
        "layers":{
            "world": {
                "src": rel_path,
                "simplify": 2,
                "attributes" : {
                        "iso3":"ISO_3_CODE"
                },
                "filter": ["ISO_3_CODE", "in", ["PHL", "MYS", "THA", "VNM", "LAO", "SGP", "IDN", "KHM", "BRN", "TLS", "MMR"]]
            }
        }
    }
    K = Kartograph()
    K.generate(d, outfile=os.path.dirname(os.path.realpath(__file__)) + "\static\\resources\sea.svg")


@application.route("/", methods=["GET", "POST"])
@application.route("/index", methods=["GET", "POST"])
def index():
    #json_data = open(os.path.dirname(os.path.realpath(__file__)) + "\worldconfig.json")
    #d = json.load(json_data)
    #generate()
    #get_from_json("CAAMUZAqD4ZBJgBAEpEY5itDis0NgxV3fGrDOWxNAvlYrj3xdPtxmsJ9pS9DegCeZBqhx47sLZBccVlXlx4pfsslIN3f7v0ZBRXmjYUrva1yT5dJsiZCrgAMbzzRmhZBXEqi4cZAoNvAZC1ZBZAQbgVZC6k8nZAAJiK0HekhhLPgiSKZBPzczlEvQzGR93Wbv1q6lgYJLt3rmaPYFl4Jnf2wmS0tMOAk9rK6FZAm0qxfkXbBLNBZC52nqudLcTHZCQ")
    form = SearchForm()
    if form.validate_on_submit():
        if (form.search.data.lower() == "east asia") | (form.search.data.lower() =="eastasia") | (form.search.data.lower() == "ea"):
            return render_template("index.html", form=form, mapid="east asia")
        elif form.search.data.lower() == "age":
            return render_template("index.html", form=form, mapid="age")
        else:
            return render_template("index.html", form=form, mapid="world")
    if request.method == "POST":
        fb_token = request.json["token"]
        if str(fb_token) == "CAAMUZAqD4ZBJgBAEpEY5itDis0NgxV3fGrDOWxNAvlYrj3xdPtxmsJ9pS9DegCeZBqhx47sLZBccVlXlx4pfsslIN3f7v0ZBRXmjYUrva1yT5dJsiZCrgAMbzzRmhZBXEqi4cZAoNvAZC1ZBZAQbgVZC6k8nZAAJiK0HekhhLPgiSKZBPzczlEvQzGR93Wbv1q6lgYJLt3rmaPYFl4Jnf2wmS0tMOAk9rK6FZAm0qxfkXbBLNBZC52nqudLcTHZCQ":
            get_from_json(fb_token)
    return render_template("index2.html", form=form, mapid="world")

@application.route("/fb", methods=["GET", "POST"])
def fb():
    return render_template("fb_login.html")

@application.route("/token", methods=["GET", "POST"])
def token():
    if request.method == "POST":
        fb_token = request.params("token")
        get_from_json(fb_token)
        return render_template("token.html", token=fb_token)
    return redirect(url_for("index"))

def update_json(iso_code):
    data = ""
    script_dir = os.path.dirname(__file__)
    rel_path="static/resources/popularity.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "rb") as fp:
        data = json.load(fp)
        fp.close()

    if iso_code in data:
        data[iso_code]["popularity"] += 100
    else:
        data[iso_code] = {"popularity": 100}
    jsonFile=open(abs_file_path, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()
    return True

def get_from_json(token):
    #Using aviato.py
    data = getLoc_and_Meta(token)
    visited = []
    for i in range(0, len(data)-1):
        if "country" in data[i]["location"]:
            if data[i]["location"]["country"] != "Singapore":
                country = pycountry.countries.get(name=data[i]["location"]["country"]).alpha3
                if country not in visited:
                    update_json(country)
                    visited.append(country)
        elif "longitude" in data[i]["location"]:
            lat = data[i]["location"]["latitude"]
            lng = data[i]["location"]["longitude"]
            req = "http://ws.geonames.org/countryCode?lat=" + str(lat)[0:7] + "&lng=" + str(lng)[0:7] + "&username=seansaito"
            if req != "":
                h = httplib2.Http(".cache")
                #Make request to geonames, with the latitude and longitude as parameters
                resp, content = h.request(req)
                #Get the alpha2 ISO country code
                content = content[0:len(content)-2]
                country = pycountry.countries.get(alpha2=content)
                #Convert to alpha3
                iso3 = country.alpha3
                if country not in visited:
                    update_json(iso3)
                    visited.append(country)
    return True
