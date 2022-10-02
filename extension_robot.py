import math
import random
import copy
from matplotlib import pyplot
from matplotlib import colors
from base import create_grid, get_it_next_move_direction,get_closest_prey,is_prey_in_vicinty,get_from_yaml,get_it_next_move_vicinity


def get_farthest_from_source(moves, original_it_loc, dim_x,dim_y):
    max_dist = float('-inf')
    for move in moves:
        distance = math.sqrt(
            sum([(a - b) ** 2 for a, b in zip(move, original_it_loc)]))
        if distance > max_dist:
            max_dist = distance
            farthest_move = move
    return farthest_move


def get_next_move_prey(pry_locs, original_it_loc, dim_x,dim_y):
    moves = []
    all_moves = [[1, 0],
                 [0, 1],
                 [-1, 0],
                 [0, -1]]
    for a_move in all_moves:
        child_x = pry_locs[0] + a_move[0]
        child_y = pry_locs[1] + a_move[1]
        if (child_x > dim_x-1 or child_x < 0 or child_y > dim_y-1 or child_y < 0):
            continue
        else:
            moves.append((child_x, child_y))

    return get_farthest_from_source(moves, original_it_loc, dim_x,dim_y)


def is_any_prey_in_vicinity(source, destinations, dim_x,dim_y):
    for dest in destinations:
        res = is_prey_in_vicinty(source, dest, dim_x,dim_y)
        if res:
            return True, dest
    return False, None




def get_it_next_move_vicinity_extension(it_starting_location, preymove, dim_x,dim_y):
    overlap=get_it_next_move_vicinity(it_starting_location, preymove, dim_x,dim_y)
    return random.sample(overlap, 2) if len(overlap) >= 2 else overlap


def is_source_in_vicinity(next_move_it, pre_move, dim_x,dim_y):
    distance = math.sqrt(
        sum([(a - b) ** 2 for a, b in zip(next_move_it, pre_move)]))
    return False if distance > 1 else True


def main():
    dim_x,dim_y,it_starting_location,prey_starting_locations=get_from_yaml()

    colours = { "IT": 1, "PREY":2, "FROZEN": 3 }
    cmap1 = colors.ListedColormap(['violet', 'green','yellow'])
    cmap2 = colors.ListedColormap(['violet', 'green','yellow','red'])
    grid = create_grid(dim_x,dim_y)
    
    im = None
    pltGrid = copy.deepcopy(grid)
    pltGrid[it_starting_location[0]][it_starting_location[1]] = colours["IT"]
    for prey_locs in prey_starting_locations:
        pltGrid[prey_locs[0]][prey_locs[1]] = colours["PREY"]
    pyplot.figure(figsize=(5, 5))
    pyplot.grid()
    im = None


    frozen_location_map = {}
    next_move_it = it_starting_location
    next_move_prey = prey_starting_locations
    freezecount = 0
    preycount = len(prey_starting_locations)
    total_moves = 0
    started_freeze=0

    freeze_locations_grid = [[0]*dim_x for i in range(dim_y)]

    while freezecount != preycount:
        original_it_loc = next_move_it
        """
        Running the "it" robot
        """
        # check if any prey is in vicinity
        prey_in_vicinity, dest = is_any_prey_in_vicinity(
            next_move_it, next_move_prey, dim_x,dim_y)
        # if any prey is in vicinity, get two moves from the intersection of the it and prey next possible move
        if prey_in_vicinity:
            next_move_it = get_it_next_move_vicinity_extension(
                next_move_it, dest, dim_x,dim_y)
            # if length of intersection is one, get the next move from the intersection of the first_move_it(new source) and prey next possible move
            if len(next_move_it) == 1:
                first_move_it = next_move_it[0]
                next_move_it_random = get_it_next_move_vicinity_extension(
                    first_move_it, dest, dim_x,dim_y)
                next_move_it.append(random.choice(next_move_it_random))
        # not in vicity
        else:

            temp_next_move_it = []
            # run towards the closest prey
            closest_prey = get_closest_prey(
                next_move_it, next_move_prey)
            next_dir = get_it_next_move_direction(
                next_move_it, closest_prey)
            temp_next_move_it.append((next_move_it[0]+next_dir[0],
                                      next_move_it[1]+next_dir[1]))
            prey_in_vicinity, dest = is_any_prey_in_vicinity(
                temp_next_move_it[0], next_move_prey, dim_x,dim_y)
            # to get the next move , either prey is more far away or in vicinity. If it is in vicinity again get the intersection
            if prey_in_vicinity:
                next_move_it_random = get_it_next_move_vicinity_extension(
                    temp_next_move_it[0], dest, dim_x,dim_y)
                temp_next_move_it.append(random.choice(next_move_it_random))
            #prey is far
            else:
                closest_prey = get_closest_prey(
                    temp_next_move_it[0], next_move_prey)
                next_dir = get_it_next_move_direction(
                    temp_next_move_it[0], closest_prey)
                temp_next_move_it.append((temp_next_move_it[0][0]+next_dir[0],
                                          temp_next_move_it[0][1]+next_dir[1]))
            next_move_it = temp_next_move_it

        """
        Running the prey robots
        """
        for i in range(len(next_move_prey)):
            next_move_prey[i] = get_next_move_prey(
                next_move_prey[i], original_it_loc, dim_x,dim_y)

        pltGrid = [[0]*dim_x for i in range(dim_y)]
        pltGrid[next_move_it[1][0]][next_move_it[1][1]] = colours["IT"]
        for prey_locs in next_move_prey:
            pltGrid[prey_locs[0]][prey_locs[1]] = colours["PREY"]

        temp_next_move_prey = copy.deepcopy(next_move_prey)
        for move in temp_next_move_prey:
            if move in next_move_it:
                frozen_location_map[move] = 1+frozen_location_map.get(move, 0)
                started_freeze =1
                freezecount += 1
                freeze_locations_grid[move[0]][move[1]] = colours["FROZEN"]
                next_move_prey.remove(move)

        next_move_it = next_move_it[1]
        temp_next_move_prey = copy.deepcopy(next_move_prey)
        for move in temp_next_move_prey:
            if move in frozen_location_map and not is_source_in_vicinity(next_move_it, move, dim_x,dim_y):
                # unfreeze other robots
                frozen_robots = frozen_location_map[move]
                for _ in range(frozen_robots):
                    next_move_prey.append(move)
                    frozen_location_map[move] -= 1
                    freezecount -= 1
                    freeze_locations_grid[move[0]][move[1]] = 0
                    pltGrid[move[0]][move[1]] = colours["PREY"]


                # freeze itself
                frozen_location_map[move] = 1+frozen_location_map.get(move, 0)
                freezecount += 1
                freeze_locations_grid[move[0]][move[1]] = colours["FROZEN"]
                next_move_prey.remove(move)
        
        for i in range(dim_y):
            for j in range(dim_x):
                if freeze_locations_grid[i][j] == colours["FROZEN"]:
                    pltGrid[i][j] = colours["FROZEN"]
        
        pyplot.imshow(pltGrid)
        if (im is None):
            
            im = pyplot.imshow(pltGrid)
            
        else:
            im.set_data(pltGrid)
        
        if started_freeze!=1:
            pyplot.pcolormesh(pltGrid,cmap=cmap1,edgecolors='k',linewidth=2)
        else:
            pyplot.pcolormesh(pltGrid,cmap=cmap2,edgecolors='k',linewidth=2)
            
        pyplot.ylim([0,dim_y])
        pyplot.xlim([0,dim_y])
        pyplot.pause(1)
        total_moves += 1

    pyplot.waitforbuttonpress(timeout=10)
    print("total_moves", total_moves)
    print("frozen_location_map",frozen_location_map)


main()
