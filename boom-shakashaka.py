from .claspy import *
from . import utils
from .utils.solutions import *

def encode(string):
    return utils.encode(string)#, clue_encoder = lambda s : s)
    
def solve(E):
    #TODO
    set_max_val(9)
    
    tl = 'top-left.png'
    tr = 'top-right.png'
    bl = 'bottom-left.png'
    br = 'bottom-right.png'

    TRIANGLE_SYMBOLS = (tl, tr, bl, br)

    grid = [[MultiVar(*TRIANGLE_SYMBOLS, ' ', 'black') for c in range(E.C)] for r in range(E.R)]

    # Diagonal rectangles
    for r in range(E.R):
        for c in range(E.C):

            # ---- Upper-left triangle shading ----
            if utils.grids.is_valid_coord(E.R, E.C, r-1, c+1):
                # If this cell has upper-left triangle shading,
                require((grid[r][c] != tl) |
                    # The cell up and to the right of it is upper-left triangle,
                    # and the cell to the right of it is unshaded
                    ((grid[r-1][c+1] == tl) & (grid[r][c+1] == ' ')) |
                    # Or the cell immediately to the right is upper-right triangle.
                    (grid[r][c+1] == tr)
                )
            elif utils.grids.is_valid_coord(E.R, E.C, r, c+1):
                require((grid[r][c] != tl) |
                    # The cell immediately to the right is upper-right triangle.
                    (grid[r][c+1] == tr)
                )
            if utils.grids.is_valid_coord(E.R, E.C, r+1, c-1):
                require((grid[r][c] != tl) |
                    # The cell down and to the left of it is upper-left triangle,
                    # and the cell below it is unshaded.
                    ((grid[r+1][c-1] == tl) & (grid[r+1][c] == ' ')) |
                    # Or the cell immediately below is lower-left triangle.
                    (grid[r+1][c] == bl)
                )
            elif utils.grids.is_valid_coord(E.R, E.C, r+1, c):
                require((grid[r][c] != tl) |
                    # The cell immediately below is lower-left triangle.
                    (grid[r+1][c] == bl)
                )
            # Cells in the bottom row and rightmost column cannot have upper-left triangle shading. 
            if r == E.R-1 or c == E.C-1:
                require(grid[r][c] != tl)

            # ---- Upper-right triangle shading ----
            if utils.grids.is_valid_coord(E.R, E.C, r-1, c-1):
                require((grid[r][c] != tr) |
                    # The cell up and to the left of it is upper-right triangle,
                    # and the cell to the left of it is unshaded
                    ((grid[r-1][c-1] == tr) & (grid[r][c-1] == ' ')) |
                    # Or the cell immediately to the left is upper-left triangle.
                    (grid[r][c-1] == tl)
                )
            elif utils.grids.is_valid_coord(E.R, E.C, r, c-1):
                require((grid[r][c] != tr) |
                    # The cell immediately to the left is upper-left triangle.
                    (grid[r][c-1] == tl)
                )
            if utils.grids.is_valid_coord(E.R, E.C, r+1, c+1):
                require((grid[r][c] != tr) | 
                    ((grid[r][c] == tr) & (grid[r+1][c] == ' ')) |
                    (grid[r+1][c] == br)
                )
            elif utils.grids.is_valid_coord(E.R, E.C, r+1, c):
                require((grid[r][c] != tr) | 
                    (grid[r+1][c] == br)
                )
            if r == E.R-1 or c == 0:
                # Cannot be upper-right triangle.
                require(grid[r][c] != tr)

            # ---- Lower-left triangle shading ----
            if utils.grids.is_valid_coord(E.R, E.C, r+1, c+1):
                require((grid[r][c] != bl) |
                    ((grid[r+1][c+1] == bl) & (grid[r][c+1] == ' ')) |
                    (grid[r][c+1] == br)
                )
            elif utils.grids.is_valid_coord(E.R, E.C, r, c+1):
                require((grid[r][c] != bl) |
                    (grid[r][c+1] == br)
                )
            if utils.grids.is_valid_coord(E.R, E.C, r-1, c-1):
                require((grid[r][c] != bl) |
                    ((grid[r-1][c-1] == bl) & (grid[r-1][c] == ' ')) |
                    (grid[r-1][c] == tl)
                )
            elif utils.grids.is_valid_coord(E.R, E.C, r-1, c):
                require((grid[r][c] != bl) |
                    (grid[r-1][c] == tl)
                )
            if r == 0 or c == E.C-1:
                require(grid[r][c] != bl)
            
            # ---- Lower-right triangle shading ----
            if utils.grids.is_valid_coord(E.R, E.C, r+1, c-1):
                require((grid[r][c] != br) |
                    ((grid[r+1][c-1] == br) & (grid[r][c-1] == ' ')) |
                    (grid[r][c-1] == bl)
                )
            elif utils.grids.is_valid_coord(E.R, E.C, r, c-1):
                require((grid[r][c] != br) |
                    (grid[r][c-1] == bl)
                )
            if utils.grids.is_valid_coord(E.R, E.C, r-1, c+1):
                require((grid[r][c] != br) |
                    ((grid[r-1][c+1] == br) & (grid[r-1][c] == ' ')) |
                    (grid[r-1][c] == tr)
                )
            elif utils.grids.is_valid_coord(E.R, E.C, r-1, c):
                require((grid[r][c] != br) |
                    (grid[r-1][c] == tr)
                )
            if r == 0 or c == 0:
                require(grid[r][c] != br)

    # Grid-aligned rectangles
    for r in range(E.R):
        for c in range(E.C):
            # If there is a cell up and to the right
            if utils.grids.is_valid_coord(E.R, E.C, r-1, c+1):
                # If this cell, the cell above, and the cell to the right are all unshaded
                # The cell up and to the right must have an unshaded lower left
                require(
                    ~((grid[r][c] == ' ') & (grid[r-1][c] == ' ') & (grid[r][c+1] == ' ')) |
                    (var_in(grid[r-1][c+1], (' ', tr)))
                )
            # If there is a cell up and to the left
            if utils.grids.is_valid_coord(E.R, E.C, r-1, c-1):
                require(
                    ~((grid[r][c] == ' ') & (grid[r-1][c] == ' ') & (grid[r][c-1] == ' ')) |
                    (var_in(grid[r-1][c-1], (' ', tl)))
                )
            # If there is a cell down and to the right
            if utils.grids.is_valid_coord(E.R, E.C, r+1, c+1):
                require(
                    ~((grid[r][c] == ' ') & (grid[r+1][c] == ' ') & (grid[r][c+1] == ' ')) |
                    (var_in(grid[r+1][c+1], (' ', br)))
                )
            # If there is a cell down and to the left
            if utils.grids.is_valid_coord(E.R, E.C, r+1, c-1):
                require(
                    ~((grid[r][c] == ' ') & (grid[r+1][c] == ' ') & (grid[r][c-1] == ' ')) |
                    (var_in(grid[r+1][c-1], (' ', bl)))
                )

    # Clues!
    for (r, c) in E.clues:
        shakashaka_cond = sum_bools(E.clues[(r,c)],
                [var_in(grid[y][x], TRIANGLE_SYMBOLS) \
                    for (y, x) in utils.grids.get_neighbors(E.R, E.C, r, c)]
            ) & (grid[r][c] == 'black')
        minesweeper_cond = sum_bools(E.clues[(r, c)], 
            [grid[y][x] == 'black' for (y, x) in utils.grids.get_surroundings(E.R, E.C, r, c)]
        ) & (grid[r][c] != 'black')
        require(shakashaka_cond | minesweeper_cond)
    
    # special
    require(grid[5][0] == ' ')
        
    sols = utils.get_all_grid_solutions(grid)
    is_shaka_clue = []
    is_mine_clue = []
    for r in range(E.R):
        shaka_row = []
        mine_row = []
        for c in range(E.C):
            if (r, c) in E.clues:
                shaka_row.append(grid[r][c].value() == 'black')
                mine_row.append(grid[r][c].value() != 'black')
            else:
                shaka_row.append(False)
                mine_row.append(False)
        is_shaka_clue.append(shaka_row)
        is_mine_clue.append(mine_row)
    
    print('is shaka clue?')
    for r in is_shaka_clue:
        print('\t'.join(['True' if e else 'False' for e in r]))

    print()
    print() 

    print('is mine clue?')
    for r in is_mine_clue:
        print('\t'.join(['True' if e else 'False' for e in r]))

    print()
    print() 

    print('is black? (ie is mine?)')
    for r in range(E.R):
        print('\t'.join(['True' if grid[r][c].value() == 'black' else 'False' for c in range(E.C)]))

    print()
    print() 

    print('is black but not shaka clue')
    for r in range(E.R):
        print('\t'.join(['True' if grid[r][c].value() == 'black' and (r, c) not in E.clues \
            else 'False' for c in range(E.C)]))

    return sols

def decode(solutions):
    return utils.decode(solutions)
