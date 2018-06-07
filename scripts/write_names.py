import json


with open("viruses.json", "r") as f:    
    names = sorted([virus["name"] for virus in json.load(f)])

with open("names.txt", "w") as f:
    f.write("\n".join(names))
