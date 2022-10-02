import random
import copy
from matplotlib import pyplot
from matplotlib import colors
from base import create_grid, get_it_next_move_direction,get_closest_prey,is_prey_in_vicinty,get_from_yaml,get_it_next_move_vicinity


def get_next_move_prey(pry_locs, dim_x,dim_y):
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
    return random.choice(moves)


def get_it_next_move_vicinity_original(it_starting_location, preymove, dim_x,dim_y):
    overlap=get_it_next_move_vicinity(it_starting_location, preymove, dim_x,dim_y)
    return random.choice(overlap)


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
        
    im = None

    next_move_it = it_starting_location
    next_move_prey = prey_starting_locations
    freezecount = 0
    preycount = len(prey_starting_locations)
    total_moves = 0
    freeze_locations_grid = [[0]*dim_x for i in range(dim_x)]
    started_freeze=0
    while freezecount != preycount:
        flag = 0
        for preymove in next_move_prey:
            if is_prey_in_vicinty(next_move_it, preymove, dim_x,dim_y):
                next_move_it = get_it_next_move_vicinity_original(next_move_it, preymove, dim_x,dim_y)
                flag = 1
                break
        if flag == 0:
            closest_prey = get_closest_prey(next_move_it, next_move_prey)
            next_dir = get_it_next_move_direction(next_move_it, closest_prey)
            next_move_it = (next_move_it[0]+next_dir[0], next_move_it[1]+next_dir[1])

        for i in range(len(next_move_prey)):
            next_move_prey[i] = get_next_move_prey(next_move_prey[i], dim_x,dim_y)
        print("next_move_it", next_move_it)
        print("next_move_prey", next_move_prey)

        pltGrid = [[0]*dim_x for i in range(dim_y)]
        pltGrid[next_move_it[0]][next_move_it[1]] = colours["IT"]
        for prey_locs in next_move_prey:
            pltGrid[prey_locs[0]][prey_locs[1]] = colours["PREY"]

        temp_next_move_prey = copy.deepcopy(next_move_prey)
        for move in temp_next_move_prey:
            if move == next_move_it:
                freezecount += 1
                freeze_locations_grid[move[0]][move[1]] = colours["FROZEN"]
                started_freeze=1
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
    


main()

