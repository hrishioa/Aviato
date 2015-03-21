import pycountry
import json
import random

#Generate random json file with random values for countries in southeast asia

sea_countries = [
    "Philippines",
    "Malaysia",
    "Timor-Leste",
    "Indonesia",
    "Brunei Darussalam",
    "Singapore",
    "Cambodia",
    "Lao People's Democratic Republic",
    "Myanmar",
    "Thailand",
    "Malaysia",
    "Viet Nam"
]

data = {}
jsonFile = open("app/static/resources/sea_data.json", "w+")

for country in sea_countries:
    iso3 = pycountry.countries.get(name=country).alpha3
    data[iso3] = {"popularity" : float(str(random.uniform(100, 500))[0:6])}
    data[iso3]["age"] = float(str(random.uniform(16, 30))[0:5])

jsonFile.write(json.dumps(data))
jsonFile.close()
