from kartograph import Kartograph

def myfilter(record):
    return record["ISO"] == "FRA"

cfg = {
        "layers": {
            "mylayer": {
                "src": "countries.shp",
                "filter": myfilter
             }
        },
        
        "bounds": {
           "mode": "bbox", 
            "data": [70, 17, 135, 54]
        }
}
}

K = Kartograph()
K.generate(cfg, output="mymap.svg")

