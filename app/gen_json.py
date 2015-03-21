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


#This generates a json file that is similar to the one used for the 3D example in Kartograph
#Loading json file with longitude/latitude data for each country, reprsented with alpha2 code
ll_data = ""
with open("app/countrycode-latlong-array.json", "rb") as fp:
    ll_data = json.load(fp)
    fp.close()

data_2 = []
jsonFile = open("app/static/resources/sea_data_3d.json", "w+")

for country in sea_countries:
    popularity = float(str(random.uniform(100, 500))[0:6])
    age = float(str(random.uniform(16, 30))[0:5])
    entry = {
        "Country": pycountry.countries.get(name=country).alpha3,
        "ll": ll_data[pycountry.countries.get(name=country).alpha2.lower()],
        "Popularity2013": popularity,
        "Popularity2012": popularity + float(str(random.uniform(-50, 50))[0:5]),
        "Age2013": age,
        "Age2012": age + float(str(random.uniform(-5, 5))[0:4])
    }
    data_2.append(entry)

jsonFile.write(json.dumps(data_2))
jsonFile.close()
