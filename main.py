import heapq
from itertools import permutations

# Datos de camiones
trucks = [
    {"id": 1, "max_weight": 70, "max_fuel": 35},
    {"id": 2, "max_weight": 64, "max_fuel": 50},
    {"id": 3, "max_weight": 80, "max_fuel": 38}
]

# Paquetes con sus pesos
items = [
    {"id": 1, "weight": 20}, {"id": 2, "weight": 5}, {"id": 3, "weight": 10},
    {"id": 4, "weight": 40}, {"id": 5, "weight": 25}, {"id": 6, "weight": 35},
    {"id": 7, "weight": 80}, {"id": 8, "weight": 50}
]

# Lugares de entrega con distancias
places = [
    {"id": 1, "distance": 3, "item_id": 1}, {"id": 2, "distance": 4, "item_id": 2},
    {"id": 3, "distance": 2, "item_id": 3}, {"id": 4, "distance": 1, "item_id": 4},
    {"id": 5, "distance": 5, "item_id": 5}, {"id": 6, "distance": 3, "item_id": 6},
    {"id": 7, "distance": 4, "item_id": 7}, {"id": 8, "distance": 2, "item_id": 8}
]

# Grafo de distancias simuladas
graph = {
    0: {1: 3, 2: 4, 3: 2, 4: 1, 5: 5, 6: 3, 7: 4, 8: 2},  # Nodo 0 es el origen
    1: {2: 1, 3: 4, 4: 7},
    2: {1: 1, 3: 2, 5: 5},
    3: {1: 4, 2: 2, 6: 3},
    4: {1: 7, 5: 2, 7: 4},
    5: {2: 5, 4: 2, 8: 1},
    6: {3: 3, 8: 6},
    7: {4: 4, 8: 2},
    8: {5: 1, 6: 6, 7: 2}
}

# Algoritmo de Dijkstra para rutas óptimas
def dijkstra(graph, start):
    pq = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    return distances, previous

# Asignación de paquetes a camiones
assignments = {truck["id"]: {"items": [], "route": [], "fuel_used": 0} for truck in trucks}
for place in places:
    item = next(i for i in items if i["id"] == place["item_id"])
    
    best_truck = None
    min_fuel = float('inf')
    
    for truck in trucks:
        if sum(i["weight"] for i in assignments[truck["id"]]["items"]) + item["weight"] <= truck["max_weight"]:
            fuel_usage = truck["max_fuel"] * (place["distance"] / 10)
            if fuel_usage < min_fuel:
                min_fuel = fuel_usage
                best_truck = truck
    
    if best_truck:
        assignments[best_truck["id"]]["items"].append(item)
        assignments[best_truck["id"]]["route"].append(place["id"])
        assignments[best_truck["id"]]["fuel_used"] += min_fuel

# Optimización de rutas con Dijkstra y regreso al origen
for truck_id in assignments:
    if assignments[truck_id]["route"]:
        start_node = 0
        end_nodes = assignments[truck_id]["route"]
        end_nodes.append(0)  # Regresar a origen
        distances, prev_nodes = dijkstra(graph, start_node)
        optimal_route = sorted(end_nodes, key=lambda x: distances.get(x, float('inf')))
        assignments[truck_id]["route"] = optimal_route

# Resultados
for truck_id, data in assignments.items():
    print(f"\n🚚 Camión {truck_id}:")
    print(f"   - Paquetes: {[item['id'] for item in data['items']]}")
    print(f"   - Ruta: {data['route']}")
    print(f"   - Combustible estimado: {round(data['fuel_used'], 2)}L")