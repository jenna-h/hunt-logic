from .claspy import *
from . import utils
from .utils import regions

# TODO(himawan)
# TODO(mstang)
#
# Make a good Sudoku frontend and parameterize this bad boy

def encode(string):
    return utils.encode(string, has_borders = True)

def solve(encoding):
    rows, cols, clues, border_coords = encoding
    rooms = regions.full_bfs(rows, cols, border_coords)
    
    grid = utils.RectangularGridNumbersSolver(9, 9, 1, 9)
    grid.rows_and_cols()
    grid.regions(rooms)

    for (r, c) in clues:
        require(grid.grid[r][c] == clues[(r,c)])
        
    require(grid.grid[0][1] + grid.grid[0][2] == grid.grid[1][2])
    require(grid.grid[0][4] + grid.grid[0][5] == grid.grid[0][6])
    
    require(grid.grid[3][3] + grid.grid[2][4] == grid.grid[1][4])
    
    require(grid.grid[4][2] + grid.grid[4][3] == grid.grid[3][4])
    require(grid.grid[1][8] + grid.grid[2][7] == grid.grid[3][6])
    require(grid.grid[2][8] + grid.grid[3][8] == grid.grid[3][7])
    
    require(grid.grid[2][6] + grid.grid[3][5] == grid.grid[4][5])

    require(grid.grid[4][1] + grid.grid[5][1] == grid.grid[5][0])
    require(grid.grid[7][2] + grid.grid[6][3] == grid.grid[5][4])
    require(grid.grid[6][6] + grid.grid[5][7] == grid.grid[5][8])
    
    require(grid.grid[7][0] + grid.grid[8][0] == grid.grid[6][0])
    
    require(grid.grid[8][4] + grid.grid[8][5] == grid.grid[8][3])
    require(grid.grid[7][6] + grid.grid[7][7] == grid.grid[8][8])

    sols = grid.solutions()
    print(sols)
    return sols

def decode(solutions):
    return utils.decode(solutions)
