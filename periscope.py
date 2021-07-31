from .claspy import *
from . import utils
from .utils.borders import *

def encode(string):
    return utils.encode(string)
    
def solve(E):
    set_max_val(100)

    forward_slash = '/'
    back_slash = '\\'

    red = 'r'
    green = 'g'
    blue = 'b'

    one = 'one'
    bor = 'bor'
    tod = 'tod'
    hor = 'hor'
    spe = 'spe'
    bab = 'bab'
    unp = 'unp'

    bla_ans = 'bla_ans'
    sea_ans = 'sea_ans'

    list_of_controllers = (one, bor, tod, hor, spe, bab, unp, bla_ans, sea_ans)
    

    start = [[MultiVar(forward_slash, back_slash, ' ') for c in range(5)] for r in range(5)]
    
    controls = {
        x: (IntVar(1, 3), IntVar(1, 3)) for x in list_of_controllers
    }
    # Must control different ones--what if we relax?
    for x in controls:
        for y in controls:
            if x != y:
                require((controls[x][0] != controls[y][0]) | (controls[x][1] != controls[y][1]))

    seqs = {
        tuple():  ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (one,): ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  '.', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (one, bor,): ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  '.', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', '.', ' '), # rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (one, bor, tod): ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' '), # rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        # actually one, bor, tod, one
        (bor, tod): ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (one, bor, tod, hor): ((' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', '.', ' ', ' '), (' ',  '.', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (one, tod): ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', '.', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (spe,): ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (spe, one): ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (spe, hor): ((' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (spe, tod): ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (spe, one, hor): ((' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (spe, one, hor, tod): ((' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (u' ',  ' ', ' ', '.', ' ')), #rgbr
        # actually one, bor, one, spe, hor
        (bor, spe, hor): ((' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        # actually one, bor, tod, one, spe, hor
        (bor, tod, spe, hor): ((' ',  '.', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (tod,):  ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', '.', ' '), #rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        # actually one, bor, one, spe, one, hor, tod
        (one, bor, spe, hor, tod): ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' '), # rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        (one, tod, bab): ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', '.', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  '.', ' ', ' ', ' '), # rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        # actually one, tod, bab, one
        (tod, bab): ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  '.', ' ', ' ', ' '), # rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', ' ', ' '), (' ',  ' ', ' ', '.', ' ')), #rgbr
        # actually one, tod, bab, one, spe
        (tod, bab, spe): ((' ',  ' ', ' ', '.', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbt
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), #rgbl
              (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), (' ',  ' ', ' ', ' ', ' '), # rgbb
              (' ',  '.', ' ', ' ', ' '), (' ',  ' ', '.', '.', ' '), (' ',  ' ', '.', '.', ' ')), #rgbr
    
    }

    for x in range(5):
        for y in range(5):
            if 0 < x < 4 and 0 < y < 4:
                require(start[x][y] != ' ')
            else:
                require(start[x][y] == ' ')

    for seq in seqs:
        mirrors = [[MultiVar(forward_slash, back_slash, ' ') for c in range(5)] for r in range(5)]
        red_light = [[MultiVar('r', 'J', '7', 'L', '+', ' ', '.') for c in range(5)] for r in range(5)]
        green_light = [[MultiVar('r', 'J', '7', 'L', '+', ' ', '.') for c in range(5)] for r in range(5)]
        blue_light = [[MultiVar('r', 'J', '7', 'L', '+', ' ', '.') for c in range(5)] for r in range(5)]

        is_flipped = []
        for step in list_of_controllers:
            is_flipped.append((controls[step], step in seq))
        for x in range(5):
            for y in range(5):
                if 0 < x < 4 and 0 < y < 4:
                    require(mirrors[x][y] != ' ')
                    for mirror_coord, flipped in is_flipped:
                        require(
                                (mirrors[x][y] == (cond(start[x][y] == forward_slash, back_slash, forward_slash) if flipped else start[x][y])) |
                                ~((x == mirror_coord[0]) & (y == mirror_coord[1]))
                            )
                else:
                    require(mirrors[x][y] == ' ')
        red_top_clues, green_top_clues, blue_top_clues, \
            red_left_clues, green_left_clues, blue_left_clues, \
            red_bottom_clues, green_bottom_clues, blue_bottom_clues, \
            red_right_clues, green_right_clues, blue_right_clues = seqs[seq]
        
        for r in range(5):
            for c in range(5):
                if r == 0:
                    require(mirrors[r][c] == ' ')
                    require(red_light[r][c] == red_top_clues[c])
                    require(blue_light[r][c] == blue_top_clues[c])
                    require(green_light[r][c] == green_top_clues[c])
                if r == 4:
                    require(mirrors[r][c] == ' ')
                    require(red_light[r][c] == red_bottom_clues[c])
                    require(blue_light[r][c] == blue_bottom_clues[c])
                    require(green_light[r][c] == green_bottom_clues[c])
                if c == 0:
                    require(mirrors[r][c] == ' ')
                    require(red_light[r][c] == red_left_clues[r])
                    require(blue_light[r][c] == blue_left_clues[r])
                    require(green_light[r][c] == green_left_clues[r])
                if c == 4:
                    require(mirrors[r][c] == ' ')
                    require(red_light[r][c] == red_right_clues[r])
                    require(blue_light[r][c] == blue_right_clues[r])
                    require(green_light[r][c] == green_right_clues[r])

                for light_type in (red_light, green_light, blue_light):
                    if 0 < r < 4 and 0 < c < 4:
                        require(light_type[r][c] != '.')

                    # ---- J and r patterns ----
                    # light and mirror relation
                    require(
                        var_in(light_type[r][c], ('J', 'r', '+', ' ')) |
                        (mirrors[r][c] != forward_slash)
                    )
                    # light-light relation
                    if 0 < r and 0 < c:
                        require(
                            (var_in(light_type[r-1][c], ('r', '7', '+', '.')) & var_in(light_type[r][c-1], ('r', 'L', '+', '.'))) |
                            (light_type[r][c] != 'J')
                        )
                    else:
                        require(light_type[r][c] != 'J')
                    if r < 4 and c < 4:
                        require(
                            (var_in(light_type[r+1][c], ('L', 'J', '+', '.')) & var_in(light_type[r][c+1], ('7', 'J', '+', '.'))) |
                            (light_type[r][c] != 'r')
                        )
                    else:
                        require(light_type[r][c] != 'r')
                    # ---- L and 7 patterns ----
                    # light and mirror relation
                    require(
                        var_in(light_type[r][c], ('L', '7', '+', ' ')) |
                        (mirrors[r][c] != back_slash)
                    )
                    # light-light relation
                    if 0 < r and c < 4:
                        require(
                            (var_in(light_type[r-1][c], ('r', '7', '+', '.')) & var_in(light_type[r][c+1], ('7', 'J', '+', '.'))) |
                            (light_type[r][c] != 'L')
                        )
                    else:
                        require(light_type[r][c] != 'L')
                    if r < 4 and 0 < c:
                        require(
                            (var_in(light_type[r+1][c], ('L', 'J', '+', '.')) & var_in(light_type[r][c-1], ('L', 'r', '+', '.'))) |
                            (light_type[r][c] != '7')
                        )
                    else:
                        require(light_type[r][c] != '7')
                    # ---- + pattern ----
                    # light-light relation
                    if 0 < r < 4 and 0 < c < 4:
                        require(
                            (var_in(light_type[r-1][c], ('r', '7', '+', '.')) & 
                            var_in(light_type[r][c+1], ('7', 'J', '+', '.')) & 
                            var_in(light_type[r+1][c], ('L', 'J', '+', '.')) &
                            var_in(light_type[r][c-1], ('r', 'L', '+', '.'))) |
                            (light_type[r][c] != '+')
                        )
                    else:
                        require(light_type[r][c] != '+')
        
        for r in range(5):
            for c in range(5):
                if r in (0, 4) or c in (0, 4):
                    for light_type in (red_light, green_light, blue_light):
                        # ---- . pattern ----
                        # light-light relation
                        at_least_one = BoolVar(False)
                        if 0 < r:
                            at_least_one |= var_in(light_type[r-1][c], ('r', '7', '+'))
                        if r < 4:
                            at_least_one |= var_in(light_type[r+1][c], ('L', 'J', '+'))
                        if 0 < c:
                            at_least_one |= var_in(light_type[r][c-1], ('r', 'L', '+'))
                        if c < 4:
                            at_least_one |= var_in(light_type[r][c+1], ('7', 'J', '+'))
                        require(at_least_one | (light_type[r][c] != '.'))
                if r in (0, 4) and c in (0, 4):
                    require(light_type[r][c] == ' ')

    solutions = []
    while claspy_solve() and len(solutions) < 50:
        x = BoolVar(True)
        # Controls must be different
        controls_sol = []
        for y in list_of_controllers:
            x &= (controls[y][0] == controls[y][0].value()) & (controls[y][1] == controls[y][1].value())
            controls_sol.append((y, (controls[y][0].value(), controls[y][1].value())))

        # Start must be different
        start_sol = []
        for r in range(5):
            start_sol.append([start[r][c].value() for c in range(5)])
            for c in range(5):
                x &= (start[r][c] == start[r][c].value())
        require(~x)

        red_sol, green_sol, blue_sol = [], [], []
        for r in range(5):
            red_sol.append([red_light[r][c].value() for c in range(5)])
            green_sol.append([green_light[r][c].value() for c in range(5)])
            blue_sol.append([blue_light[r][c].value() for c in range(5)])
        
        mirror_sol = []
        for r in range(5):
            mirror_sol.append([mirrors[r][c].value() for c in range(5)])

        solutions.append((controls_sol, start_sol, red_sol, green_sol, blue_sol, mirror_sol))
    
    for sol in solutions:
        mapping, grid, red, green, blue, mirror_sol = sol
        print('controls mapping =', mapping)
        print()
        print('starting mirrors =')
        for row in grid:
            print(row)
        print()
        # print('red =')
        # for row in red:
        #     print(row)
        # print()
        # print('green =')
        # for row in green:
        #     print(row)
        # print()
        # print('blue =')
        # for row in blue:
        #     print(row)
        # print()
        # print('mirrors =')
        # for row in mirror_sol:
        #     print(row)

        print('----')
        print()
    
    return solutions

def decode(solutions):
    return utils.decode(solutions)
