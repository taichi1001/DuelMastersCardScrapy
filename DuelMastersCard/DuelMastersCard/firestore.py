import json
import os

import firebase_admin
from firebase_admin import credentials, firestore

jsns = {}
with open("./output.json", encoding="utf-8") as f:
    jsns = json.load(f)

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "./sealed-deck-generator-firebase-adminsdk-31hvy-5babb988bb.json"

cred = credentials.Certificate("./sealed-deck-generator-firebase-adminsdk-31hvy-5babb988bb.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

for jsn in jsns:
    doc_ref = db.collection("card").document(jsn["name"][0])
    doc_ref.set(
        {
            "cards": jsn["cards"],
            "collections": jsn["collections"],
            "name": jsn["name"][0],
        }
    )
