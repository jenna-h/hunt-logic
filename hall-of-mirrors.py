from .claspy import *
from . import utils
from .utils.borders import *

def encode(string):
    return utils.encode(string)
    
def solve(E):
    set_max_val(100)

    forward_slash = '/'
    back_slash = '\\'

    grid = [[' ', ' ', '.', ' ', ' ', ' ', ' ', '.', '.', ' '],
            [' ', '/', '/', '/', '/', '/', '/', '/', '/', '.'],
            ['.', '/', '/', '/', '\\', '\\', '/', '/', '/', '.'],
            ['.', '/', '\\', '\\', '\\', '/', '\\', '\\', '/', ' '],
            [' ', '/', '/', '\\', '\\', '/', '/', '\\', '/', '.'],
            ['.', '\\', '\\', '\\', '/', '\\', '/', '/', '/', '.'],
            [' ', '\\', '/', '/', '\\', '\\', '/', '/', '/', '.'],
            ['.', '\\', '\\', '\\', '/', '\\', '/', '/', '/', ' '],
            [' ', '\\', '/', '\\', '\\', '/', '\\', '\\', '/', ' '],
            [' ', ' ', ' ', ' ', '.', '.', '.', '.', ' ', ' ']]

    known_mirrors = {
        (1, 1): True,
        (1, 2): True,
        (1, 4): True,
        (1, 5): False,
        (1, 6): False,
        (1, 7): False,
        (1, 8): False,

        (2, 1): True,
        (2, 3): True,
        (2, 4): False,
        (2, 5): False,
        (2, 6): False,
        (2, 7): False,
        (2, 8): True,

        (3, 1): False,
        (3, 2): False,
        (3, 3): False,
        (3, 4): False,
        (3, 5): False,
        (3, 6): True,
        (3, 7): True,
        (3, 8): True,

        (4, 3): False,
        (4, 4): True,
        (4, 5): False,
        (4, 6): True,
        (4, 8): True,

        (5, 3): True,
        (5, 4): False,
        (5, 5): True,
        (5, 6): True,
        (5, 7): False,
        (5, 8): False,

        (6, 3): True,
        (6, 4): False,
        (6, 5): False,
        (6, 6): False,
        (6, 8): False,

        (7, 3): False,
        (7, 4): True,
        (7, 5): False,
        (7, 6): True,
        (7, 7): True,
        (7, 8): True,

        # (8, 1): True,
        # (8, 2): True,
        (8, 3): True,
        (8, 4): False,
        (8, 5): False,
        (8, 6): True,
        (8, 7): False,
        (8, 8): False,
    }
    for x in range(10):
        known_mirrors[(0, x)] = False
        known_mirrors[(9, x)] = False
    for y in range(10):
        known_mirrors[(y, 0)] = False
        known_mirrors[(y, 9)] = False

    mirrors = [[BoolVar() for c in range(10)] for r in range(10)]
    light = [[MultiVar('r', 'J', '7', 'L', '+', ' ', '.', '1', '-') for c in range(10)] for r in range(10)]
    
    # Stuff I know as a human
    require(light[0][1] == ' ')

    def mirror_pattern(r, c):
        if (r, c) in known_mirrors:
            if known_mirrors[(r, c)]:
                if grid[r][c] == '/':
                    return '/'
                elif grid[r][c] == '\\':
                    return '\\'
                elif grid[r][c] in ' .':
                    raise ValueError('Did not expect known_mirrors to be true for a border')
            else:
                return ' '
        else:
            if grid[r][c] == '/':
                return cond(mirrors[r][c], '/', ' ')
            elif grid[r][c] == '\\':
                return cond(mirrors[r][c], '\\', ' ')
            else:
                return ' '
    
    def mirror_val(r, c):
        if (r, c) in known_mirrors:
            if known_mirrors[(r, c)]:
                if grid[r][c] == '/':
                    return '/'
                elif grid[r][c] == '\\':
                    return '\\'
                elif grid[r][c] in ' .':
                    raise ValueError('Did not expect known_mirrors to be true for a border')
            else:
                return ' '
        else:
            if grid[r][c] == '/':
                return '/' if mirrors[r][c].value() else ' '
            elif grid[r][c] == '\\':
                return '\\' if mirrors[r][c].value() else ' '
            else:
                return ' '

    for r in range(10):
        for c in range(10):
            if (r, c) in known_mirrors:
                require(mirrors[r][c] == known_mirrors[(r, c)])

            if 0 < r < 9 and 0 < c < 9:
                require(light[r][c] != '.')
            else:
                if grid[r][c] == '.':
                    require(light[r][c] == grid[r][c])
                else:
                    require(var_in(light[r][c], ('.', ' ')))

            # ---- J and r patterns ----
            # light and mirror relation
            require(
                var_in(light[r][c], ('J', 'r', '+', ' ')) |
                (mirror_pattern(r, c) != forward_slash)
            )
            require(
                (mirror_pattern(r, c) == forward_slash) |
                ~var_in(light[r][c], ('J', 'r'))
            )
            # light-light relation
            if 0 < r and 0 < c:
                require(
                    (var_in(light[r-1][c], ('r', '7', '+', '1', '.')) & var_in(light[r][c-1], ('r', 'L', '+', '-', '.'))) |
                    (light[r][c] != 'J')
                )
            else:
                require(light[r][c] != 'J')
            if r < 9 and c < 9:
                require(
                    (var_in(light[r+1][c], ('L', 'J', '+', '1', '.')) & var_in(light[r][c+1], ('7', 'J', '+', '-', '.'))) |
                    (light[r][c] != 'r')
                )
            else:
                require(light[r][c] != 'r')
            # ---- L and 7 patterns ----
            # light and mirror relation
            require(
                var_in(light[r][c], ('L', '7', '+', ' ')) |
                (mirror_pattern(r, c) != back_slash)
            )
            require(
                (mirror_pattern(r, c) == back_slash) |
                ~var_in(light[r][c], ('L', '7'))
            )
            # light-light relation
            if 0 < r and c < 9:
                require(
                    (var_in(light[r-1][c], ('r', '7', '+', '1', '.')) & var_in(light[r][c+1], ('7', 'J', '+', '-', '.'))) |
                    (light[r][c] != 'L')
                )
            else:
                require(light[r][c] != 'L')
            if r < 9 and 0 < c:
                require(
                    (var_in(light[r+1][c], ('L', 'J', '+', '1', '.')) & var_in(light[r][c-1], ('L', 'r', '+', '-', '.'))) |
                    (light[r][c] != '7')
                )
            else:
                require(light[r][c] != '7')
            # ---- + pattern ----
            # light-light relation
            # NOTE: It's okay to have lasers cross!
            if 0 < r < 9 and 0 < c < 9:
                require(
                    (var_in(light[r-1][c], ('r', '7', '+', '1', '.')) & 
                    var_in(light[r][c+1], ('7', 'J', '+', '-', '.')) & 
                    var_in(light[r+1][c], ('L', 'J', '+', '1', '.')) &
                    var_in(light[r][c-1], ('r', 'L', '+', '-', '.'))) |
                    (light[r][c] != '+')
                )
            else:
                require(light[r][c] != '+')
            # ---- 1 pattern ----
            # light-light relation
            if 0 < r < 9:
                require(
                    (var_in(light[r-1][c], ('r', '7', '+', '.', '1')) & var_in(light[r+1][c], ('J', 'L', '+', '.', '1'))) |
                    (light[r][c] != '1')
                )
            else:
                require(light[r][c] != '1')
            # ---- - pattern ----
            # light-light relation
            if 0 < c < 9:
                require(
                    (var_in(light[r][c-1], ('r', 'L', '+', '.', '-')) & var_in(light[r][c+1], ('J', '7', '+', '.', '-'))) |
                    (light[r][c] != '-')
                )
            else:
                require(light[r][c] != '-')
    
    for r in range(10):
        for c in range(10):
            if r in (0, 9) or c in (0, 9):
                # ---- . pattern ----
                # light-light relation
                at_least_one = BoolVar(False)
                if 0 < r:
                    at_least_one |= var_in(light[r-1][c], ('r', '7', '+', '1'))
                if r < 9:
                    at_least_one |= var_in(light[r+1][c], ('L', 'J', '+', '1'))
                if 0 < c:
                    at_least_one |= var_in(light[r][c-1], ('r', 'L', '+', '-'))
                if c < 9:
                    at_least_one |= var_in(light[r][c+1], ('7', 'J', '+', '-'))
                require(at_least_one == (light[r][c] == '.'))

    # There are exactly 8pairs * 2items/pair + 4 meta + 4 ends = 24 . s
    num_dots = BoolVar(0)
    for r in range(10):
        for c in range(10):
            num_dots += cond(light[r][c] == '.', 1, 0)
    # require(num_dots == 24)
    require(num_dots == 16)

    # Exactly 26 mirrors are on
    all_mirror_bools = []
    for r in range(10):
        all_mirror_bools += mirrors[r]
    require(sum_bools(26, all_mirror_bools))

    def check_all_connectivity():
        hearts = check_connectivity((5, 1), 'r', (7, 0))
        diamonds = check_connectivity((1, 8), 'd', (9, 5))
        return hearts # and diamonds
    
    def check_connectivity(curr, direction, end):
        while 0 < curr[0] < 9 and 0 < curr[1] < 9:
            mirror = mirror_val(*curr)
            if mirror == '/':
                if direction == 'r':
                    curr = (curr[0]-1, curr[1])
                    direction = 'u'
                elif direction == 'l':
                    curr = (curr[0]+1, curr[1])
                    direction = 'd'
                elif direction == 'u':
                    curr = (curr[0], curr[1]+1)
                    direction = 'r'
                elif direction == 'd':
                    curr = (curr[0], curr[1]-1)
                    direction = 'l'
            elif mirror == '\\':
                if direction == 'r':
                    curr = (curr[0]+1, curr[1])
                    direction = 'd'
                elif direction == 'l':
                    curr = (curr[0]-1, curr[1])
                    direction = 'u'
                elif direction == 'u':
                    curr = (curr[0], curr[1]-1)
                    direction = 'l'
                elif direction == 'd':
                    curr = (curr[0], curr[1]+1)
                    direction = 'r'
            else:
                if direction == 'r':
                    curr = (curr[0], curr[1]+1)
                    direction = 'r'
                elif direction == 'l':
                    curr = (curr[0], curr[1]-1)
                    direction = 'l'
                elif direction == 'u':
                    curr = (curr[0]-1, curr[1])
                    direction = 'u'
                elif direction == 'd':
                    curr = (curr[0]+1, curr[1])
                    direction = 'd'
        return curr == end

    solutions = []
    while claspy_solve() and len(solutions) < 5:
        x = BoolVar(True)
        for r in range(10):
            for c in range(10):
                x &= (mirrors[r][c] == mirrors[r][c].value())
        require(~x)
        
        if check_all_connectivity():
            mirror_sol = []
            for r in range(10):
                mirror_sol.append([mirror_val(r, c) for c in range(10)])

            light_sol = []
            for r in range(10):
                light_sol.append([light[r][c].value() for c in range(10)])
            
            solutions.append((mirror_sol, light_sol))
    
    for (mirror_sol, light_sol) in solutions:
        print("\t'".join(light_sol[0]))
        for r in range(1, 9):
            row = []
            row.append(light_sol[r][0])
            row += mirror_sol[r][1:9]
            row.append(light_sol[r][9])
            print("\t'".join(row))
        print("\t'".join(light_sol[9]))
        
        print()

        for r in range(10):
            print("\t'".join(light_sol[r]))

        print('----')
        print()
    
    return solutions

def decode(solutions):
    return utils.decode(solutions)