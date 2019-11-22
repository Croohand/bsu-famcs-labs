import json

from flask import Flask


app = Flask(__name__)
with open('data/features.json', 'r') as f:
    app.features = json.load(f)
with open('data/implications.json', 'r') as f:
    app.implications = json.load(f)
with open('data/objects.json', 'r') as f:
    app.objects = json.load(f)


from app import routes
