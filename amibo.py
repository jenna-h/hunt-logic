from .claspy import *
from . import utils
from .utils import solutions

def encode(string):
    return utils.encode(string)

def solve(encoding):
    '''
    Given an encoding of an amibo puzzle, as returned by encode_amibo,
    returns a list of solutions, where each solution is
    a list of cell values, in a left-to-right, top-to-bottom order;
    each cell value is one of:
     - a clue value (an integer or '?')
     - '1': an vertical bar section
     - '-': a horizontal bar section
     - '+': the intersection of vertical and horizontal sections
     - ' ' : a blank cell
    '''
    rows, cols, clue_cells = encoding
    
    reset()

    # the maximum length of a horizontal bar is 'rows' cells;
    # max length of vertical bar is 'cols'
    set_max_val(max(rows, cols))

    # define which connection patterns are 'horizontal' / 'vertical' in nature
    HORIZONTAL = ['-', '+']
    VERTICAL = ['1', '+']

    # the pattern for each cell
    pattern = [[MultiVar(' ', '-', '1', '+') for c in range(cols)] for r in range(rows)]

    # the length of the horizontal / vertical bar that this particular cell belongs to;
    # 0 if it's not part of any bar
    horizontal_length = [[IntVar(0, cols) for c in range(cols)] for r in range(rows)]
    vertical_length = [[IntVar(0, rows) for c in range(cols)] for r in range(rows)]

    # a cell is a 'starting cell' if it's the leftmost in a horizontal bar,
    # or topmost in a vertical bar
    horizontal_start = [[BoolVar() for c in range(cols)] for r in range(rows)]
    vertical_start = [[BoolVar() for c in range(cols)] for r in range(rows)]


    for r in range(rows):
        for c in range(cols):
            if (r, c) in clue_cells:
                # clue cells have no connectivity
                require(pattern[r][c] == ' ')
                require(horizontal_length[r][c] == 0)
                require(vertical_length[r][c] == 0)
                require(~horizontal_start[r][c])
                require(~vertical_start[r][c])
            else:
                # if this cell is a vertical start, it must be vertical in nature
                require(var_in(pattern[r][c], VERTICAL) | ~vertical_start[r][c])
                require(var_in(pattern[r][c], HORIZONTAL) | ~horizontal_start[r][c])
                # if this cell is not vertical in nature, it must have a 'vertical length' of 0
                require((vertical_length[r][c] == 0) | var_in(pattern[r][c], VERTICAL))
                require((horizontal_length[r][c] == 0) | var_in(pattern[r][c], HORIZONTAL))
                if 0 < r:
                    # if this cell is not in the top row 
                    require(
                        # if the cell above is vertical
                        cond(var_in(pattern[r-1][c], VERTICAL),
                            # then this cell cannot be a vertical start
                            ~vertical_start[r][c],
                            # if the cell above is not vertical,
                            # and this cell is vertical, then it must be a vertical start
                            (vertical_start[r][c] | ~var_in(pattern[r][c], VERTICAL))))
                else:
                    # if this cell is in the top row,
                    # if the cell is vertical, it must be a vertical start
                    require(vertical_start[r][c] | ~var_in(pattern[r][c], VERTICAL))
                if 0 < c:
                    require(cond(var_in(pattern[r][c-1], HORIZONTAL),
                                ~horizontal_start[r][c],
                                (horizontal_start[r][c] | ~var_in(pattern[r][c], HORIZONTAL))))
                else:
                    require(horizontal_start[r][c] | ~var_in(pattern[r][c], HORIZONTAL))
                    
                # for each possible ending point of the vertical bar
                for y in range(r, rows):
                    # the vertical bar goes from (r, c) to (y, c), inclusive,
                    vertical_bar = var_in(pattern[r][c], VERTICAL)
                    # its length is (y-r+1),
                    vertical_lens = (vertical_length[r][c] == (y-r+1))
                    # and it needs to intersect a horizontal bar of the same length
                    horizontal_intersect = (horizontal_length[r][c] == (y-r+1))

                    # iterate over the range!
                    for y1 in range(r+1, y+1):
                        vertical_bar &= var_in(pattern[y1][c], VERTICAL)
                        vertical_lens &= (vertical_length[y1][c] == (y-r+1))
                        horizontal_intersect |= (horizontal_length[y1][c] == (y-r+1))
                    # make sure that the bar is EXACTLY the right length
                    if y != rows-1:
                        vertical_bar &= ~var_in(pattern[y+1][c], VERTICAL)
                        
                    # if this is a vertical start,
                    # and the segments indicate that the current value of y is correct,
                    # then force the values of the 'vertical length' counters and
                    # ensure there is a horizontal intersection
                    require(cond(vertical_start[r][c],
                                  cond(vertical_bar,
                                       vertical_lens & horizontal_intersect,
                                       True),
                                  True))
                    
                # handle horizontal bars
                for x in range(c, cols):
                    horizontal_bar = var_in(pattern[r][c], HORIZONTAL)
                    horizontal_lens = (horizontal_length[r][c] == (x-c+1))
                    vertical_intersect = (vertical_length[r][c] == (x-c+1))
                    for x1 in range(c+1, x+1):
                        horizontal_bar &= var_in(pattern[r][x1], HORIZONTAL)
                        horizontal_lens &= (horizontal_length[r][x1] == (x-c+1))
                        vertical_intersect |= (vertical_length[r][x1] == (x-c+1))
                    if x != cols-1:
                        horizontal_bar &= ~var_in(pattern[r][x+1], HORIZONTAL)
                    require(cond(horizontal_start[r][c],
                                  cond(horizontal_bar,
                                       horizontal_lens & vertical_intersect,
                                       True),
                                  True))
                        
    for (r, c) in clue_cells:
        neighbors = []
        # if there is a top neighbor
        if 0 < r:
            # the top neighbor is the one that satisfies the clue if
            #  - it has vertical connectivity
            top = var_in(pattern[r-1][c], VERTICAL)
            #  - and it has the correct vertical length
            if isinstance(clue_cells[r,c], int):
                require((vertical_length[r-1][c] == clue_cells[r,c]) |
                        ~top)
            # keep track of the top-adjacency condition
            neighbors.append(top)
        if r < rows-1:
            bottom = var_in(pattern[r+1][c], VERTICAL)
            if isinstance(clue_cells[r,c], int):
                require((vertical_length[r+1][c] == clue_cells[r,c]) |
                        ~bottom)
            neighbors.append(bottom)
        if 0 < c:
            left = var_in(pattern[r][c-1], HORIZONTAL)
            if isinstance(clue_cells[r,c], int):
                require((horizontal_length[r][c-1] == clue_cells[r,c]) |
                        ~left)
            neighbors.append(left)
        if c < cols-1:
            right = var_in(pattern[r][c+1], HORIZONTAL)
            if isinstance(clue_cells[r,c], int):
                require((horizontal_length[r][c+1] == clue_cells[r,c]) |
                        ~right)
            neighbors.append(right)
        # exactly 1 neighbor satisfies the clue
        require(at_most(1, neighbors))
        require(at_least(1, neighbors))

    # connectivity[r][c] is true IFF the cell is connected to the rest
    connectivity = [[Atom() for c in range(cols)] for r in range(rows)]
    # keep track of parents (we need to make sure there are no cycles)
    parent = [[MultiVar('<', '>', '^', 'v', '.', ' ') for c in range(cols)] for r in range(rows)]

    # for some random clue cell
    for (r, c) in clue_cells:
        # exactly one of the neighbors will be connected to the clue cell
        if 0 < r:
            require((parent[r-1][c] == '.') == var_in(pattern[r-1][c], VERTICAL))
            connectivity[r-1][c].prove_if(var_in(pattern[r-1][c], VERTICAL))
        if r < rows-1:
            require((parent[r+1][c] == '.') == var_in(pattern[r+1][c], VERTICAL))
            connectivity[r+1][c].prove_if(var_in(pattern[r+1][c], VERTICAL))
        if 0 < c:
            require((parent[r][c-1] == '.') == var_in(pattern[r][c-1], HORIZONTAL))
            connectivity[r][c-1].prove_if(var_in(pattern[r][c-1], HORIZONTAL))
        if c < cols-1:
            require((parent[r][c+1] == '.') == var_in(pattern[r][c+1], HORIZONTAL))
            connectivity[r][c+1].prove_if(var_in(pattern[r][c+1], HORIZONTAL))
        break

    for r in range(rows):
        for c in range(cols):
            # if this cell is not in the top row 
            if 0 < r:
                # if:
                #   - this cell and the one above it are vertical
                #           (they connect vertically),
                #   - and the parent of (r, c) is ^,
                #   - and (r-1, c) connects to the rest of the non-empty, non-clue cells,
                # 
                # then this cell is also connected
                connectivity[r][c].prove_if(var_in(pattern[r][c], VERTICAL) &
                                            var_in(pattern[r-1][c], VERTICAL) &
                                            (parent[r][c] == '^') &
                                            connectivity[r-1][c])
                # vertically adjacent cells are a parent-child
                # if this is not the case, then we have a cycle!
                require(((parent[r-1][c] == 'v') | (parent[r][c] == '^')) |
                        ~(var_in(pattern[r-1][c], VERTICAL) &
                            var_in(pattern[r][c], VERTICAL)))
            # if this cell is not in the bottom row
            if r < rows-1:
                # make sure that this cell is connected;
                # we don't have to test for parent-child relationships, since
                # the '0 < r' if-block tests the relationship between
                # every cell and its top neighbor
                connectivity[r][c].prove_if(var_in(pattern[r][c], VERTICAL) &
                                            var_in(pattern[r+1][c], VERTICAL) &
                                            (parent[r][c] == 'v') &
                                            connectivity[r+1][c])
            if 0 < c:
                connectivity[r][c].prove_if(var_in(pattern[r][c], HORIZONTAL) &
                                            var_in(pattern[r][c-1], HORIZONTAL) &
                                            (parent[r][c] == '<') &
                                            connectivity[r][c-1])
                require(((parent[r][c-1] == '>') | (parent[r][c] == '<')) |
                        ~(var_in(pattern[r][c-1], HORIZONTAL) &
                            var_in(pattern[r][c], HORIZONTAL)))
            if c < cols-1:
                connectivity[r][c].prove_if(var_in(pattern[r][c], HORIZONTAL) &
                                            var_in(pattern[r][c+1], HORIZONTAL) &
                                            (parent[r][c] == '>') &
                                            connectivity[r][c+1])
            # empty and clue cells have empty parents
            require((pattern[r][c] == ' ') == (parent[r][c] == ' '))
            # non-empty, non-clue cells must be connected!
            require(connectivity[r][c] == (pattern[r][c] != ' '))

    return get_all_grid_solutions(pattern,
                format_function = clue_cells[(r, c)] if (r, c) in clue_cells else pattern[r][c].value())
    
def decode(solutions):
    return utils.decode(solutions)
