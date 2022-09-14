import streamlit as st
import folium
from pyproj import Transformer
from streamlit_folium import folium_static
from geojson import MultiPolygon

from api import get_plots_nearby

st.title("Waterschapshuis API test")

col1, col2 = st.columns(2)

with col1:
    x = st.number_input("X coordinaat [m in RD]", value=148269)
with col2:
    y = st.number_input("Y coordinaat [m in RD]", value=410592)

transformer = Transformer.from_crs(28992, 4326)
lat, lon = transformer.transform(x, y)
m = folium.Map(location=[lat, lon])


plots = get_plots_nearby(lat, lon)

style_grasland = {"fillColor": "#228B22", "color": "#228B22"}
style_mais = {"fillColor": "#f0f00e", "color": "#f0f00e"}
style_pompoen = {"fillColor": "#e0a40b", "color": "#e0a40b"}
style_prei = {"fillColor": "#ffffff", "color": "#ffffff"}
style_undefined = {"fillColor": "#c7c5bf", "color": "#c7c5bf"}

for plot in plots:
    geom = plot["geometry"]
    mp = MultiPolygon(geom["coordinates"])

    # terrible code but who cares for a test..
    if plot["cropName"].find("Grasland") > -1:
        folium.GeoJson(
            mp, name=plot["cropName"], style_function=lambda x: style_grasland
        ).add_to(m)
    elif plot["cropName"].find("Maïs") > -1:
        folium.GeoJson(
            mp, name=plot["cropName"], style_function=lambda x: style_mais
        ).add_to(m)
    elif plot["cropName"].find("Pompoen") > -1:
        folium.GeoJson(
            mp, name=plot["cropName"], style_function=lambda x: style_pompoen
        ).add_to(m)
    elif plot["cropName"].find("Prei") > -1:
        folium.GeoJson(
            mp, name=plot["cropName"], style_function=lambda x: style_prei
        ).add_to(m)
    else:
        folium.GeoJson(
            mp, name=plot["cropName"], style_function=lambda x: style_undefined
        ).add_to(m)


folium_static(m)
