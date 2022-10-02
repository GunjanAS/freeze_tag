import math,yaml

def get_from_yaml():
    with open("input.yaml", "r") as stream:
        try:
            yaml_data=(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)

    dim_x = yaml_data['grid_x_size']
    dim_y=yaml_data['grid_y_size']
    it_starting_location = (yaml_data['it_starting_location']['x'], yaml_data['it_starting_location']['y'])
    prey_starting_locations = [(i['x'],i['y']) for i in yaml_data['prey_starting_locations']]
    return dim_x,dim_y,it_starting_location,prey_starting_locations

def create_grid(dim_x,dim_y):
    
    grid = [[0 for i in range(dim_x)] for j in range(dim_y)]
    return grid

def get_closest_prey(source, destinations):
    min_dist = float('inf')
    for destination in destinations:
        distance = math.sqrt(
            sum([(a - b) ** 2 for a, b in zip(source, destination)]))
        if distance < min_dist:
            min_dist = distance
            closest_dest = destination
    return closest_dest

def get_it_next_move_direction(source, destination):
    direction_map = {
        (0, "positive"): (0, -1),
        (0, "negative"): (0, 1),
        ("positive", 0): (-1, 0),
        ("negative", 0): (1, 0),
        ("positive", "positive"): (-1, -1),
        ("positive", "negative"): (-1, 1),
        ("negative", "negative"): (1, 1),
        ("negative", "positive"): (1, -1)
    }
    x1, y1 = source[0], source[1]
    x2, y2 = destination[0], destination[1]
    diffx = x1-x2
    diffy = y1-y2
    if diffx == 0:
        key1 = 0
    elif diffx > 0:
        key1 = "positive"
    else:
        key1 = "negative"
    if diffy == 0:
        key2 = 0
    elif diffy > 0:
        key2 = "positive"
    else:
        key2 = "negative"
    return direction_map[(key1, key2)]

def is_prey_in_vicinty(source, destinations, dim_x,dim_y):

    all_moves = [[1, 0],
                 [0, 1],
                 [-1, 0],
                 [0, -1],
                 [-1, -1],
                 [-1, 1],
                 [1, -1],
                 [1, 1]]
    for a_move in all_moves:
        child_x = source[0] + a_move[0]
        child_y = source[1] + a_move[1]
        if (child_x > dim_x-1 or child_x < 0 or child_y > dim_y-1 or child_y < 0):
            continue
        else:
            if (child_x, child_y) == destinations:
                return True
    return False

def get_it_next_move_vicinity(it_starting_location, preymove, dim_x,dim_y):
    all_moves_prey = [[1, 0],
                      [0, 1],
                      [-1, 0],
                      [0, -1]]
    all_moves_it = [[1, 0],
                    [0, 1],
                    [-1, 0],
                    [0, -1],
                    [-1, -1],
                    [-1, 1],
                    [1, -1],
                    [1, 1]]
    possible_it_nextmoves = []
    possible_prey_nextmoves = []
    for a_move in all_moves_prey:
        child_x = preymove[0] + a_move[0]
        child_y = preymove[1] + a_move[1]
        if (child_x > dim_x-1 or child_x < 0 or child_y > dim_y-1 or child_y < 0):
            continue
        else:
            possible_prey_nextmoves.append((child_x, child_y))
    for a_move in all_moves_it:
        child_x = it_starting_location[0] + a_move[0]
        child_y = it_starting_location[1] + a_move[1]
        if (child_x > dim_x-1 or child_x < 0 or child_y > dim_y-1 or child_y < 0):
            continue
        else:
            possible_it_nextmoves.append((child_x, child_y))
    overlap=list(set(possible_it_nextmoves) & set(possible_prey_nextmoves))
    return overlap