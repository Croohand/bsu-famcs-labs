import json
import os
import random

from flask import render_template, request, send_file, abort
from app import app


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


def get_suitable_objects(state):
    suitable = []
    for name, desc in app.objects.items():
        obj_features = desc['features']
        good = True
        for feature, answer in state['features'].items():
            obj_answer = obj_features.get(feature, app.features[feature]['values'][-1])
            if answer != obj_answer:
                good = False
        if good:
            suitable.append(name)
    return suitable


def enrich_features(state):
    for impl in app.implications:
        good = True
        for feature, value in impl['if'].items():
            if state['features'].get(feature) != value:
                good = False
        if good:
            for feature, value in impl['then'].items():
                if state['features'].get(feature, value) != value:
                    state['failed'] = True
                state['features'][feature] = value


@app.route('/get-next-state', methods=['POST'])
def get_next_state():
    state = request.get_json(force=True)
    state['status'] = 'playing'
    enrich_features(state)
    objects = get_suitable_objects(state)
    if not objects:
        state['failed'] = True
    else:
        unknown_features = [feature for feature in app.features if feature not in state['features']]
        if len(objects) == 1 and len(unknown_features) < 5:
            state['status'] = 'win'
            state['message'] = f'Это {objects[0]}!'
            state['result'] = objects[0]
        else:
            feature = random.choice(unknown_features)
            state['currentFeature'] = feature
            state['currentQuestion'] = app.features[feature]['question']
            state['currentValues'] = app.features[feature]['values']
            state['currentReprs'] = app.features[feature]['values_repr']
    if 'failed' in state:
        state['status'] = 'lose'
        state['message'] = 'Не знаю, что это может быть.'
    return json.dumps(state)


@app.route('/get-picture', methods=['GET'])
def get_picture():
    name = request.args.get('name')
    if name not in app.objects:
        abort(404)
    return send_file('../data/pictures/' + app.objects[name]['picture'])

