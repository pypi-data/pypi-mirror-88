from io import StringIO
import requests as rq
import pandas as pd
from ipyauth import Auth, ParamsAuth0

import json
import requests as rq

from ipyauth import Auth, ParamsAuth0

#BASE_URL = "http://localhost:5000"
#BASE_URL = 'https://tingkart-api.herokuapp.com'
#BASE_URL = 'https://tingkart.azurewebsites.net'
BASE_URL = 'https://tingkart-app.azurewebsites.net'

def get_current_dataframe():
    return df

def login():
    from ipyauth import ParamsAuth0, Auth
    p = ParamsAuth0(
        response_type='token id_token', 
        domain='sysfrog.eu.auth0.com',
        client_id='uk16k1vZGfY9CQeOGrI6kl22a80zKb30',
        audience='api/fruit',
        redirect_uri='http://localhost:8888/callback',
        scope='profile openid mail write:usual-fruit read:exotic-fruit')

    a = Auth(params=p)

    return a

def get_map(a, point_of_interest, km_from_poi ):
    from ipyleaflet import Map, basemaps, basemap_to_tiles, Circle, Marker
    from ipywidgets import Layout

    m = Map(center=[point_of_interest[0], point_of_interest[1]], zoom=13)
    m = Map(basemap=basemaps.OpenStreetMap.BlackAndWhite, scroll_wheel_zoom=True, center=[point_of_interest[0], point_of_interest[1]], zoom=9,
        layout=Layout(width='100%', min_height='600px'))

    circle = Circle()
    circle.location = point_of_interest
    circle.radius = int(km_from_poi * 1000)
    circle.color = "green"
    circle.fill_color = "green"

    sensors = all_sensors_in_radius(a, point_of_interest, km_from_poi )

    m.add_layer(circle)
    return m, sensors

def get_measurements(a, from_date, to_date, resolution, sensor_id, measurements):
    url = BASE_URL + '/api/measurements/{}/{}/{}/{}/{}'.format(from_date, to_date, resolution, sensor_id, measurements)

    headers = {'Authorization': 'Bearer {}'.format(a.access_token)}

    req = rq.get(url, headers=headers)

    data = StringIO(req.text)
    data = pd.read_csv(data)

    return data

def get_environments(a, object_id): 
    url = BASE_URL + '/api/environment_types/{}'.format(object_id)

    headers = {'Authorization': 'Bearer {}'.format(a.access_token)}

    req = rq.get(url, headers=headers)

    data = StringIO(req.text)
    data = pd.read_csv(data)

    return data


def get_observations(a, from_date, to_date, resolution, object_id, measurements):
    # Resolution = time scale/bucket (eg. 1 hours time scale, 3 hours time scale or 1 days time scale)
    url = BASE_URL + '/api/observations/{}/{}/{}/{}/{}'.format(from_date, to_date, resolution, object_id, measurements)

    headers = {'Authorization': 'Bearer {}'.format(a.access_token)}

    req = rq.get(url, headers=headers)

    data = StringIO(req.text)
    data = pd.read_csv(data,index_col=0)

    return data

def get_observation_types(a, object_id):
    url = BASE_URL + '/api/observation_types/{}'.format( object_id )

    headers = {'Authorization': 'Bearer {}'.format(a.access_token)}

    req = rq.get(url, headers=headers)

    #data = StringIO(req.text)

    #data = pd.read_csv(data,index_col=0)

    return req.json()

def all_sensors_in_radius(a, point_of_interest, km_from_poi ):

    lat, lng = point_of_interest
    url = BASE_URL + '/api/sensors/{}/{}/{}'.format(lat, lng, km_from_poi)

    headers = {'Authorization': 'Bearer {}'.format(a.access_token)}

    req = rq.get(url, headers=headers)
    data = StringIO(req.text)

    data = pd.read_csv(data,index_col=0)

    return data


def get_all_sensors(a):
    url = BASE_URL + '/api/sensors'

    headers = {'Authorization': 'Bearer {}'.format(a.access_token)}

    req = rq.get(url, headers=headers)
    data = req.json()
    #data = StringIO(req.text)

    #data = pd.read_csv(data,index_col=0)

    return data

def get_sensor_id(a, object_id):
    url = BASE_URL + '/api/sensors/{}'.format(object_id)
    headers = {'Authorization': 'Bearer {}'.format(a.access_token)}

    req = rq.get(url, headers=headers)
    return req

def get_measurement_types(a, sensor_id):

    url = BASE_URL + '/api/measurement_types/{}'.format(sensor_id)

    headers = {'Authorization': 'Bearer {}'.format(a.access_token)}

    req = rq.get(url, headers=headers)
    data = StringIO(req.text)

    data = pd.read_csv(data,index_col=0)

    return data
