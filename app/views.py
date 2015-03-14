from app import application
from flask import render_template, flash, redirect, url_for, request, Response
from datetime import datetime
from kartograph.kartograph import Kartograph
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
    d = {
        "layers":{
            "world": {
                "src": "world_countries_boundary_file_world_2002.shp",
                "simplify": 2,
                "attributes" : {
                        "iso3":"ISO_3_CODE"
                },
                "filter": ["ISO_3_CODE", "in", ["JPN", "CHN", "KOR", "VNM"]]
            }
        }
    }
    K = Kartograph()
    K.generate(d, outfile=os.path.dirname(os.path.realpath(__file__)) + "\static\\resources\world_from_views.svg")


@application.route("/", methods=["GET", "POST"])
@application.route("/index", methods=["GET", "POST"])
def index():
    #json_data = open(os.path.dirname(os.path.realpath(__file__)) + "\worldconfig.json")
    #d = json.load(json_data)
    #generate()
    form = SearchForm()
    if form.validate_on_submit():
        if (form.search.data.lower() == "southeast asia") | (form.search.data.lower() =="southeastasia") | (form.search.data.lower() == "sea"):
            return render_template("index.html", form=form, mapid="sea")

    return render_template("index.html", form=form, mapid="world")

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

def get_from_json():
    #Using aviato.py
    data = getLoc_and_Meta()
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
