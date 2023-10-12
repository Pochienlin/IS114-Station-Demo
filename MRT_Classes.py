from typing import Any, Dict, List, Optional, Tuple
import heapq

class Station:
    def __init__(self, code: str, name: str, line: str):
        self.code = code
        self.name = name
        self.line = line
        self.neighbors: Dict['Station', int] = {}

    def add_neighbor(self, neighbor: 'Station', cost: int = 1):
        self.neighbors[neighbor] = cost
    def __str__(self):
        return f"{{code: {self.code}, name: {self.name}, neighbors: {[n.name for n in self.neighbors]}, line: {self.line}}}"

class MetroMap:
    def __init__(self, lines: Dict[str, List[Tuple[str, str]]]):
        self.stations: Dict[str, Station] = {}
        self._process_lines(lines)
    def __str__(self):
        output=""
        for code, station in self.stations.items():
            output += f"Station: {station.__str__()}\n"
        return output

    def _process_lines(self, lines: Dict[str, List[Tuple[str, str]]]):
        name_to_station = {}
        for line, stops in lines.items():
            for i in range(len(stops)):
                code, name = stops[i]
                station = Station(code, name, line)
                self.stations[code] = station

                # Connect to the previous station on the same line
                if i > 0:
                    last_code, _ = stops[i-1]
                    self.add_connection(last_code, code)

                # Connect interchange stations
                if name in name_to_station:
                    for other_station in name_to_station[name]:
                        self.add_connection(code, other_station.code)

                else:
                    name_to_station[name] = set()

                name_to_station[name].add(station)
                        
    def add_connection(self, code1: str, code2: str):
        station1 = self.stations[code1]
        station2 = self.stations[code2]
        station1.add_neighbor(station2)
        station2.add_neighbor(station1)
    
    def find_shortest_path(self, start: str, stop: str) -> Tuple[List[str], List[Tuple[str, str]]]:
        parent_map = {start: None}
        costs = {start: 0}
        queue = [(0, start)]
        
        while queue:
            _, current_code = heapq.heappop(queue)
            if current_code == stop:
                break
            for neighbor in self.stations[current_code].neighbors:
                new_cost = costs[current_code] + self.stations[current_code].neighbors[neighbor]
                if neighbor.code not in costs or new_cost < costs[neighbor.code]:
                    costs[neighbor.code] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor.code))
                    parent_map[neighbor.code] = current_code
        
        # Construct the path and line changes
        path = []
        line_changes = []
        current = stop
        while current is not None:
            path.append(current)
            if parent_map[current] and self.stations[current].line != self.stations[parent_map[current]].line:
                line_changes.append((self.stations[parent_map[current]], self.stations[current]))
            current = parent_map[current]
        path.reverse()
        line_changes.reverse()
        return path, line_changes