from flask import Flask
app = Flask(__name__)

import numpy as np  
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.geocoders import Nominatim
import folium
import webbrowser


pd.pandas.set_option('display.max_columns', None)
data= pd.read_csv('./CitizenNeeds.csv')




@app.route('/')
def hello():
    plt.figure()
    chains=data['Basic Need'].value_counts()
    sns.barplot(x=chains,y=chains.index,palette='rocket')
    plt.title("Density plot of Basic Need in Kerala")
    plt.xlabel("Number of citizens opted")
    plt.show()
    plt.figure()
    chains=data['Standard Need'].value_counts()
    sns.barplot(x=chains,y=chains.index,palette='rocket')
    plt.title("Density plot of Standard Need in Kerala")
    plt.xlabel("Number of citizens opted")
    plt.show()
    plt.figure()
    chains=data['Premium Need'].value_counts()
    sns.barplot(x=chains,y=chains.index,palette='rocket')
    plt.title("Density plot of Premium Need in Kerala")
    plt.xlabel("Number of citizens opted")
    plt.show()
    return "Hello world"



@app.route('/<name>')
def hello_name(name):
    data= pd.read_csv('./CitizenNeeds.csv')
    data_TVM = data[data['District'].str.contains("Trivandrum")]
    data_TVM_basic = {} 
    data_TVM_std = {} 
    data_TVM_prm = {} 
    data_TVM_basic = data_TVM['Basic Need'].value_counts()
    data_TVM_std = data_TVM['Standard Need'].value_counts()
    data_TVM_prm = data_TVM['Premium Need'].value_counts()
    data_TSR = data[data['District'].str.contains("Thrissur")]
    data_TSR_basic = {} 
    data_TSR_std = {} 
    data_TSR_prm = {} 
    data_TSR_basic = data_TSR['Basic Need'].value_counts()
    data_TSR_std = data_TVM['Standard Need'].value_counts()
    data_TSR_prm = data_TVM['Premium Need'].value_counts()
    data_KKD = data[data['District'].str.contains("Kozhikode")]
    data_KKD_basic = {} 
    data_KKD_std = {} 
    data_KKD_prm = {} 
    data_KKD_basic = data_KKD['Basic Need'].value_counts()
    data_KKD_std = data_KKD['Standard Need'].value_counts()
    data_KKD_prm = data_KKD['Premium Need'].value_counts()
    data_EKM = data[data['District'].str.contains("Ernakulam")]
    data_EKM_basic = {} 
    data_EKM_std = {} 
    data_EKM_prm = {} 
    data_EKM_basic = data_EKM['Basic Need'].value_counts()
    data_EKM_std = data_EKM['Standard Need'].value_counts()
    data_EKM_prm = data_EKM['Premium Need'].value_counts()

    locations=pd.DataFrame({"Name":data['District'].unique()})
    locations['Name']=locations['Name'].apply(lambda x: "" + str(x))
    lat_lon=[]
    geolocator=Nominatim(user_agent="app")
    for location in locations['Name']:
        location = geolocator.geocode(location)
        if location is None:
            lat_lon.append(np.nan)
        else:    
            geo=(location.latitude,location.longitude)
            lat_lon.append(geo)


    locations['geo_loc']=lat_lon
    locations.to_csv('locations.csv',index=False)

    Rest_locations=pd.DataFrame(data['District'].value_counts().reset_index())
    Rest_locations.columns=['Name','count']
    Rest_locations=Rest_locations.merge(locations,on='Name',how="left").dropna()

    lat,lon=zip(*np.array(Rest_locations['geo_loc']))
    Rest_locations['lat']=lat
    Rest_locations['lon']=lon
    Rest_locations['count'] = [float(i) for i in Rest_locations['count']]

    Rest_locations['basic'] = [data_EKM_basic.index[0], data_TVM_basic.index[0],data_TSR_basic.index[0],data_KKD_basic.index[0]]
    Rest_locations['std'] = [data_EKM_std.index[0], data_TVM_std.index[0],data_TSR_std.index[0],data_KKD_std.index[0]]
    Rest_locations['prm'] = [data_EKM_prm.index[0], data_TVM_prm.index[0],data_TSR_prm.index[0],data_KKD_prm.index[0]]

    Rest_locations['count_basic'] = [data_EKM_basic[0], data_TVM_basic[0],data_TSR_basic[0],data_KKD_basic[0]]
    Rest_locations['count_std'] = [data_EKM_std[0], data_TVM_std[0],data_TSR_std[0],data_KKD_std[0]]
    Rest_locations['count_prm'] = [data_EKM_prm[0], data_TVM_prm[0],data_TSR_prm[0],data_KKD_prm[0]]

    Rest_locations['count_basic'] = [float(i) for i in Rest_locations['count_basic']]
    Rest_locations['count_std'] = [float(i) for i in Rest_locations['count_std']]
    Rest_locations['count_prm'] = [float(i) for i in Rest_locations['count_prm']]

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
    new = 1
    url = "./mymap.html"
    webbrowser.open(url)
    return "Hello {}!".format(name)

    


if __name__ == '__main__':
    app.run()