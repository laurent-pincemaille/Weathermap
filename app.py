from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Données simulées de température par coordonnées géographiques (exemples)
temperature_data = {
    'Paris':  {'coord':(48.8566, 2.3522),'temperature': 20},  # Paris
    'New York':{'coord':(40.7128, -74.0060),'temperature': 25},  # New York
    # Ajoutez d'autres coordonnées et températures ici
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_temperature", methods=["POST"])
def get_temperature():
    data = request.get_json()
    city = data["city"]["name"]
    
    if city in temperature_data:
        temperature = temperature_data[city]['temperature']
    else:
        temperature = None

    return jsonify({"temperature": temperature})

if __name__ == "__main__":
    app.run(debug=True)
