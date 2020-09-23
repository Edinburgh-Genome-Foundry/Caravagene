import json
from caravagene import ConstructList

with open("from_json.json", "r") as f:
    constructs_json = f.read()

constructs_dict = json.loads(constructs_json)
constructs = ConstructList.from_dict(constructs_dict)
constructs.to_pdf("from_json.pdf")
