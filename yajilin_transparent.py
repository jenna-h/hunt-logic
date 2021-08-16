from .claspy import *
from . import utils

def encode(string):
    return utils.encode(string, clue_encoder = lambda s : s)

def solve(E):
    # Restrict the number of bits used for IntVar.
    # The highest number that we need is the highest clue number.
    if E.clues:
        set_max_val(max([int(clue[:-1]) for clue in E.clues.values()]))
    else:
        # set_max_val(0) DOES produce all of the valid 'solutions'...
        # but this isn't a puzzle! it's just an empty grid!!
        return []

    loop_solver = utils.RectangularGridLoopSolver(E.R, E.C, shading = True)
    shading_solver = utils.RectangularGridShadingSolver(
                        E.R, E.C, grid = loop_solver.grid, shading_symbols = ['.'])
    loop_solver.loop(E.clues, includes_clues = True, allow_blanks = False, transparent = True)
    shading_solver.no_adjacent()
    
    # ----CLUE RULES----
    
    for r in range(E.R):
        for c in range(E.C):
            # clues satisfied
            if (r, c) in E.clues:
                num = int(E.clues[(r,c)][:-1])
                direction = E.clues[(r,c)][-1]
                # build a list of coordinates that are "seen" by this clue
                seen_cells = []
                if direction == 'L':
                    seen_cells = [(r,x) for x in range(0, c)]
                elif direction == 'R':
                    seen_cells = [(r,x) for x in range(c+1, E.C)]
                elif direction == 'U':
                    seen_cells = [(y,c) for y in range(0, r)]
                elif direction == 'D':
                    seen_cells = [(y,c) for y in range(r+1, E.R)]
                # get a list of boolean variables that tell you whether the cells are shaded
                shaded_seen = [BoolVar(loop_solver.grid[y][x] == '.') for (y,x) in seen_cells]
                # require that exactly 'num' of the cells are shaded,
                # unless the clue cell itself is shaded
                require(sum_bools(num, shaded_seen) | (loop_solver.grid[r][c] == '.'))
    
    #TODO(someone): fix transparent Yajilin frontend
    return loop_solver.solutions()
    
def decode(solutions):
    return utils.decode(solutions)
