from .claspy import *
from . import utils
from .utils.loops import *
from .utils.solutions import *

def encode(string):
    return utils.encode(string, clue_encoder = lambda s : s)
    
def solve(E):
    reset() 

    normal_sols = normal_yaji(E)
    one_off_sols = one_off_yaji(E)
    full_lane_sols = full_lane_yaji(E)
    clued_loop_sols = clued_loop_yaji(E)

    print('# normals =', len(normal_sols))
    print('# one off =', len(one_off_sols))
    print('# full lane =', len(full_lane_sols))
    print('# clued loop =', len(clued_loop_sols))

    return normal_sols + one_off_sols + full_lane_sols + clued_loop_sols


def normal_yaji(E):
    reset()
    set_max_val(max([int(clue[0][0])+1 for clue in E.clues.values() if clue != 'gray'], default=1))


    loop_solver = utils.RectangularGridLoopSolver(E.R, E.C, shading = True)
    shading_solver = utils.RectangularGridShadingSolver(
                        E.R, E.C, grid = loop_solver.grid, shading_symbols = ['.'])
    loop_solver.loop(E.clues, allow_blanks = False)
    shading_solver.no_adjacent()
    
    # ----CLUE RULES----
    
    for r in range(E.R):
        for c in range(E.C):
            # clues satisfied
            if (r, c) in E.clues:
                if E.clues[(r,c)] == 'gray':
                    require(loop_solver.grid[r][c] == '')
                else:
                    num_string = E.clues[(r,c)][0][0]
                    direction = E.clues[(r,c)][0][1]
                    # check the clue for validity
                    if not num_string.isnumeric() or direction not in 'lrud':
                        raise ValueError('Please ensure that each clue has both a number and a direction.')
                    
                    # build a list of coordinates that are "seen" by this clue
                    seen_cells = []
                    if direction == 'l':
                        seen_cells = [(r,x) for x in range(0, c)]
                    elif direction == 'r':
                        seen_cells = [(r,x) for x in range(c+1, E.C)]
                    elif direction == 'u':
                        seen_cells = [(y,c) for y in range(0, r)]
                    elif direction == 'd':
                        seen_cells = [(y,c) for y in range(r+1, E.R)]
                    # get a list of boolean variables that tell you whether the cells are shaded
                    shaded_seen = [BoolVar(loop_solver.grid[y][x] == '.') for (y,x) in seen_cells]
                    # require that exactly 'num' of the cells are shaded
                    require(sum_bools(int(num_string), shaded_seen))
    
    return loop_solver.solutions()

def one_off_yaji(E): 
    reset()
    set_max_val(100)

    loop_solver = utils.RectangularGridLoopSolver(E.R, E.C, shading = True)
    shading_solver = utils.RectangularGridShadingSolver(
                        E.R, E.C, grid = loop_solver.grid, shading_symbols = ['.'])
    loop_solver.loop(E.clues, allow_blanks = False)
    shading_solver.no_adjacent()
    
    # ----CLUE RULES----
    
    for r in range(E.R):
        for c in range(E.C):
            # clues satisfied
            if (r, c) in E.clues:
                if E.clues[(r,c)] == 'gray':
                    require(loop_solver.grid[r][c] == '')
                else:
                    num_string = E.clues[(r,c)][0][0]
                    direction = E.clues[(r,c)][0][1]
                    # check the clue for validity
                    if not num_string.isnumeric() or direction not in 'lrud':
                        raise ValueError('Please ensure that each clue has both a number and a direction.')
                    
                    # build a list of coordinates that are "seen" by this clue
                    seen_cells = []
                    if direction == 'l':
                        seen_cells = [(r,x) for x in range(0, c)]
                    elif direction == 'r':
                        seen_cells = [(r,x) for x in range(c+1, E.C)]
                    elif direction == 'u':
                        seen_cells = [(y,c) for y in range(0, r)]
                    elif direction == 'd':
                        seen_cells = [(y,c) for y in range(r+1, E.R)]
                    # get a list of boolean variables that tell you whether the cells are shaded
                    shaded_seen = [BoolVar(loop_solver.grid[y][x] == '.') for (y,x) in seen_cells]
                    # require that exactly 'num' of the cells are shaded
                    if int(num_string) > 0:
                        require(sum_bools(int(num_string)+1, shaded_seen) | sum_bools(int(num_string)-1, shaded_seen))
                    # else:
                    #     require(sum_bools(1, shaded_seen))

    
    return loop_solver.solutions()


def full_lane_yaji(E):
    reset()
    set_max_val(max([int(clue[0][0])+1 for clue in E.clues.values() if clue != 'gray'], default=1))


    loop_solver = utils.RectangularGridLoopSolver(E.R, E.C, shading = True)
    shading_solver = utils.RectangularGridShadingSolver(
                        E.R, E.C, grid = loop_solver.grid, shading_symbols = ['.'])
    loop_solver.loop(E.clues, allow_blanks = False)
    shading_solver.no_adjacent()
    
    # ----CLUE RULES----
    
    for r in range(E.R):
        for c in range(E.C):
            # clues satisfied
            if (r, c) in E.clues:
                if E.clues[(r,c)] == 'gray':
                    require(loop_solver.grid[r][c] == '')
                else:
                    num_string = E.clues[(r,c)][0][0]
                    direction = E.clues[(r,c)][0][1]
                    # check the clue for validity
                    if not num_string.isnumeric() or direction not in 'lrud':
                        raise ValueError('Please ensure that each clue has both a number and a direction.')
                    
                    # build a list of coordinates that are "seen" by this clue
                    seen_cells = []
                    if direction == 'l':
                        seen_cells = [(r,x) for x in range(0, E.C)]
                    elif direction == 'r':
                        seen_cells = [(r,x) for x in range(0, E.C)]
                    elif direction == 'u':
                        seen_cells = [(y,c) for y in range(0, E.R)]
                    elif direction == 'd':
                        seen_cells = [(y,c) for y in range(0, E.R)]
                    # get a list of boolean variables that tell you whether the cells are shaded
                    shaded_seen = [BoolVar(loop_solver.grid[y][x] == '.') for (y,x) in seen_cells]
                    # require that exactly 'num' of the cells are shaded
                    require(sum_bools(int(num_string), shaded_seen))
    
    return loop_solver.solutions()

def clued_loop_yaji(E):
    reset()
    set_max_val(max([int(clue[0][0])+1 for clue in E.clues.values() if clue != 'gray'], default=1))


    loop_solver = utils.RectangularGridLoopSolver(E.R, E.C, shading = True)
    shading_solver = utils.RectangularGridShadingSolver(
                        E.R, E.C, grid = loop_solver.grid, shading_symbols = ['.'])
    loop_solver.loop(E.clues, allow_blanks = False)
    shading_solver.no_adjacent()
    
    # ----CLUE RULES----
    
    for r in range(E.R):
        for c in range(E.C):
            # clues satisfied
            if (r, c) in E.clues:
                if E.clues[(r,c)] == 'gray':
                    require(loop_solver.grid[r][c] == '')
                else:
                    num = E.clues[(r,c)][0][0]
                    d = E.clues[(r,c)][0][1]
                    # check the clue for validity
                    if not num.isnumeric() or d not in 'lrud':
                        raise ValueError('Please ensure that each clue has both a number and a direction.')
                    
                    # build a list of coordinates that are "seen" by this clue
                    seen_cells = []
                    if d == 'u':
                        require(sum_bools(int(num), [var_in(loop_solver.grid[y][c], 
                            DOWN_CONNECTING) for y in range(r-1)]))
                    elif d == 'r':
                        require(sum_bools(int(num), [var_in(loop_solver.grid[r][x], 
                            RIGHT_CONNECTING) for x in range(c+1, E.C-1)]))
                    elif d == 'd':
                        require(sum_bools(int(num), [var_in(loop_solver.grid[y][c], 
                            DOWN_CONNECTING) for y in range(r+1, E.R-1)]))
                    elif d == 'l':
                        require(sum_bools(int(num), [var_in(loop_solver.grid[r][x], 
                            RIGHT_CONNECTING) for x in range(c-1)]))
    
    return loop_solver.solutions()

def decode(solutions):
    return utils.decode(solutions)
