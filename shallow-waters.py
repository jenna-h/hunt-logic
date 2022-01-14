from .claspy import *
from . import utils
from .utils.regions import *
from .utils.solutions import *

def encode(string):
    return utils.encode(string, clue_encoder = lambda s : s, has_borders=True) 
    
def solve(E):
    #TODO
    set_max_val(100)

    print(E.edges)

    rooms = full_bfs(15, 21, E.edges)
    grid = [[MultiVar('-', '.') for c in range(21)] for r in range(15)]
    
    # one type of item in each
    for room in rooms:
        for (r, c) in room:
            room_value = grid[r][c]
            break
        all_have_value = True
        for (r, c) in room:
            all_have_value &= (grid[r][c] == room_value)
        require(all_have_value)

    # edge nums
    for c in E.top:
        require(sum_bools(int(E.top[c]), [grid[r][c] == '-' for r in range(15)]))
    for r in E.left:
        require(sum_bools(int(E.left[r]), [grid[r][c] == '-' for c in range(21)]))

    # no 2x2 of pool noodles
    for r in range(15-1):
        for c in range(21-1):
            require(
                at_most(3, [grid[r][c] == '-',
                grid[r+1][c] == '-',
                grid[r][c+1] == '-',
                grid[r+1][c+1] == '-'])
            )
    
    return get_all_grid_solutions(grid)

def decode(solutions):
    return utils.decode(solutions)
