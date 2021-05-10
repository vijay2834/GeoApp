from django.shortcuts import render, redirect
import os
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from folium.plugins import CirclePattern
from folium.plugins import Draw
from folium.plugins import MeasureControl
from folium.plugins import MousePosition
from folium.plugins import Geocoder
from folium.features import CustomIcon

# Create your views here.
def home(request):
    shp_dir = os.path.join(os.getcwd(),'media','shp')
    df = pd.read_csv(r"https://raw.githubusercontent.com/vijay2834/GeoApp/main/Data/global_power_plant_database.csv")
    df = df[df['country'] == 'IND']
    df_1 = df[df['primary_fuel'] == 'Coal']
    df_2 = df[df['primary_fuel'] != 'Coal']
    df_1['primary_waste'] = ['fly ash']*(df_1.shape[0])
    df_2['primary_waste'] = ['fly ash']*(df_2.shape[0])
    map = folium.Map(location=[20.5937, 78.9629 ], zoom_start=5)
    draw = Draw()
    draw.add_to(map)
    map.add_child(MeasureControl())
    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    MousePosition(
        position="bottomright",
        separator=" | ",
        empty_string="NaN",
        lng_first=True,
        num_digits=20,
        prefix="Coordinates:",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(map)
    Geocoder().add_to(map)

    marker_cluster_1 = MarkerCluster().add_to(map) # create marker clusters
    for i in range(df_1.shape[0]):
        location = [df_1['latitude'].iloc[i],df_1['longitude'].iloc[i]]
        tooltip = "Name:{}<br> Primary_waste: {}<br> Click for more".format(df_1["name"].iloc[i], df_1['primary_waste'].iloc[i])
        CirclePattern()
        folium.Marker(location, # adding more details to the popup screen using HTML
                      popup="""
                      <i>Available waste (Tonnes): </i> <br> <b>{}</b> <br>
                      <i>Decay time (sec): </i><b><br>{}</b><br>""".format(
                        round(df_1['generation_gwh_2016'].iloc[i],2),
                        round(df_1['generation_gwh_2017'].iloc[i],2)),
                        icon = folium.Icon(color='green'),
                      tooltip=tooltip).add_to(marker_cluster_1)

    marker_cluster_2 = MarkerCluster().add_to(map) # create marker clusters

    for i in range(df_2.shape[0]):
        location = [df_2['latitude'].iloc[i],df_2['longitude'].iloc[i]]
        tooltip = "Name:{}<br> Primary_fuel: {}<br> Click for more".format(df_2["name"].iloc[i], df_2['primary_waste'].iloc[i])

        folium.Marker(location, # adding more details to the popup screen using HTML
                      popup="""
                      <i>Required material (Tonnes): </i> <br> <b>{}</b> <br>
                      <i>response time (sec): </i><b><br>{}</b><br>""".format(
                        round(df_2['generation_gwh_2016'].iloc[i],2),
                        round(df_2['generation_gwh_2017'].iloc[i],2)),
                        icon = folium.Icon(color='red',icon = 'info-sign'),
                      tooltip=tooltip).add_to(marker_cluster_2)


    #folium.GeoJson(os.path.join(shp_dir,'basin.geojson'),name='basin',
    #    style_function = lambda x:style_basin).add_to(m)

    #folium.GeoJson(os.path.join(shp_dir,'rivers.geojson'),name='basin',
    #    style_function = lambda x:style_river).add_to(m)

    folium.LayerControl().add_to(map)

    map = map._repr_html_()
    context={'my_map':map}
    return render(request, 'geoApp/home.html',context)
