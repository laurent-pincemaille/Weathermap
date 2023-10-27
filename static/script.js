// Code JavaScript pour initialiser la carte Leaflet
const temperatureFilter = document.getElementById("temperatureFilter");
const temperatureValue = document.getElementById("temperatureValue");

// Initialiser la carte
const map = L.map("map").setView([0, 0], 2);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);


// Ajouter des marqueurs pour les villes avec des données de température
const cities = [
    { name: "Paris", lat: 48.8566, lon: 2.3522 },
    { name: "New York", lat: 40.7128, lon: -74.0060 },
    { name: "Los Angeles", lat: 34.0522, lon: -118.2437 }
    // Ajoutez d'autres villes ici
];

// Écouter les changements de filtre de température
temperatureFilter.addEventListener("input", updateTemperature);

function updateTemperature() {
    const selectedTemperature = temperatureFilter.value;
    temperatureValue.textContent = `${selectedTemperature}°C`;

    // Supprimez les anciens marqueurs de la carte
    map.eachLayer(layer => {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    // Parcourez les villes et ajoutez des marqueurs en fonction de la température (à adapter)
    cities.forEach(city => {
        getCityTemperature(city)
            .then(temperature => {
                if (temperature !== null && temperature >= selectedTemperature) {
                    L.marker([city.lat, city.lon])
                        .bindPopup(`<b>${city.name}</b><br>${temperature}°C`)
                        .addTo(map);
                }
            });
    });
}

async function getCityTemperature(city) {
    const response = await fetch("/get_temperature", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({city}),
    });
    const data = await response.json();
    return data.temperature;
}

// Initialiser la carte avec les marqueurs
updateTemperature();
