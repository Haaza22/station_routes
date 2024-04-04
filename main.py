# Input:
# Start station and location (Example: Victoria outside station)
# AND
# Destination (Example: London Bridge)
# AND (if applicable)
# Accessibility level (can/cannot use stairs)
#
# Output:
# Underground route: (Example, northbound to X on Y (colour Z) change at W and so on)
# Station pathing route: (at the branch go left through the ticket gate, also need )

import stations as ST


# Station has class for lines and stations, and all initialised

def overall_path(start, start_loc, end, access):
    # Start is the start station in "STN" form
    # Start Loc is in the form SS_DD
    # End is end station level
    # Access is accessability level

    start_station = ST.station_list[start]
    station_end = ST.station_list[end]
    # Underground route is numbers
    underground_route, changes = dijkstra_stations(start_station.num, station_end.num)

    changes[0][1] = start_loc
    station_path_route = []
    for i in range(0, len(changes)):
        cur_station = ST.station_num_to_object(changes[i][0])
        to_apnd = cur_station.station_pathing_routes(changes[i][1], changes[i][2], access)
        station_path_route.append(to_apnd)

    return underground_route, station_path_route


# A* or Dijkstra on a 2D matrix of stations, and their connections. each stop a weight of 1
def dijkstra_stations(start, end):
    graph = ST.station_matrix
    lines = ST.lines_matrix
    # Number of vertices in the graph
    vertices = len(graph)
    distance = [float('inf')] * vertices
    distance[start] = 0
    visited = set()
    predecessor = {}
    # For swappung lines
    line_swap_penalty = 2
    changes = []

    # Dijkstra's algorithm
    while True:
        # Find the vertex with the minimum distance that is not yet visited
        min_distance = float('inf')
        for v in range(vertices):
            if distance[v] < min_distance and v not in visited:
                min_distance = distance[v]
                current_vertex = v

        # Mark the current vertex as visited
        visited.add(current_vertex)
        if current_vertex is None or current_vertex == end:
            break

        # Update distances from start to all its neighbors
        for v in range(vertices):
            if graph[current_vertex][v] > 0:  # If there's a connection
                new_distance = distance[current_vertex] + graph[current_vertex][v]
                if current_vertex in predecessor:
                    prev_vertex = predecessor[current_vertex]
                    if lines[prev_vertex][current_vertex] != lines[current_vertex][v]:
                        new_distance = new_distance + line_swap_penalty  # Add penalty
                        changes.append(
                            (current_vertex, v, lines[prev_vertex][current_vertex], lines[current_vertex][v]))

                if new_distance < distance[v]:
                    # if the path is better then update
                    distance[v] = new_distance
                    predecessor[v] = current_vertex

    # Construct the shortest path from start to end
    route_calcing = []
    vertex = end
    while vertex is not None:
        route_calcing.append(vertex)
        vertex = predecessor.get(vertex, None)
    route_calcing.reverse()

    # Only include changes if they are used
    path_set = set(route_calcing)
    changes = [(start_st, end_st, line_1, line_2) for start_st, end_st, line_1, line_2 in changes if
               end_st in path_set and start_st in path_set]
    # Dijkstra done, now analysing

    # Return needs to be "Station, this line (line colour), this direction (to X), this many stops"
    # All one line
    line_order = []
    cur_changes = 0
    stations_gone = 0
    if len(changes) == 0:
        # If theres no change
        cur_line = lines[route_calcing[0]][route_calcing[1]]
        swap_time = len(route_calcing) - 1
        line_order.append([cur_line, swap_time])
    else:
        # If theres a change
        for i in range(0, len(route_calcing)):
            if route_calcing[i] == changes[cur_changes][0]:
                cur_line = lines[route_calcing[i - 1]][route_calcing[i]]
                line_order.append([cur_line, stations_gone])
                stations_gone = 0
            else:
                stations_gone = stations_gone + 1
        cur_line = lines[route_calcing[i - 1]][route_calcing[i]]
        line_order.append([cur_line, stations_gone])

    name_list = []
    for stop in route_calcing:
        name_list.append(ST.station_num_to_name(stop))

    presented = []
    total_stops = 0
    # needs to have: station num, start in str, end in str
    d, _ = ST.lines_dir_and_bound(route_calcing[0], route_calcing[1], line_order[0][0])

    station_route = [[start, 0, ST.plat_change_calc_depth(line_order[0][0], d)]]
    direction = -1
    bound = -1
    changes_done=0
    for i in range(0, len(line_order)):
        total_stops = total_stops + line_order[i][1]
        # Start
        if i == 0:
            cur_msg = "First get on "
        else:
            cur_msg = "Change to the "
        # Line, colour, direction, bound to, stops, platform off
        # Line
        cur_msg = cur_msg + ST.line_num_to_name(line_order[i][0]) + " line"
        # colour
        cur_msg = cur_msg + " (" + ST.line_num_to_col(line_order[i][0]) + ")"
        # get direction and bound
        old_direction = direction
        direction, bound = ST.lines_dir_and_bound(route_calcing[total_stops - line_order[i][1]],
                                                  route_calcing[total_stops],
                                                  line_order[i][0])
        if i > 0:
            # getting all changes for thing
            old_line = line_order[i - 1][0]
            start_point, end_point = ST.plat_change_calc(line_order[i][0], direction, old_line, old_direction)
            station_route.append([changes[changes_done][0], start_point, end_point])
            changes_done=changes_done+1
        # Direction
        cur_msg = cur_msg + " " + direction
        # Bound
        cur_msg = cur_msg + " to " + bound
        # Stops
        if line_order[i][1] == 1:
            cur_msg = cur_msg + " for " + str(line_order[i][1]) + " stop"
        else:
            cur_msg = cur_msg + " for " + str(line_order[i][1]) + " stops"
        # Station to
        cur_msg = cur_msg + " to " + str(name_list[total_stops])
        # Add msg
        presented.append(cur_msg)

    # Presented is the overall undergound route
    # Changes is used to calc to station routes, so it says from [VI_NB,BK_NB] and such
    return presented, station_route


# print(ST.BK.name_full)
# print(ST.line_list["BK"].name_full)
# Test for Vic to Kings cross
# print()
# for row in ST.station_matrix:
#     print(row)
# print()
# for row in ST.lines_matrix:
#     print(row)
# print()

underground_route, station_route_presented = overall_path("VIC", "OV_GR", "KNG", 1)
print(underground_route)
print(station_route_presented)

print()

underground_route_presented, station_route_presented = overall_path("VIC", "OV_GR", "PAD", 1)
print(underground_route_presented)
print(station_route_presented)

# To get a route and such, call function overall_path
# This function takes the 3 letter station code of start station, the 5 letter start location of said start station
# the 3 letter station code of end station then the accessability level
# It returns: underground_route, station_route
# Both of these are arrays of strings, being the instructions in order step by step. Underground route is the
# one where is like 'get on victoria line for 20 stops then change here'. station_route is how to get around on
# the station, how to get from overground to northbound victoria, then at the other station how to get from
# northbound victoria to southbound bakerloo. that sort of thing