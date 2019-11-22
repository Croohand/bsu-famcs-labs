import json
import os

from flask import render_template, request, send_file, abort
from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get-next-state', methods=['POST'])
def get_next_state():
    return request.get_json()


@app.route('/get-picture', methods=['GET'])
def get_picture():
    name = request.args.get('name')
    if name not in app.objects:
        abort(404)
    return send_file('../data/pictures/' + app.objects[name]['picture'])

