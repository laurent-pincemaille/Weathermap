import folium
import requests
from cachetools import LRUCache
from joblib import Memory
from branca.colormap import LinearColormap
import os
# Remplacez 'YOUR_API_KEY' par votre clé API OpenWeatherMap
API_KEY = '856e8e2c5708a1b11394f08b1b9a578e'





# Décorateur pour mettre en cache les données météorologiques
def cache_weather_data(func):
    # Initialisation du cache
    cache = LRUCache(maxsize=100)  # Cache en mémoire

    # Définissez un dossier de cache pour le stockage sur disque
    cachedir = './weather_cache'
    memory = Memory(cachedir, verbose=0)
    def wrapper(city):
        if city in cache:
            return cache[city]
        else:
            # Vérifiez si les données sont en cache sur disque
            temperature = memory.cache(func)(city)
            cache[city] = temperature  # Mettre en cache en mémoire
            return temperature
    return wrapper

# Fonction pour obtenir les données météorologiques à partir de l'API OpenWeatherMap
@cache_weather_data
def get_weather_data(city):
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(base_url)
    data = response.json()
    save_icon(data['weather'][0]['icon'])
    return data

def get_weather(city):
    data = get_weather_data(city)
    temperature = data['main']['temp'] - 273.15  # Conversion de Kelvin à Celsius
    icon = data['weather'][0]['icon']
    icon_path = os.path.join(os.getcwd(),rf"images/icons/{icon}.png")
    current_weather = data['weather'][0]['description']
    return {'temperature':temperature,'current_weather':current_weather,'icon_path':icon_path}

def get_icon(city):
    data = get_weather_data(city)
    icon = data['weather'][0]['icon']
    path = rf"images/icons/{icon}.png"
    return path 



def save_icon(id_icon):
    import os
    folder_path = "images/icons"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_url= f'http://openweathermap.org/img/w/{id_icon}.png'
    response = requests.get(image_url)
    filepath = os.path.join(folder_path, f'{id_icon}.png')

    # Save the image to the specified folder
    with open(filepath, 'wb') as file:
        file.write(response.content)
    print(f'Saving to {filepath}')

# Créez une carte Folium centrée sur une coordonnée géographique
m = folium.Map(location=[0, 0], zoom_start=2)

legend = LinearColormap(['blue', 'red'], vmin=-10, vmax=35)
legend.caption = 'Température (°C)'
legend.add_to(m)

# Ajoutez des marqueurs pour les villes de votre choix avec les températures actuelles
cities = [('Paris', [48.8566, 2.3522]), ('New York', [40.7128, -74.0060]), ('Tokyo', [35.682839, 139.759455])]

# Ajoutez un curseur HTML pour choisir le seuil de température
slider_html = """
<input type="range" id="temperature-slider" min="-10" max="40" value="12">
<div id="temperature-label">Seuil de température : 12°C</div>
"""

slider_js = """
var slider = document.getElementById("temperature-slider");
var label = document.getElementById("temperature-label");

slider.oninput = function() {
    label.innerHTML = "Seuil de température : " + this.value + "°C";
    filterMarkers(this.value);
}

function filterMarkers(threshold) {
    var markers = document.getElementsByClassName("temperature-marker");
    for (var i = 0; i < markers.length; i++) {
        var marker = markers[i];
        var temperature = parseFloat(marker.getAttribute("data-temperature"));
        if (temperature > threshold) {
            marker.style.display = "block";
        } else {
            marker.style.display = "none";
        }
    }
}
"""

# Ajoutez le curseur à la carte
m.get_root().html.add_child(folium.Element(slider_html))
m.get_root().script.add_child(folium.Element(slider_js))

for city, coords in cities:
    weather = get_weather(city)
    temperature = weather['temperature']
    color = legend(temperature)
    if temperature is not None:
        # Créez un polygone pour la ville
        # polygon = folium.Polygon(
        #     locations=[coords],
        #     color="blue",  # Couleur de la bordure
        #     fill=True,
        #     fill_color="blue",  # Couleur de remplissage
        #     fill_opacity=0.4,  # Opacité du remplissage
        #     popup=f"Température actuelle à {city}: {temperature:.1f}°C"
        # )
        # polygon.add_to(m)
        folium.CircleMarker(
        location=coords,
        radius=1,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
                     popup=f"Température actuelle à {city}: {temperature:.1f}°C"             ).add_to(m)
        
        # Créez un marqueur avec l'icône météorologique personnalisée
        folium.Marker(
            location=coords,  
            icon=folium.CustomIcon(
                icon_image=weather['icon_path'],  # Chemin de l'icône correspondant aux conditions météorologiques actuelles
                icon_size=(25, 25),
            ),
            popup=f"Conditions météo actuelles : {weather['current_weather']}",
        ).add_to(m)

        # Ajoutez une légende de température sous le cercle
        folium.map.Marker(
            [coords[0] - 0.2, coords[1]+0.2],  # Ajustez la position de la légende
            icon=folium.DivIcon(html=f'<div style="color: {color}; font-weight: bold; font-size: 16px;">{temperature:.1f}°C</div>')
        ).add_to(m)

    


# Enregistrez la carte dans un fichier HTML
m.save('carte_meteo.html')
print("Hey")