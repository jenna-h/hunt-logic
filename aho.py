from .claspy import *
from . import utils
from .utils import borders
from .utils.borders import Direction
from .utils import solutions
from .utils import regions

def encode(string):
    return utils.encode(string)

def solve(encoding):
    '''
    Given an encoding of an aho puzzle, as would be returned by encode_aho,

    Returns a list of solutions, of maximum size MAX_SOLUTIONS_TO_FIND,
    where each solution is a list of dictionaries mapping edge directions
    ('left', 'right', 'top', 'bottom') to Booleans (if a direction is absent
    in the dictionary, there is no edge). Each dictionary represents
    the edges of the corresponding cell (left-to-right, top-to-bottom read order).
    '''
    rows, cols, clue_cells = encoding

    reset()

    # assign an ID to each clue cell
    clue_cell_id = {}
    id_to_cell = {}
    for r in range(rows):
        for c in range(cols):
            if (r, c) in clue_cells:
                id_to_cell[len(clue_cell_id)] = (r,c)
                clue_cell_id[(r,c)] = len(clue_cell_id)
                
    max_clue =  max(clue_cells.values())
    
    set_max_val(max(len(clue_cell_id)-1, max_clue, rows-1, cols-1))

    region_symbol_sets = []
    for region_id in range(len(clue_cell_id)):
        region_symbol_sets.append([region_id])

    regions_solver = RectangularGridRegionSolver(rows, cols, max_num_regions = len(clue_cell_id), region_symbol_sets = region_symbol_sets)

    # shape conditions
    #
    # For this part, we first need make two observations:
    #  1) A rectangle is defined by 2 points (opposite corners)
    #  2) An L shape is composed of 2 rectangles
    #
    # Let's first discuss rectangles, since they're the simpler case.
    #   A rectangle defined by (r1, c1) and (r2, c2) contains (r, c) IFF
    #       (r is between r1 and r2) and (c is between c1 and c2)
    #
    # Now consider the case of an L shape.
    #   Every L shape can be defined by 3 points
    #       1) one "corner"
    #       2) one point which defines the "opposite corner" of rectangle 1
    #       3) one point which defines the "opposite corner" of rectangle 2
    #   
    #   There are some additional rules about the relationship between
    #   rectangle 1 and rectangle 2.
    #       - Neither rectangle can contain the other
    #       - The rectangles can't have the same row coord or col coord
    #           for example, if they have the same row coordinate,
    #           (x denotes rect 1, o denotes rect 2):
    #               xxxo
    #               xxxo
    #               xxxo
    #           this just creates a rectangle :(
    #                 
    #   A point is inside of the L shape if it's in either one of the rectangles
    #   (see definition of "inside" for rectangles above)
    for clue_id in id_to_cell:
        # clue divisible by 3; need L shape
        if clue_cells[id_to_cell[clue_id]] % 3 == 0:
            corner = (IntVar(0, rows-1), IntVar(0, cols-1))
            rect_1 = (IntVar(0, rows-1), IntVar(0, cols-1))
            rect_2 = (IntVar(0, rows-1), IntVar(0, cols-1))

            # corner != rect_1
            require(~((corner[0] == rect_1[0]) & (corner[1] == rect_1[1])))
            # corner != rect_2
            require(~((corner[0] == rect_2[0]) & (corner[1] == rect_2[1])))

            # the L needs to have a bend in it; no straight lines!
            require(rect_1[0] != rect_2[0])
            require(rect_1[1] != rect_2[1])
            
            # the 2nd rectangle can't be inside the first
            require(~(
                        # rect_2's row is between corner's row and rect_1's row
                        (
                            ((corner[0] <= rect_2[0]) & (rect_2[0] <= rect_1[0])) |
                            ((rect_1[0] <= rect_2[0]) & (rect_2[0] <= corner[0]))
                        )
                            &
                        # col between cols
                        (
                            ((corner[1] <= rect_2[1]) & (rect_2[1] <= rect_1[1])) |
                            ((rect_1[1] <= rect_2[1]) & (rect_2[1] <= corner[1]))
                        )
                    ))
            # and the 1st rectangle can't be inside the second
            require(~(
                        # rect_1's row is between corner's row and rect_2's row
                        (
                            ((corner[0] <= rect_1[0]) & (rect_1[0] <= rect_2[0])) |
                            ((rect_2[0] <= rect_1[0]) & (rect_1[0] <= corner[0]))
                        )
                            &
                        # col between cols
                        (
                            ((corner[1] <= rect_1[1]) & (rect_1[1] <= rect_2[1])) |
                            ((rect_2[1] <= rect_1[1]) & (rect_1[1] <= corner[1]))
                        )
                    ))

            for r in range(rows):
                for c in range(cols):
                    # (r,c) is in this room IFF it is in one of the rectangles
                    require((room[r][c] == clue_id) == \
                            # inside 1st rectangle
                            (
                                # row is between corner's row and rect_1's row
                                (
                                    ((corner[0] <= r) & (r <= rect_1[0])) |
                                    ((rect_1[0] <= r) & (r <= corner[0]))
                                )
                                    &
                                # col between cols
                                (
                                    ((corner[1] <= c) & (c <= rect_1[1])) |
                                    ((rect_1[1] <= c) & (c <= corner[1]))
                                )
                            ) |
                            # inside 2nd rectangle
                            (
                                # row is between corner's row and rect_1's row
                                (
                                    ((corner[0] <= r) & (r <= rect_2[0])) |
                                    ((rect_2[0] <= r) & (r <= corner[0]))
                                )
                                    &
                                # col between cols
                                (
                                    ((corner[1] <= c) & (c <= rect_2[1])) |
                                    ((rect_2[1] <= c) & (c <= corner[1]))
                                )
                            ))
        else:
            corner_1 = (IntVar(0, rows-1), IntVar(0, cols-1))
            corner_2 = (IntVar(0, rows-1), IntVar(0, cols-1))

            # it's okay for corner_1 == corner_2; that causes a 1x1 square,
            # which is needed for '1' clues

            for r in range(rows):
                for c in range(cols):
                    # (r,c) is in this room IFF it is in the rectangle
                    require((region_solver.grid[r][c] == clue_id) == \
                                # row is between corners' rows
                                (
                                    ((corner_1[0] <= r) & (r <= corner_2[0])) |
                                    ((corner_2[0] <= r) & (r <= corner_1[0]))
                                )
                                    &
                                # col between cols
                                (
                                    ((corner_1[1] <= c) & (c <= corner_2[1])) |
                                    ((corner_2[1] <= c) & (c <= corner_1[1]))
                                )
                            )
                            
    return regions_solver.solutions()

def decode(solutions):
    return utils.decode(solutions)
