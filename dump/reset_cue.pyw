import json, os

scriptsdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(scriptsdir)
JSON_PATH = os.path.join(scriptsdir, "common", "data.json")
print(JSON_PATH)
with open(JSON_PATH, 'r') as j:
    jsondata = json.load(j)
jsondata['values']["which_DS"] = False

with open(JSON_PATH, 'w') as j:
    json.dump(jsondata,j,indent=4)
