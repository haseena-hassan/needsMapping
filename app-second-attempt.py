from flask import Flask, render_template, request, Response, jsonify, send_file
app = Flask(__name__, static_url_path='')

import numpy as np  
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.geocoders import Nominatim
import folium
import webbrowser
import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from geopy.exc import GeocoderTimedOut

def do_geocode(address, attempt=1, max_attempts=5):
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return do_geocode(address, attempt=attempt+1)
        raise

data= pd.read_csv('./CitizenNeeds.csv')
locations= pd.read_csv('./locations.csv')

map_data = pd.DataFrame(data['District'].value_counts().reset_index())
map_data.columns=['District','count']
map_data=map_data.merge(locations,on='District',how="left").dropna()
print(map_data)
lat,lon=zip(*np.array(map_data['geo_loc']))
map_data['lat'], map_data['lon'] =lat, lon
need, count = [[], [], []], [[], [], []]
districts = data['District']
for i in map_data['District']:
    val = districts.str.contains(i)
    basic = data[val]['Basic Need'].value_counts()
    need[0].append(basic.index[0])
    count[0].append(float(basic[0]))
    standard = data[val]['Standard Need'].value_counts()
    need[1].append(standard.index[0])
    count[1].append(float(standard[0]))
    premium = data[val]['Premium Need'].value_counts()
    need[2].append(premium.index[0])
    count[2].append(float(premium[0]))

map_data['basic'] = need[0]
map_data['std'] = need[1]
map_data['prm'] = need[2]
map_data['count_basic'] = count[0]
map_data['count_std'] = count[1]
map_data['count_prm'] = count[2]
map_data.to_csv('map_data.csv',index=False)

@app.route('/start')
def hello():

    return "Hello {}!".format("world")

@app.route('/post_survey', methods=['POST'])
def get_data():
    data = request.get_json()
    return "Survey updated", 201

@app.route('/get_dept')
def send_data():

    data = []
    return jsonify({'data' : data})




@app.route('/map.html')
def show_map():
    data= pd.read_csv('./CitizenNeeds.csv')
    Rest_locations= pd.read_csv('./map_data.csv')
    data = pd.DataFrame({
    'lat':Rest_locations['lat'],
    'lon':Rest_locations['lon'],
    'name':Rest_locations['Name'],
    'value_b':Rest_locations['count_basic'],
    'value_s':Rest_locations['count_std'],
    'value_p':Rest_locations['count_prm'],
    'basic':Rest_locations['basic'],
    'std':Rest_locations['std'],
    'prm':Rest_locations['prm']
    })
    m = folium.Map(location=[10.8505, 76.2711], tiles="OpenStreetMap", zoom_start=6)
    for i in range(0,len(data)):
        folium.Circle(
            location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
            popup=data.iloc[i]['name'] + ' : ' + data.iloc[i]['basic'],
            radius=data.iloc[i]['value_b']*1000,
            color='crimson',
            fill=True,
            fill_color='crimson'
        ).add_to(m)
        folium.Circle(
            location=[data.iloc[i]['lat']+0.2, data.iloc[i]['lon']+0.2],
            popup=data.iloc[i]['name'] + ' : ' + data.iloc[i]['std'],
            radius=data.iloc[i]['value_s']*500,
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(m)
        folium.Circle(
            location=[data.iloc[i]['lat'], data.iloc[i]['lon']+0.2],
            popup=data.iloc[i]['name'] + ' : ' + data.iloc[i]['prm'],
            radius=data.iloc[i]['value_p']*300,
            color='green',
            fill=True,
            fill_color='green'
        ).add_to(m)
    m.save('mymap.html')
    return m._repr_html_()

@app.route('/barplot-basic')
def get_image1():
    plt.figure(figsize=(15,8))
    chains=data['Basic Need'].value_counts()
    sns.barplot(x=chains,y=chains.index,palette='rocket')
    plt.title("Density plot of Basic Need in Kerala")
    plt.xlabel("Number of citizens opted")
    plt.savefig('./plot-basic.png')
    return send_file('./plot-basic.png', mimetype='image/png')

@app.route('/barplot-standard')
def get_image2():
    plt.figure(figsize=(15,8))
    chains=data['Standard Need'].value_counts()
    sns.barplot(x=chains,y=chains.index,palette='rocket')
    plt.title("Density plot of Standard Need in Kerala")
    plt.xlabel("Number of citizens opted")
    plt.savefig('./plot-standard.png')
    return send_file('./plot-standard.png', mimetype='image/png')

@app.route('/barplot-premium')
def get_image3():
    plt.figure(figsize=(15,8))
    chains=data['Premium Need'].value_counts()
    sns.barplot(x=chains,y=chains.index,palette='rocket')
    plt.title("Density plot of Premium Need in Kerala")
    plt.xlabel("Number of citizens opted")
    plt.savefig('./plot-premium.png')
    return send_file('./plot-premium.png', mimetype='image/png')



if __name__ == '__main__':
    app.run()
