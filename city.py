import networkx as nx
import matplotlib.pyplot as plt
import heapq
import math
import time
from datetime import datetime

def create_indian_cities_graph():
    """Create a graph of major Indian cities with actual distances and additional metadata"""
    graph = {
        'Delhi': {
            'Mumbai': {'distance': 1414, 'route': 'NH48', 'traffic': 'moderate'},
            'Kolkata': {'distance': 1474, 'route': 'NH19', 'traffic': 'heavy'},
            'Jaipur': {'distance': 281, 'route': 'NH48', 'traffic': 'low'},
            'Lucknow': {'distance': 555, 'route': 'NH27', 'traffic': 'moderate'},
            'Ahmedabad': {'distance': 934, 'route': 'NH48', 'traffic': 'moderate'}
        },
        'Mumbai': {
            'Bangalore': {'distance': 984, 'route': 'NH48', 'traffic': 'moderate'},
            'Hyderabad': {'distance': 706, 'route': 'NH65', 'traffic': 'heavy'},
            'Ahmedabad': {'distance': 524, 'route': 'NH48', 'traffic': 'low'},
            'Jaipur': {'distance': 1148, 'route': 'NH48', 'traffic': 'moderate'}
        },
        'Kolkata': {
            'Hyderabad': {'distance': 1515, 'route': 'NH16', 'traffic': 'heavy'},
            'Chennai': {'distance': 1679, 'route': 'NH16', 'traffic': 'moderate'},
            'Lucknow': {'distance': 985, 'route': 'NH27', 'traffic': 'low'}
        },
        'Bangalore': {
            'Chennai': {'distance': 346, 'route': 'NH48', 'traffic': 'moderate'},
            'Hyderabad': {'distance': 574, 'route': 'NH44', 'traffic': 'heavy'},
            'Mumbai': {'distance': 984, 'route': 'NH48', 'traffic': 'moderate'}
        },
        'Chennai': {
            'Hyderabad': {'distance': 627, 'route': 'NH65', 'traffic': 'moderate'},
            'Bangalore': {'distance': 346, 'route': 'NH48', 'traffic': 'low'},
            'Kolkata': {'distance': 1679, 'route': 'NH16', 'traffic': 'heavy'}
        },
        'Hyderabad': {
            'Mumbai': {'distance': 706, 'route': 'NH65', 'traffic': 'moderate'},
            'Bangalore': {'distance': 574, 'route': 'NH44', 'traffic': 'heavy'},
            'Chennai': {'distance': 627, 'route': 'NH65', 'traffic': 'moderate'},
            'Kolkata': {'distance': 1515, 'route': 'NH16', 'traffic': 'heavy'}
        },
        'Ahmedabad': {
            'Mumbai': {'distance': 524, 'route': 'NH48', 'traffic': 'moderate'},
            'Jaipur': {'distance': 657, 'route': 'NH48', 'traffic': 'low'},
            'Delhi': {'distance': 934, 'route': 'NH48', 'traffic': 'heavy'}
        },
        'Jaipur': {
            'Delhi': {'distance': 281, 'route': 'NH48', 'traffic': 'low'},
            'Ahmedabad': {'distance': 657, 'route': 'NH48', 'traffic': 'moderate'},
            'Lucknow': {'distance': 574, 'route': 'NH27', 'traffic': 'moderate'}
        },
        'Lucknow': {
            'Delhi': {'distance': 555, 'route': 'NH27', 'traffic': 'moderate'},
            'Kolkata': {'distance': 985, 'route': 'NH27', 'traffic': 'heavy'},
            'Jaipur': {'distance': 574, 'route': 'NH27', 'traffic': 'low'}
        }
    }
    return graph

def get_city_positions():
    """Get improved geographical positions for cities to reduce overlap"""
    return {
        'Delhi': (6.5, 8.5),    # Adjusted North
        'Mumbai': (2, 4.2),     # Adjusted West
        'Kolkata': (9.2, 5),    # Adjusted East
        'Bangalore': (4, 1),    # South
        'Chennai': (6.2, 1),    # Adjusted South
        'Hyderabad': (5, 3.2),  # Adjusted Central
        'Ahmedabad': (1, 6.2),  # Adjusted West
        'Jaipur': (4, 7.2),     # Adjusted North
        'Lucknow': (7.2, 6.8)   # Adjusted North-Central
    }

def calculate_eta(distance, traffic):
    """Calculate estimated time of arrival based on distance and traffic"""
    average_speed = {
        'low': 70,
        'moderate': 55,
        'heavy': 40
    }
    speed = average_speed[traffic]
    return distance / speed

def dijkstra(graph, start, end):
    """Enhanced Dijkstra's algorithm considering traffic conditions"""
    distances = {city: float('infinity') for city in graph}
    distances[start] = 0
    previous = {city: None for city in graph}
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_distance, current_city = heapq.heappop(pq)
        
        if current_city == end:
            break
            
        if current_city in visited:
            continue
            
        visited.add(current_city)
        
        for neighbor, data in graph[current_city].items():
            # Consider traffic conditions in distance calculation
            traffic_factor = {'low': 1.0, 'moderate': 1.2, 'heavy': 1.5}
            adjusted_distance = data['distance'] * traffic_factor[data['traffic']]
            distance = current_distance + adjusted_distance
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_city
                heapq.heappush(pq, (distance, neighbor))
    
    path = []
    current_city = end
    while current_city is not None:
        path.append(current_city)
        current_city = previous[current_city]
    path.reverse()
    
    return path, distances[end]

def visualize_ride_route(graph, path=None):
    """Enhanced visualization for ride routes with real-time information"""
    plt.figure(figsize=(15, 12))
    plt.clf()
    
    # Create a simplified graph with just distances for NetworkX
    simple_graph = {city: {dest: data['distance'] for dest, data in connections.items()}
                   for city, connections in graph.items()}
    G = nx.Graph(simple_graph)
    pos = get_city_positions()
    
    # Improved background
    plt.grid(True, linestyle='--', alpha=0.2)
    
    # Draw all edges with traffic-based colors
    for city1 in graph:
        for city2, data in graph[city1].items():
            traffic_colors = {'low': 'green', 'moderate': 'orange', 'heavy': 'red'}
            nx.draw_networkx_edges(G, pos, 
                                 edgelist=[(city1, city2)],
                                 edge_color=traffic_colors[data['traffic']],
                                 width=1, alpha=0.3)
    
    # Create detailed edge labels
    edge_labels = {}
    for city1 in graph:
        for city2, data in graph[city1].items():
            eta = calculate_eta(data['distance'], data['traffic'])
            label = f"{data['distance']}km\n{data['route']}\n{eta:.1f}h"
            edge_labels[(city1, city2)] = label
    
    # Draw edge labels with improved positioning
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=7,
                               bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    # Draw all nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightgray', 
                          node_size=2500, alpha=0.5)
    
    # Draw city labels with improved style
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # Highlight the ride route if provided
    if path and len(path) > 1:
        path_edges = list(zip(path[:-1], path[1:]))
        
        # Calculate total metrics
        total_distance = 0
        total_time = 0
        for i in range(len(path)-1):
            data = graph[path[i]][path[i+1]]
            total_distance += data['distance']
            total_time += calculate_eta(data['distance'], data['traffic'])
        
        # Draw highlighted path
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, 
                             edge_color='blue', width=3)
        
        # Highlight ride points
        nx.draw_networkx_nodes(G, pos, nodelist=path,
                             node_color='lightblue', 
                             node_size=2500, alpha=0.7)
        
        # Highlight start and end points
        nx.draw_networkx_nodes(G, pos, nodelist=[path[0]],
                             node_color='lime', 
                             node_size=2500, alpha=0.7)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[-1]],
                             node_color='red', 
                             node_size=2500, alpha=0.7)
        
        # Add comprehensive route information
        current_time = datetime.now()
        eta_time = current_time.replace(hour=(current_time.hour + int(total_time)) % 24)
        
        title = f"Ride Route: {' → '.join(path)}\n"
        title += f"Total Distance: {total_distance} km | Estimated Time: {total_time:.1f} hours\n"
        title += f"Expected Arrival: {eta_time.strftime('%I:%M %p')}"
        plt.title(title, pad=20, size=12)
    else:
        plt.title("Available Ride Routes\nClick to select pickup and drop-off points", 
                 pad=20, size=14)
    
    plt.axis('off')
    plt.tight_layout()
    plt.draw()
    plt.pause(0.1)

def format_ride_details(path, graph):
    """Enhanced format for ride details with comprehensive information"""
    if not path or len(path) < 2:
        return "No valid route found!"
        
    total_distance = 0
    total_time = 0
    
    details = "\nRide Details:\n" + "="*70 + "\n"
    details += f"Pickup Location: {path[0]}\n"
    details += f"Drop-off Location: {path[-1]}\n"
    
    details += "\nRoute Breakdown:\n" + "-"*70 + "\n"
    details += f"{'From':15} {'To':15} {'Distance':10} {'Route':10} {'Traffic':10} {'ETA':10}\n"
    details += "-"*70 + "\n"
    
    for i in range(len(path)-1):
        data = graph[path[i]][path[i+1]]
        distance = data['distance']
        eta = calculate_eta(distance, data['traffic'])
        
        details += f"{path[i]:15} {path[i+1]:15} {distance:10} {data['route']:10} "
        details += f"{data['traffic']:10} {eta:.1f}h\n"
        
        total_distance += distance
        total_time += eta
    
    details += "="*70 + "\n"
    details += f"Total Distance: {total_distance} km\n"
    details += f"Total Estimated Time: {total_time:.1f} hours\n"
    details += f"Expected Arrival: {datetime.now().replace(hour=(datetime.now().hour + int(total_time)) % 24).strftime('%I:%M %p')}\n"
    
    return details

def main():
    graph = create_indian_cities_graph()
    
    print("\nRide Route Finder")
    print("="*50)
    print("\nAvailable Locations:")
    for i, city in enumerate(sorted(graph.keys()), 1):
        print(f"{i}. {city}")
    
    while True:
        print("\n" + "="*50)
        pickup = input("\nEnter pickup location (or 'quit' to exit): ").title()
        if pickup.lower() == 'quit':
            break
            
        if pickup not in graph:
            print(f"Error: '{pickup}' is not a valid location!")
            continue
            
        dropoff = input("Enter drop-off location: ").title()
        if dropoff not in graph:
            print(f"Error: '{dropoff}' is not a valid location!")
            continue
            
        if pickup == dropoff:
            print("Pickup and drop-off locations are the same!")
            continue
        
        # Find and display route
        path, _ = dijkstra(graph, pickup, dropoff)
        print(format_ride_details(path, graph))
        
        # Visualize
        visualize_ride_route(graph, path)
        plt.show(block=False)
        
        choice = input("\nPlan another ride? (yes/no): ").lower()
        if choice != 'yes':
            break
    
    plt.close('all')

if __name__ == "__main__":
    main()