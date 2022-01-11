from .claspy import *
from . import utils
from .utils.solutions import *
from .utils.grids import *
from .utils.loops import *
import itertools

def encode(string):
    return utils.encode(string, clue_encoder = lambda s : s)
    
def solve(E):
    #TODO
    set_max_val(100)

    # The settings that provide valid solutions are as follows:
    # (0, 1, 2, -), (T, T, T, F)
    # (2, 0, -, 1), (T, T, F, T)
    # (1, -, 0, 2), (T, F, T, T)
    # (-, 2, 1, 0), (F, T, T, T)
    balance_loop_num, castle_wall_num, masyu_num, tapa_num = 0, 2, 1, 0
    use_balance_loop, use_castle_wall, use_masyu, use_tapa_loop = False, True, True, True

    ls = RectangularGridLoopSolver(E.R, E.C)
    ls.loop({})

    balance_loop = [
        # {(1, 2): ['?', 'b']}
        {(1, 2): ['?', 'b'], (2, 2): ['4', 'w'], (4, 1): ['3', 'b'], (6, 0): ['6', 'b'], (7, 0): ['?', 'w']},
        {(1, 3): ['3', 'b'], (1, 4): ['4', 'w'], (4, 3): ['4', 'w'], (4, 5): ['3', 'b'], (7, 4): ['4', 'b'], (7, 5): ['2', 'w']},
        {(1, 6): ['5', 'b'], (4, 7): ['3', 'b'], (7, 8): ['4', 'w']}
    ]

    castle_wall = [
        {(1, 1): ['3', 'r', 'b'], (3, 0): ['2', 'd', 'b'], (5, 2): ['1', 'r', 'w'], (7, 1): ['5', 'r', 'w']},
        {(0, 3): ['1', 'l', 'g'], (2, 4): ['2', 'r', 'b'], (4, 3): ['1', 'd', 'g'], (4, 5): ['0', 'r', 'b'], (6, 4): ['1', 'u', 'w'], (8, 5): ['0', 'l', 'g']},
        {(0, 8): ['5', 'l', 'g'], (2, 6): ['1', 'l', 'w'], (4, 7): ['3', 'l', 'b'], (6, 8): ['2', 'u', 'g'], (8, 6): ['1', 'l', 'g']}
    ]

    masyu = [
        {(2, 0): 'b', (4, 1): 'w', (6, 2): 'w'},
        {(2, 3): 'w', (3, 5): 'b', (5, 3): 'w', (6, 5): 'b'},
        {(0, 6): 'w', (2, 7): 'w', (6, 7): 'b', (8, 8): 'b'}
    ]

    tapa_loop = [
        # {(1, 0): [2]}
        {(1, 0): [2], (4, 1): [1, 5], (7, 2): [2, 2]},
        {(2, 3): [2, 4], (4, 4): [2, 3], (6, 5): [1, 2]},
        {(2, 7): [7], (4, 7): [3, 3], (6, 7): [5]}
    ]

    TURNING = ['J', '7', 'L', 'r']
    STRAIGHT = ['-', '1']
    # --- BALANCE LOOP ---
    if use_balance_loop:
        for (r, c), (num, color) in balance_loop[balance_loop_num].items():
            require(~var_in(ls.grid[r][c], ISOLATED))
            u_conn = IntVar(1)
            u_has_found_bend = BoolVar(False)
            r_conn = IntVar(1)
            r_has_found_bend = BoolVar(False)
            d_conn = IntVar(1)
            d_has_found_bend = BoolVar(False)
            l_conn = IntVar(1)
            l_has_found_bend = BoolVar(False)
            # Count cells above
            for y in range(r-1, -1, -1):
                is_straight = var_in(ls.grid[y][c], STRAIGHT)
                is_bend = var_in(ls.grid[y][c], TURNING)
                u_conn += cond(is_straight & ~u_has_found_bend, 1, 0)
                u_has_found_bend |= is_bend
            # Count cells to the right
            for x in range(c+1, E.C):
                is_straight = var_in(ls.grid[r][x], STRAIGHT)
                is_bend = var_in(ls.grid[r][x], TURNING)
                r_conn += cond(is_straight & ~r_has_found_bend, 1, 0)
                r_has_found_bend |= is_bend
            # Count cells below
            for y in range(r+1, E.R):
                is_straight = var_in(ls.grid[y][c], STRAIGHT)
                is_bend = var_in(ls.grid[y][c], TURNING)
                d_conn += cond(is_straight & ~d_has_found_bend, 1, 0)
                d_has_found_bend |= is_bend
            # Count cells to the left
            for x in range(c-1, -1, -1):
                is_straight = var_in(ls.grid[r][x], STRAIGHT)
                is_bend = var_in(ls.grid[r][x], TURNING)
                l_conn += cond(is_straight & ~l_has_found_bend, 1, 0)
                l_has_found_bend |= is_bend
            if color == 'w':
                require((u_conn == r_conn) | (ls.grid[r][c] != 'L'))
                require((u_conn == d_conn) | (ls.grid[r][c] != '1'))
                require((u_conn == l_conn) | (ls.grid[r][c] != 'J'))
                require((r_conn == d_conn) | (ls.grid[r][c] != 'r'))
                require((r_conn == l_conn) | (ls.grid[r][c] != '-'))
                require((d_conn == l_conn) | (ls.grid[r][c] != '7'))
            else:
                require((u_conn != r_conn) | (ls.grid[r][c] != 'L'))
                require((u_conn != d_conn) | (ls.grid[r][c] != '1'))
                require((u_conn != l_conn) | (ls.grid[r][c] != 'J'))
                require((r_conn != d_conn) | (ls.grid[r][c] != 'r'))
                require((r_conn != l_conn) | (ls.grid[r][c] != '-'))
                require((d_conn != l_conn) | (ls.grid[r][c] != '7'))
            if num != '?':
                int_num = int(num)
                require((u_conn + r_conn == int_num) | (ls.grid[r][c] != 'L'))
                require((u_conn + d_conn == int_num) | (ls.grid[r][c] != '1'))
                require((u_conn + l_conn == int_num) | (ls.grid[r][c] != 'J'))
                require((r_conn + d_conn == int_num) | (ls.grid[r][c] != 'r'))
                require((r_conn + l_conn == int_num) | (ls.grid[r][c] != '-'))
                require((d_conn + l_conn == int_num) | (ls.grid[r][c] != '7'))

    # --- CASTLE WALL ---
    if use_castle_wall:
        cw_white_clues, cw_black_clues = set(), set()
        for (r, c), (num, d, color) in castle_wall[castle_wall_num].items():
            if num != '':
                if d == 'u':
                    require(sum_bools(int(num), [var_in(ls.grid[y][c], 
                        DOWN_CONNECTING) for y in range(r-1)]))
                elif d == 'r':
                    require(sum_bools(int(num), [var_in(ls.grid[r][x], 
                        RIGHT_CONNECTING) for x in range(c+1, E.C-1)]))
                elif d == 'd':
                    require(sum_bools(int(num), [var_in(ls.grid[y][c], 
                        DOWN_CONNECTING) for y in range(r+1, E.R-1)]))
                elif d == 'l':
                    require(sum_bools(int(num), [var_in(ls.grid[r][x], 
                        RIGHT_CONNECTING) for x in range(c-1)]))
            # Colors.
            if color == 'w':
                cw_white_clues.add((r, c))
            elif color == 'b':
                cw_black_clues.add((r, c))
            # No clues on the loop.
            require(var_in(ls.grid[r][c], ISOLATED))
        ls.inside(cw_white_clues)
        ls.outside(cw_black_clues)


    # --- MASYU ---
    if use_masyu:
        for (r, c), color in masyu[masyu_num].items():
            if color == 'b':
                require(var_in(ls.grid[r][c], TURNING))

                # not leftmost
                if 0 <= c-1:
                    # if not leftmost and not topmost
                    if 0 <= r-1:
                        # if a cell looks like J,
                        # the cells above and to the left of it must be straight
                        require(
                            (var_in(ls.grid[r-1][c], STRAIGHT) &
                                var_in(ls.grid[r][c-1], STRAIGHT)) |
                                    (ls.grid[r][c] != 'J'))
                    # if not leftmost and not bottommost
                    if r+1 < E.R:
                        # if a cell looks like 7,
                        # the cells below and to the left of it must be straight
                        require(
                            (var_in(ls.grid[r+1][c], STRAIGHT) &
                                var_in(ls.grid[r][c-1], STRAIGHT)) |
                                    (ls.grid[r][c] != '7'))
                # not rightmost
                if c+1 < E.C:
                    # if not rightmost and not topmost
                    if 0 <= r-1:
                        # if a cell looks like L,
                        # the cells above and to the right of it must be straight
                        require(
                            (var_in(ls.grid[r-1][c], STRAIGHT) &
                                var_in(ls.grid[r][c+1], STRAIGHT)) |
                                    (ls.grid[r][c] != 'L'))
                    # if not rightmost and not bottommost
                    if r+1 < E.R:
                        
                        # if a cell looks like r,
                        # the cells below and to the right of it must be straight
                        require(
                            (var_in(ls.grid[r+1][c], STRAIGHT) &
                                var_in(ls.grid[r][c+1], STRAIGHT)) |
                                    (ls.grid[r][c] != 'r'))

            # ----- WHITE CIRCLE RULES -----
            
            else:
                require(var_in(ls.grid[r][c], STRAIGHT))

                # if the line is horizontal,
                # at least one of the cells to the left and right is a turn
                if 0 < c and c < E.C-1:
                    require(
                        var_in(ls.grid[r][c-1], TURNING) |
                                var_in(ls.grid[r][c+1], TURNING) |
                                (ls.grid[r][c] != '-'))
                    
                # if the line is vertical,
                # at least one of the cells to the top and bottom is a turn
                if 0 < r and r < E.R-1:
                    require(
                        var_in(ls.grid[r-1][c], TURNING) |
                                var_in(ls.grid[r+1][c], TURNING) |
                                (ls.grid[r][c] != '1'))


    # --- TAPA-LIKE LOOP ---
    # --- BEGIN ARMY OF HELPER FUNCTIONS ---

    # -- Helper functions about generating possible loop patterns for clues --
    def acc_patterns(acc, initial=''):
        '''
        Given a set `acc` to accumulate patterns into,
        and an initial condition `initial`,

        Calculate possible patterns around a Tapa Loop clue,
        starting from the NW corner, using the following notation:
            s: the start of a loop segment
            e: the end of a loop segment
            c: a corner (both start and end, in one cell)
            -: a continuation (neither a start nor an end)
            ' ': empty space
        '''
        if len(initial) == 0:
            for possible in 'cs-e ':
                acc_patterns(acc, possible)
        elif len(initial) == 7: # base case - need to complete loop
            if initial[0] in '-e': # if start of the loop needs a predecessor
                if initial[-1] in 's-': # if the previous cell needs a successor
                    acc.add(initial + '-')
                else: # if previous cell has no successor
                    acc.add(initial + 's')
            else: # start of loop has no successor
                if initial[-1] in 's-': # if the previous cell needs a successor
                    acc.add(initial + 'e')
                else: # if previous cell has no successor
                    acc.add(initial + ' ')
        else:
            if initial[-1] in 's-': # needs successor
                for possible in '-e':
                    acc_patterns(acc, initial + possible)
            else: # cannot have successor
                for possible in 's ':
                    acc_patterns(acc, initial + possible)
                if len(initial) in (2, 4, 6): # the current cell is a corner
                    acc_patterns(acc, initial + 'c')

    def calculate_lengths(pattern):
        '''
        Return a sorted tuple of (length, frequency) tuples for the lengths 
        of loop segments used by a pattern, in the output format used by `acc_patterns`.
        '''
        if pattern[0] in '-e':
            try:
                s_idx = pattern.index('s')
            except ValueError:
                # the loop is completely enclosed
                return ((8, 1),)
            return calculate_lengths_rotated(pattern[s_idx:] + pattern[:s_idx])
        return calculate_lengths_rotated(pattern)

    def calculate_lengths_rotated(pattern):
        '''
        Return a sorted tuple of (length, frequency) tuples for the lengths 
        of loop segments used by a pattern, in the output format used by `acc_patterns`,

        WITH THE PRECONDITION THAT segment ends always follow segment starts
        in a naive left-to-right reading of the string.
        '''
        lengths = {}
        start_idx = None
        for i, c in enumerate(pattern):
            if c == 's':
                start_idx = i
            elif c == 'c':
                lengths[1] = lengths.get(1, 0) + 1
            elif c == 'e':
                lengths[i - start_idx + 1] = lengths.get(i - start_idx + 1, 0) + 1
                start_idx = None
        return tuple(sorted(lengths.items()))

    def get_lookup():
        '''
        Get a 'lookup table' of sorted (length, frequency) pairs to sets of patterns.
        '''
        all_patterns = set()
        acc_patterns(all_patterns)

        lookup = {}
        for pattern in all_patterns:
            pattern_lengths = calculate_lengths(pattern)
            if pattern_lengths in lookup:
                lookup[pattern_lengths].add(pattern)
            else:
                lookup[pattern_lengths] = {pattern}
        
        return lookup

    # Map of 'se- c' patterns to strings based on position (tuple's 0 index is NW corner)
    POSITIONAL_SHAPES = (
        {'s': ('L', '-'), 'e': ('7', '1'), '-': ('r',), ' ': ('',), 'c': ('J',)},
        {'s': ('L',), 'e': ('J',), '-': ('-',), ' ': ('',)},
        {'s': ('r', '1'), 'e': ('J', '-'), '-': ('7',), ' ': ('',), 'c': ('L',)},
        {'s': ('r',), 'e': ('L',), '-': ('1',), ' ': ('',)},
        {'s': ('7', '-'), 'e': ('L', '1'), '-': ('J',), ' ': ('',), 'c': ('r',)},
        {'s': ('7',), 'e': ('r',), '-': ('-',), ' ': ('',)},
        {'s': ('J', '1'), 'e': ('r', '-'), '-': ('L',), ' ': ('',), 'c': ('7',)},
        {'s': ('J',), 'e': ('7',), '-': ('1',), ' ': ('',)},
    )

    # -- Helper functions for making the index that maps clues to patterns --
    def expand_q(acc, counts):
        '''
        Expands a dictionary of the form {clue(string): count(int)}
        into all of its "possible" dictionaries (any ? clues become
        numbers).
        '''
        for i in range(1, 9):
            new_counts = counts.copy()
            if new_counts['?'] <= 1: # base case
                del new_counts['?']
                new_counts[i] = new_counts.get(i, 0) + 1
                acc.add(tuple(sorted(new_counts.items())))
            else:
                new_counts['?'] = new_counts['?'] - 1
                new_counts[i] = new_counts.get(i, 0) + 1
                expand_q(acc, new_counts)

    def calculate_clue_counts(clue_list):
        '''
        Given a list of (string) clues, `clue_list`, calculates the
        frequencies of each one.
        '''
        counts = {}
        for clue in clue_list:
            counts[clue] = counts.get(clue, 0) + 1
        return counts

    # --- end helper functions. ---

    lookup = get_lookup()

    def does_key_match_surroundings(key, adj_indices):
        '''
        Return BoolVar that tells us whether a key (a sorted tuple of (length, frequency) pairs)
        matches the surroundings.

        NOTE: REQUIRES that the pattern and `adj_indices` be generated in a clockwise order
        starting from NW corner.
        '''
        matches_at_least_one_pattern = False
        if key in lookup:
            for pattern in lookup[key]:
                this_pattern_matches_all = True
                for i, (y,x) in enumerate(adj_indices):
                    if is_valid_coord(E.R, E.C, y, x):
                        this_pattern_matches_all &= var_in(ls.grid[y][x], POSITIONAL_SHAPES[i][pattern[i]])
                    else: # trying to handle a cell off the edge
                        if pattern[i] != ' ': # impossible; give up
                            this_pattern_matches_all = False
                            break
                matches_at_least_one_pattern |= this_pattern_matches_all
        return matches_at_least_one_pattern

    # enforce Tapa clues
    if use_tapa_loop:
        for (r,c), clue in tapa_loop[tapa_num].items():
            adj_indices = [ (r+dr,c+dc) for (dr,dc) in
                ((-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1))
            ]
            condition = False # condition that this clue is fulfilled
            clue_counts = calculate_clue_counts(clue)
            if '?' in clue_counts:
                possible_counts = set()
                expand_q(possible_counts, clue_counts)
                for key in possible_counts:
                    condition |= does_key_match_surroundings(key, adj_indices)
            else:
                key = tuple(sorted(clue_counts.items()))
                condition = does_key_match_surroundings(key, adj_indices)
            require(condition)

    solutions = ls.solutions()
    for sol in solutions:
        for r in range(E.R):
            print([ls.grid[r][c].value() for c in range(E.C)])

    return solutions
   
def decode(solutions):
    return utils.decode(solutions)
