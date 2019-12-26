import folium
import pandas

data = pandas.read_csv("data/Volcanoes.txt")  # Geo data of volcanoes
lat = list(data["LAT"])  # List of latitudes
lon = list(data["LON"])  # List of longitudes
elev = list(data["ELEV"])  # List of elevations (height of the volcano)


def color_producer(elevation):
    """
        Takes an integer as an input and returns a string representing a color.
        :param elevation: An integer
        :return: One of the three strings for the color 'red', 'green' & 'orange'
    """
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


my_map = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles="openstreetmap")  # Folium map object
feature_group_volcanoes = folium.FeatureGroup(name="Volcanoes")  # New feature group object for volcanoes

"""
Iterates thru the list of latitude, longitude and elevation for each volcano and adds a circle marker for it in 
feature_group_volcanoes
"""
for lt, ln, el in zip(lat, lon, elev):
    feature_group_volcanoes.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=str(el) + ' m',
                                                          fill_color=color_producer(el), fill=True, color='grey',
                                                          fill_opacity=10))


feature_group_population = folium.FeatureGroup(name="Population")

feature_group_population.add_child(folium.GeoJson(data=open('data/world.json', 'r', encoding='utf-8-sig').read(),
                                                  style_function=lambda x: {'fillColor':'green' if x['properties']
                                                    ['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']
                                                  ['POP2005'] < 20000000 else 'red'}))

my_map.add_child(feature_group_volcanoes)  # Attaches feature group for volcanoes to the folium map object
my_map.add_child(feature_group_population)
my_map.add_child(folium.LayerControl())  # Adds a button to control the map layers
my_map.save("Map1.html")  # Creates the map as a HTML document
