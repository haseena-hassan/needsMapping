from flask import Flask, render_template, request, Response, jsonify, send_file
app = Flask(__name__, static_url_path='')
import numpy as np  
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.geocoders import Nominatim
import folium

data= pd.read_csv('./CitizenNeeds.csv')

############################################################################# FUNCTIONS


def basicbar():
    plt.figure(figsize=(15,8))
    chains=data['Basic Need'].value_counts()
    sns.barplot(x=chains,y=chains.index,palette='rocket')
    plt.title("Density plot of Basic Need in Kerala")
    plt.xlabel("Number of citizens opted")
    plt.savefig('./plot-basic.png')


def stdbar():
    plt.figure(figsize=(15,8))
    chains=data['Standard Need'].value_counts()
    sns.barplot(x=chains,y=chains.index,palette='rocket')
    plt.title("Density plot of Standard Need in Kerala")
    plt.xlabel("Number of citizens opted")
    plt.savefig('./plot-standard.png')
 

def prmbar():
    plt.figure(figsize=(15,8))
    chains=data['Premium Need'].value_counts()
    sns.barplot(x=chains,y=chains.index,palette='rocket')
    plt.title("Density plot of Premium Need in Kerala")
    plt.xlabel("Number of citizens opted")
    plt.savefig('./plot-premium.png')


# def build_map():



################################################################################ ROUTES


@app.route('/post_survey', methods=['POST'])
def get_data():
    data = request.get_json()                   #### TODO : create db with SqlAlchemy and restructure survey form
    return "Success", 201



@app.route('/get_dept')
def send_data():
    data = []
    return jsonify({'data' : data})



@app.route('/map.html')
def render_map():
    data= pd.read_csv('./CitizenNeeds.csv')
    locations=pd.DataFrame({"District":data['District'].unique()})
    locations['District']=locations['District'].apply(lambda x: "" + str(x))
    lat_lon=[]
    geolocator=Nominatim(user_agent="app")
    for location in locations['District']:
        location = geolocator.geocode(location)
        if location is None:
            lat_lon.append(np.nan)
        else:    
            geo=(location.latitude,location.longitude)
            lat_lon.append(geo)
    locations['geo_loc']=lat_lon
    locations.to_csv('locations.csv',index=False)

    map_data = pd.DataFrame(data['District'].value_counts().reset_index())
    map_data.columns=['District','count']
    map_data=map_data.merge(locations,on='District',how="left").dropna()
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



    m = folium.Map(location=[10.8505, 76.2711], tiles="OpenStreetMap", zoom_start=6)
    for i in range(0,len(map_data)):
        folium.Circle(
            location=[map_data.iloc[i]['lat'], map_data.iloc[i]['lon']],
            popup=map_data.iloc[i]['District'] + ' :\n' + map_data.iloc[i]['basic'],
            radius=map_data.iloc[i]['count_basic']*1000,
            color='crimson',
            fill=True,
            fill_color='crimson'
        ).add_to(m)
        folium.Circle(
            location=[map_data.iloc[i]['lat']+0.2, map_data.iloc[i]['lon']+0.2],
            popup=map_data.iloc[i]['District'] + ' :\n' + map_data.iloc[i]['std'],
            radius=map_data.iloc[i]['count_std']*500,
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(m)
        folium.Circle(
            location=[map_data.iloc[i]['lat'], map_data.iloc[i]['lon']+0.2],
            popup=map_data.iloc[i]['District'] + ' :\n' + map_data.iloc[i]['prm'],
            radius=map_data.iloc[i]['count_prm']*300,
            color='green',
            fill=True,
            fill_color='green'
        ).add_to(m)
    m.save('mymap.html')
    return m._repr_html_()



@app.route('/barplot-basic')
def get_image1():
    return send_file('./plot-basic.png', mimetype='image/png')



@app.route('/barplot-standard')
def get_image2():
    return send_file('./plot-standard.png', mimetype='image/png')



@app.route('/barplot-premium')
def get_image3():
    return send_file('./plot-premium.png', mimetype='image/png')




######################################################################### UNIT-TESTING


if __name__ == '__main__':
    app.run()


