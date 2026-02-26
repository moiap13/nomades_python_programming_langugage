from flask import Flask, render_template
import folium  # conda install folium
import requests

app = Flask(__name__)


@app.route("/")
def index():
    m = folium.Map(location=[46.2, 6.15], zoom_start=12)
    map_html = m._repr_html_()
    return render_template("index.html", map_html=map_html)


@app.route("/map/<float:lat>/<float:lon>")
def dynamic_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=14)
    folium.Marker(
        [lat, lon],
        popup=render_template("components/geneve.html"),
    ).add_to(m)
    return render_template("index.html", map_html=m._repr_html_())


@app.route("/api_users")
def api_users():
    m = folium.Map(location=[0, 0], zoom_start=2)
    users: list[dict] = requests.get(
        "https://jsonplaceholder.typicode.com/users"
    ).json()
    for user in users:
        lat = float(user["address"]["geo"]["lat"])
        lon = float(user["address"]["geo"]["lng"])
        popup = f"<h1>{user['name']}</h1><br>{user['address']['city']}"
        folium.Marker([lat, lon], popup=popup).add_to(m)

    m.fit_bounds(m.get_bounds())

    return render_template("index.html", map_html=m._repr_html_())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
