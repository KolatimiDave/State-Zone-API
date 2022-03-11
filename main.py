from flask import  Flask, request, jsonify
from flask_restful import abort
import pandas as pd
import string


def string_clean(val):
    val = str(val.lower())
    val = val.translate(str.maketrans('', '', string.punctuation))
    val = val.replace(' ', '')
    return val

df = pd.read_csv('state_zone_mapping.csv')


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':

        return ({'data':df.sort_values(by=['State'])[['State','Zone']].values.tolist()})


@app.route('/state/<state>', methods=['GET'])
def state_map(state):
    state = string_clean(state)
    zone = df[df['state']==state]['Zone'].to_list()
    if len(zone)>0:
        zone = zone[0]
        return jsonify({'zone':zone})
    else:
        return abort(404)  


@app.route('/zone/<zone>', methods=['GET'])
def zone_map(zone):
    zone = string_clean(zone)
    states = df[df['zone']==zone]['State'].to_list()
    if len(states)>0:
        return jsonify({'states':states})
    else:
        return abort(404)
    


@app.route('/states', methods=['GET'])
def show_states():
    return jsonify({'states':df.State.unique().tolist()})

@app.route('/zones', methods=['GET'])
def show_routes():
    return jsonify({'zones':df.Zone.unique().tolist()})

if __name__ == '__main__':
  
    app.run(debug = True)
