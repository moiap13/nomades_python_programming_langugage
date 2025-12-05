import sys
import os

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
PLOTS_DIR: str = os.path.join(ROOT_DIR, "static", "plots")
sys.path.append(ROOT_DIR)

from flask import Blueprint, render_template
import folium  # conda install folium / pip install folium
import requests


map_bp = Blueprint("map", __name__, url_prefix="/map")


@map_bp.route("/")
def index():
    m = folium.Map(location=[46.2, 6.15], zoom_start=10)
    map_html = m._repr_html_()
    return render_template("map/map.html", map_html=map_html)


@map_bp.route("/<lat>/<lon>")
def dynamic_map(lat, lon):
    m = folium.Map(location=[float(lat), float(lon)], zoom_start=14)
    folium.Marker([lat, lon], popup="Position dynamique").add_to(m)
    return render_template("map/map.html", map_html=m._repr_html_())


@map_bp.route("/api_users")
def api_users():
    m = folium.Map(location=[0, 0], zoom_start=2)
    users = requests.get("https://jsonplaceholder.typicode.com/users").json()
    for user in users:
        lat = float(user["address"]["geo"]["lat"])
        lon = float(user["address"]["geo"]["lng"])
        popup = f"<h1>{user['name']}</h1><br>{user['address']['city']}"
        folium.Marker([lat, lon], popup=popup).add_to(m)

    m.fit_bounds(m.get_bounds())

    return render_template("map/map.html", map_html=m._repr_html_())
