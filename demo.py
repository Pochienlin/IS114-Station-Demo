from MRT_Classes import Station, MetroMap
from sgMrt import stations_data


# Create a MetroMap instance
mrt_map = MetroMap(stations_data)
# print(mrt_map.stations["EW 10"])
# print(mrt_map)




res_path, res_changes = mrt_map.find_shortest_path("CG 1", "EW 10")

print(f"Path: {res_path}")
print(f"Change: {[(item[0].__str__(), item[1].__str__()) for item in res_changes]}")