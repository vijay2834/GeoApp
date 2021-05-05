from django.shortcuts import render, redirect
import os
import folium


# Create your views here.
def home(request):
    shp_dir = os.path.join(os.getcwd(),'media','shp')

    m = folium.Map(location=[20.5937, 78.9629 ], zoom_start=5)

    click = True
    folium.Marker(
        location = [20.5937,78.9629],
        popup = """Ntpc steelplant
                    1300 tonnes waste""",
        icon = folium.Icon(color = 'green'),
    ).add_to(m)
    if(click):
        folium.CircleMarker(
        radius = 100,
        location = [20.5937,78.9629],
        color = '#3186cc',
        fill = True,
        fill_color = '#3186cc',
        ).add_to(m)
    style_basin = {'fillColor':'#228B22','color':'#228B22'}
    style_river = {'color':'blue'}

    #folium.GeoJson(os.path.join(shp_dir,'basin.geojson'),name='basin',
    #    style_function = lambda x:style_basin).add_to(m)

    #folium.GeoJson(os.path.join(shp_dir,'rivers.geojson'),name='basin',
    #    style_function = lambda x:style_river).add_to(m)

    folium.LayerControl().add_to(m)

    m = m._repr_html_()
    context={'my_map':m}
    return render(request, 'geoApp/home.html',context)
