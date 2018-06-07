import pymongo


db = pymongo.MongoClient()["virtool"]

# Find viruses with changes.
agg = db.viruses.aggregate([
    {"$project": {
        "version": True,
        "last_indexed_version": True,
        "comp": {"$cmp": ["$version", "$last_indexed_version"]}
    }},
    {"$match": {
        "comp": {"$ne": 0}     
    }}
])

for item in agg:
    print(item)
    db.viruses.update_one({"_id": item["_id"]}, {
        "$set": {
            "last_indexed_version": item["version"]
        }
    })
