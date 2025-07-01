import requests
import sys

def obtener_coordenadas(ciudad):
    # Ítem: Solicitar Ciudad de Origen y Ciudad de Destino
    # Narrativa: Se convierte el nombre de una ciudad en coordenadas geográficas usando Nominatim.
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": ciudad,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "mi-aplicacion-python"
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    
    if not data:
        print(f"No se pudo encontrar la ciudad: {ciudad}")
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])

def calcular_ruta(origen_coords, destino_coords, modo):
    # Ítem: Medir la distancia entre una ciudad de Chile y una de Argentina
    # Narrativa: Se utiliza OSRM para calcular la ruta entre coordenadas geográficas.
    base_url = f"http://router.project-osrm.org/route/v1/{modo}/"
    coords = f"{origen_coords[1]},{origen_coords[0]};{destino_coords[1]},{destino_coords[0]}"
    url = base_url + coords
    params = {"overview": "false", "steps": "true"}  # Se incluyen steps aunque no se usen, para mayor precisión.
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error al obtener la ruta.")
        return None
    
    data = response.json()
    if not data["routes"]:
        print("No se pudo calcular una ruta.")
        return None

    ruta = data["routes"][0]
    return ruta["distance"]

def mostrar_resultados(distancia_mts, modo):
    # Ítem: Mostrar distancia en millas, kilómetros y duración del viaje
    # Narrativa: Se calculan y muestran distancia y tiempo según velocidad promedio real por tipo de transporte.
    distancia_km = distancia_mts / 1000
    distancia_millas = distancia_km * 0.621371

    velocidades = {
        "driving": 80,    # km/h promedio estimado en carretera
        "cycling": 15,    # km/h promedio en bicicleta
        "walking": 5      # km/h caminando
    }
    velocidad = velocidades.get(modo, 80)

    duracion_horas = distancia_km / velocidad
    horas = int(duracion_horas)
    minutos = int((duracion_horas - horas) * 60)

    print("\n=== RESULTADOS DEL VIAJE ===")
    print(f"Distancia: {distancia_km:.2f} km")
    print(f"Distancia: {distancia_millas:.2f} millas")
    print(f"Duración estimada ({modo}): {horas}h {minutos}min")
    print("=============================\n")

    # Ítem: Mostrar narrativa del viaje
    # Narrativa: Esta versión no entrega instrucciones paso a paso, pero presenta un resumen del trayecto estimado.

def main():
    # Ítem: Inicio del programa e interacción
    # Narrativa: Se presenta el programa y se permite salir escribiendo "s" en cualquier momento.
    print("Planificador de viaje Chile ↔ Argentina (sin clave API)")
    print("Escribe 's' para salir en cualquier momento.\n")

    modos = {
        "1": "driving",   # Auto
        "2": "walking",   # A pie
        "3": "cycling"    # Bicicleta
    }

    while True:
        origen = input("Ciudad de Origen: ")
        if origen.lower() == "s":
            break

        destino = input("Ciudad de Destino: ")
        if destino.lower() == "s":
            break

        # Ítem: Elegir tipo de medio de transporte
        # Narrativa: Se ofrecen tres modos de transporte para ajustar tiempo estimado de viaje.
        print("\nTipo de transporte:")
        print("1. Auto")
        print("2. A pie")
        print("3. Bicicleta")
        modo_input = input("Seleccione transporte (1/2/3): ")

        if modo_input not in modos:
            print("Opción no válida.\n")
            continue

        modo = modos[modo_input]

        coords_origen = obtener_coordenadas(origen + ", Chile")
        coords_destino = obtener_coordenadas(destino + ", Argentina")

        if coords_origen and coords_destino:
            distancia = calcular_ruta(coords_origen, coords_destino, modo)
            if distancia:
                mostrar_resultados(distancia, modo)

# Ítem: Subir a GitHub con commit a elección
# Narrativa: El archivo puede ser versionado fácilmente con Git para mantener histórico o compartir el proyecto.

if __name__ == "__main__":
    main()
