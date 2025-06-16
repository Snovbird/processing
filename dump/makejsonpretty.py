from common.common import select_anyfile
import json
import os
def makejsonpretty():
    thejsonpath = select_anyfile()

    with open(thejsonpath[0]) as file:
        thejson = json.load(file)

    with open(os.path.join(os.path.dirname(thejsonpath[0]),"formatted.json"),'w') as file:
        json.dump(thejson,file,indent=4)
    
if __name__ == "__main__":
    makejsonpretty()
