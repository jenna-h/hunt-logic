from .claspy import *
from . import utils
from .utils.solutions import *

def encode(string):
    return utils.encode(string)
    
def solve(E):
    # std_sols = solve_std(E)
    prod_sols = solve_prod(E)
    mine_sols = solve_mine(E)
    diag_sols = solve_diag(E)
    small_sols = solve_small(E)
    no_black_2x2_sols = solve_no_black_2x2(E)
    even_sols = solve_even(E)

    # print('num_std_sols =', len(std_sols))
    print('num_prod_sols =', len(prod_sols))
    print('num_mine_sols =', len(mine_sols))
    print('num_diag_sols =', len(diag_sols))
    print('num_small_sols =', len(small_sols))
    print('num_no_black_2x2_sols =', len(no_black_2x2_sols))
    print('num_even_sols =', len(even_sols))

    sol_viewer = prod_sols[:2] + mine_sols[:2] + \
        diag_sols[:2] + small_sols[:2] + \
        no_black_2x2_sols[:2] + even_sols[:2]
    
    return sol_viewer

def solve_std(E):
    reset()
    set_max_val(E.R*E.C)

    shading_solver = utils.RectangularGridShadingSolver(E.R,E.C)
    shading_solver.white_connectivity()
    shading_solver.black_edge_connectivity()
    shading_solver.white_clues(E.clues)

    # GIVEN NUMBERS ARE SATISFIED
    for (r,c) in E.clues:
        dirs = {}
        for (u,v) in ((1,0),(-1,0),(0,1),(0,-1)):
            ray = []
            n = 1
            while 0 <= r+u*n < E.R and 0 <= c+v*n < E.C: # add all ray cells
                ray.append((r+u*n,c+v*n))
                n += 1
            num_seen_cells = IntVar(0, len(ray))
            for n in range(len(ray)+1):
                cond_n = BoolVar(True)
                for d in range(n):
                    cond_n &= (~shading_solver.grid[ray[d]])
                if n < len(ray):
                    cond_n &= shading_solver.grid[ray[n]]
                require((num_seen_cells == n) == cond_n)
            dirs[(u,v)] = num_seen_cells

        require(dirs[(1,0)]+dirs[(-1,0)]+dirs[(0,1)]+dirs[(0,-1)] == E.clues[(r,c)]-1)
      
    return shading_solver.solutions()


def solve_prod(E):
    reset()
    set_max_val(E.R*E.C)

    shading_solver = utils.RectangularGridShadingSolver(E.R,E.C)
    shading_solver.white_connectivity()
    shading_solver.black_edge_connectivity()
    shading_solver.white_clues(E.clues)

    # GIVEN NUMBERS ARE SATISFIED
    for (r,c) in E.clues:
        dirs = {}
        for (u,v) in ((1,0),(-1,0),(0,1),(0,-1)):
            ray = []
            n = 1
            while 0 <= r+u*n < E.R and 0 <= c+v*n < E.C: # add all ray cells
                ray.append((r+u*n,c+v*n))
                n += 1
            num_seen_cells = IntVar(0, len(ray))
            for n in range(len(ray)+1):
                cond_n = BoolVar(True)
                for d in range(n):
                    cond_n &= (~shading_solver.grid[ray[d]])
                if n < len(ray):
                    cond_n &= shading_solver.grid[ray[n]]
                require((num_seen_cells == n) == cond_n)
            dirs[(u,v)] = num_seen_cells

        # use product rule
        cond_product = BoolVar(False) # unwind the product (so claspy works correctly)
        for (a,b) in utils.numbers.factor_pairs(E.clues[(r,c)]):
            cond_product |= (
                (dirs[(1,0)]+dirs[(-1,0)] == a-1) &
                (dirs[(0,1)]+dirs[(0,-1)] == b-1)
            )
        require(cond_product)

    return shading_solver.solutions()


def solve_mine(E):
    reset()
    set_max_val(E.R*E.C)

    shading_solver = utils.RectangularGridShadingSolver(E.R,E.C)
    shading_solver.white_connectivity()
    shading_solver.black_edge_connectivity()
    shading_solver.white_clues(E.clues)

    # GIVEN NUMBERS ARE SATISFIED
    for (r,c) in E.clues:
        dirs = {}
        require(sum_bools(E.clues[(r,c)], 
            [shading_solver.grid[y][x] for (y,x) in utils.grids.get_surroundings(E.R, E.C, r, c)]))

    return shading_solver.solutions()

def solve_joker(E):
    reset()
    set_max_val(E.R*E.C)

    shading_solver = utils.RectangularGridShadingSolver(E.R,E.C)
    shading_solver.white_connectivity()
    shading_solver.black_edge_connectivity()
    shading_solver.white_clues(E.clues)

    is_joker = {value: BoolVar() for value in E.clues.values()}
 
    # GIVEN NUMBERS ARE SATISFIED
    for (r,c) in E.clues:
        dirs = {}
        for (u,v) in ((1,0),(-1,0),(0,1),(0,-1)):
            ray = []
            n = 1
            while 0 <= r+u*n < E.R and 0 <= c+v*n < E.C: # add all ray cells
                ray.append((r+u*n,c+v*n))
                n += 1
            num_seen_cells = IntVar(0, len(ray))
            for n in range(len(ray)+1):
                cond_n = BoolVar(True)
                for d in range(n):
                    cond_n &= (~shading_solver.grid[ray[d]])
                if n < len(ray):
                    cond_n &= shading_solver.grid[ray[n]]
                require((num_seen_cells == n) == cond_n)
            dirs[(u,v)] = num_seen_cells

        require((dirs[(1,0)]+dirs[(-1,0)]+dirs[(0,1)]+dirs[(0,-1)] == E.clues[(r,c)]-1) | 
            is_joker[E.clues[(r,c)]]
        )

    # Exactly 1 joker value
    require(sum_bools(1, [is_joker[value] for value in is_joker])) 

    return shading_solver.solutions()

def solve_no_black_2x2(E):
    reset()
    set_max_val(E.R*E.C)

    shading_solver = utils.RectangularGridShadingSolver(E.R,E.C)
    shading_solver.white_connectivity()
    shading_solver.black_edge_connectivity()
    shading_solver.white_clues(E.clues)
    shading_solver.no_black_2x2()

    # GIVEN NUMBERS ARE SATISFIED
    for (r,c) in E.clues:
        dirs = {}
        for (u,v) in ((1,0),(-1,0),(0,1),(0,-1)):
            ray = []
            n = 1
            while 0 <= r+u*n < E.R and 0 <= c+v*n < E.C: # add all ray cells
                ray.append((r+u*n,c+v*n))
                n += 1
            num_seen_cells = IntVar(0, len(ray))
            for n in range(len(ray)+1):
                cond_n = BoolVar(True)
                for d in range(n):
                    cond_n &= (~shading_solver.grid[ray[d]])
                if n < len(ray):
                    cond_n &= shading_solver.grid[ray[n]]
                require((num_seen_cells == n) == cond_n)
            dirs[(u,v)] = num_seen_cells

        require(dirs[(1,0)]+dirs[(-1,0)]+dirs[(0,1)]+dirs[(0,-1)] == E.clues[(r,c)]-1)
      
    return shading_solver.solutions()

def solve_lying(E):
    reset()
    set_max_val(E.R*E.C)

    shading_solver = utils.RectangularGridShadingSolver(E.R,E.C)
    shading_solver.white_connectivity()
    shading_solver.black_edge_connectivity()
    shading_solver.white_clues(E.clues)

    # GIVEN NUMBERS ARE SATISFIED
    for (r,c) in E.clues:
        dirs = {}
        for (u,v) in ((1,0),(-1,0),(0,1),(0,-1)):
            ray = []
            n = 1
            while 0 <= r+u*n < E.R and 0 <= c+v*n < E.C: # add all ray cells
                ray.append((r+u*n,c+v*n))
                n += 1
            num_seen_cells = IntVar(0, len(ray))
            for n in range(len(ray)+1):
                cond_n = BoolVar(True)
                for d in range(n):
                    cond_n &= (~shading_solver.grid[ray[d]])
                if n < len(ray):
                    cond_n &= shading_solver.grid[ray[n]]
                require((num_seen_cells == n) == cond_n)
            dirs[(u,v)] = num_seen_cells

        require(dirs[(1,0)]+dirs[(-1,0)]+dirs[(0,1)]+dirs[(0,-1)] != E.clues[(r,c)]-1)
      
    return shading_solver.solutions()

def solve_cover(E):
    reset()
    set_max_val(E.R*E.C)

    shading_solver = utils.RectangularGridShadingSolver(E.R,E.C)
    shading_solver.white_connectivity()
    shading_solver.black_edge_connectivity()

    is_shaded = {clue: BoolVar() for clue in E.clues}

    # GIVEN NUMBERS ARE SATISFIED
    for (r,c) in E.clues:
        dirs = {}
        for (u,v) in ((1,0),(-1,0),(0,1),(0,-1)):
            ray = []
            n = 1
            while 0 <= r+u*n < E.R and 0 <= c+v*n < E.C: # add all ray cells
                ray.append((r+u*n,c+v*n))
                n += 1
            num_seen_cells = IntVar(0, len(ray))
            for n in range(len(ray)+1):
                cond_n = BoolVar(True)
                for d in range(n):
                    cond_n &= (~shading_solver.grid[ray[d]])
                if n < len(ray):
                    cond_n &= shading_solver.grid[ray[n]]
                require((num_seen_cells == n) == cond_n)
            dirs[(u,v)] = num_seen_cells

        require((dirs[(1,0)]+dirs[(-1,0)]+dirs[(0,1)]+dirs[(0,-1)] == E.clues[(r,c)]-1) |
            is_shaded[(r,c)])
      
    return shading_solver.solutions()
   

def solve_diag(E):
    reset()
    set_max_val(E.R*E.C)

    shading_solver = utils.RectangularGridShadingSolver(E.R,E.C)
    shading_solver.white_connectivity()
    shading_solver.black_edge_connectivity()
    shading_solver.white_clues(E.clues)

    # GIVEN NUMBERS ARE SATISFIED
    for (r,c) in E.clues:
        dirs = {}
        for (u,v) in ((1,0),(-1,0),(0,1),(0,-1), 
                (1,1), (1,-1), (-1,1), (-1,-1)):
            ray = []
            n = 1
            while 0 <= r+u*n < E.R and 0 <= c+v*n < E.C: # add all ray cells
                ray.append((r+u*n,c+v*n))
                n += 1
            num_seen_cells = IntVar(0, len(ray))
            for n in range(len(ray)+1):
                cond_n = BoolVar(True)
                for d in range(n):
                    cond_n &= (~shading_solver.grid[ray[d]])
                if n < len(ray):
                    cond_n &= shading_solver.grid[ray[n]]
                require((num_seen_cells == n) == cond_n)
            dirs[(u,v)] = num_seen_cells

        require(dirs[(1,0)]+dirs[(-1,0)]+dirs[(0,1)]+dirs[(0,-1)]+\
            dirs[(1,1)]+dirs[(1,-1)]+dirs[(-1,1)]+dirs[(-1,-1)] == E.clues[(r,c)]-1)
      
    return shading_solver.solutions()

def solve_small(E):
    reset()
    set_max_val(E.R*E.C)

    shading_solver = utils.RectangularGridShadingSolver(E.R,E.C)
    shading_solver.white_connectivity()
    shading_solver.black_edge_connectivity()
    shading_solver.white_clues(E.clues)

    # GIVEN NUMBERS ARE SATISFIED
    for (r,c) in E.clues:
        dirs = {}
        for (u,v) in ((1,0),(-1,0),(0,1),(0,-1)):
            ray = []
            n = 1
            while 0 <= r+u*n < E.R and 0 <= c+v*n < E.C: # add all ray cells
                ray.append((r+u*n,c+v*n))
                n += 1
            num_seen_cells = IntVar(0, len(ray))
            for n in range(len(ray)+1):
                cond_n = BoolVar(True)
                for d in range(n):
                    cond_n &= (~shading_solver.grid[ray[d]])
                if n < len(ray):
                    cond_n &= shading_solver.grid[ray[n]]
                require((num_seen_cells == n) == cond_n)
            dirs[(u,v)] = num_seen_cells

        require(dirs[(1,0)]+dirs[(-1,0)]+dirs[(0,1)]+dirs[(0,-1)] == E.clues[(r,c)])
      
    return shading_solver.solutions()

def solve_even(E):
    reset()
    set_max_val(E.R*E.C)

    shading_solver = utils.RectangularGridShadingSolver(E.R,E.C)
    shading_solver.white_connectivity()
    shading_solver.black_edge_connectivity()
    shading_solver.white_clues(E.clues)

    # GIVEN NUMBERS ARE SATISFIED
    for (r,c) in E.clues:
        dirs = {}
        for (u,v) in ((1,0),(-1,0),(0,1),(0,-1)):
            ray = []
            n = 1
            while 0 <= r+u*n < E.R and 0 <= c+v*n < E.C: # add all ray cells
                ray.append((r+u*n,c+v*n))
                n += 1
            num_seen_cells = IntVar(0, len(ray))
            for n in range(len(ray)+1):
                cond_n = BoolVar(True)
                for d in range(n):
                    cond_n &= (~shading_solver.grid[ray[d]])
                if n < len(ray):
                    cond_n &= shading_solver.grid[ray[n]]
                require((num_seen_cells == n) == cond_n)
            dirs[(u,v)] = num_seen_cells

        require(dirs[(1,0)]+dirs[(-1,0)]+dirs[(0,1)]+dirs[(0,-1)] == E.clues[(r,c)]-1)
    
    # Even
    for r in range(E.R):
        even_shaded = BoolVar(True)
        for c in range(E.C):
            even_shaded = (shading_solver.grid[r][c] & ~even_shaded) | \
                        (~shading_solver.grid[r][c] & even_shaded)
        require(even_shaded)

    for c in range(E.C):
        even_shaded = BoolVar(True)
        for r in range(E.R):
            even_shaded = (shading_solver.grid[r][c] & ~even_shaded) | \
                        (~shading_solver.grid[r][c] & even_shaded)
        require(even_shaded)

    return shading_solver.solutions()

def decode(solutions):
    return utils.decode(solutions)
