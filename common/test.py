import json

with open("data.json",'w') as fd:
    json.dump({"folder_dirs":{}},fd)