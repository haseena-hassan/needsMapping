from flask import Flask, render_template, request
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
import flask
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import send_file


pd.pandas.set_option('display.max_columns', None)
data= pd.read_csv('./CitizenNeeds.csv')


@app.route('/')
def hello():
    return "Hello haseena"

@app.route('/map.html')
def show_map():
    data= pd.read_csv('./CitizenNeeds.csv')
    Rest_locations= pd.read_csv('./Rest_locations.csv')
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
    plt.figure(figsize=(6,3))
    chains=data['Basic Need'].value_counts()
    sns.barplot(x=chains,y=chains.index,palette='rocket')
    plt.title("Density plot of Basic Need in Kerala")
    plt.xlabel("Number of citizens opted")
    plt.savefig('./plot-basic.png')
    return send_file('./plot-basic.png', mimetype='image/png')

@app.route('/barplot-standard')
def get_image2():
    plt.figure(figsize=(6,3))
    chains=data['Standard Need'].value_counts()
    sns.barplot(x=chains,y=chains.index,palette='rocket')
    plt.title("Density plot of Standard Need in Kerala")
    plt.xlabel("Number of citizens opted")
    plt.savefig('./plot-standard.png')
    return send_file('./plot-standard.png', mimetype='image/png')

@app.route('/barplot-premium')
def get_image3():
    plt.figure(figsize=(6,3))
    chains=data['Premium Need'].value_counts()
    sns.barplot(x=chains,y=chains.index,palette='rocket')
    plt.title("Density plot of Premium Need in Kerala")
    plt.xlabel("Number of citizens opted")
    plt.savefig('./plot-premium.png')
    return send_file('./plot-premium.png', mimetype='image/png')


# @app.route('/<name>')
# def hello_name(name):
#     plt.figure()
#     chains=data['Basic Need'].value_counts()
#     sns.barplot(x=chains,y=chains.index,palette='rocket')
#     plt.title("Density plot of Basic Need in Kerala")
#     plt.xlabel("Number of citizens opted")
#     plt.show()
#     return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()