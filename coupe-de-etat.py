from .claspy import *
from . import utils
from .utils.solutions import *

def encode(string):
    return utils.encode(string, clue_encoder = lambda s : s)
    
def solve(E):
    set_max_val(100)

    cars = {
        'Doc Hudson',
        'Lightning McQueen',
        'Ramone',
        'Chick Hicks',
        'Luigi',
        'Flik Car'
    }

    former_cars = [MultiVar(*cars) for i in range(6)]
    former_lens = [IntVar(1, 5) for i in range(6)]

    latter_cars = [MultiVar(*cars) for i in range(6)]
    latter_lens = [IntVar(1, 5) for i in range(6)]

    # Rule 1
    require_all_diff(former_cars)
    require_all_diff(latter_cars)

    # Rule 2
    for c in cars:
        former_total = IntVar(0)
        latter_total = IntVar(0)
        for i in range(6):
            require(former_lens[i] <= 5)
            require(latter_lens[i] <= 5)
            former_total += cond(former_cars[i] == c, former_lens[i], 0)
            latter_total += cond(latter_cars[i] == c, latter_lens[i], 0)
        require((former_total + latter_total) <= 9)

    # Rule 3
    for i in range(6):
        for j in range(6):
            require((former_lens[i] == (latter_lens[j]+latter_lens[j]))
                | ~((former_cars[i] == 'Doc Hudson') & (latter_cars[j] == 'Doc Hudson'))
            )

    # Rule 4
    require(
        sum_bools(1, [former_lens[i] == 4 for i in range(6)])
    )
    for i in range(5):
        require((former_cars[i+1] == latter_cars[1])
            | (former_lens[i] != 4)
        )

    # Rule 5
    for c in cars:
        for i in range(6):
            for j in range(6):
                require(~((former_cars[i] == c) & (latter_cars[j] == c) & (former_lens[i] == latter_lens[j])))

    # Rule 6
    former_total = IntVar(0)
    latter_total = IntVar(0)
    for i in range(6):
        former_total += former_lens[i]
        latter_total += latter_lens[i]
    require(latter_total > former_total)

    # Rule 7
    require(
        sum_bools(1, [latter_lens[i] == 5 for i in range(6)])
    )
    at_least_one_7 = BoolVar(False)
    for c1 in cars:
        for c2 in cars:
            car_total = IntVar(0)
            for i in range(6):
                car_total += cond(former_cars[i] == c2, former_lens[i], 0)
                car_total += cond(latter_cars[i] == c2, latter_lens[i], 0)
            for i in range(5):
                for j in range(6):
                    at_least_one_7 |= (
                        ((former_cars[i+1] == c1) & 
                            (former_cars[i] == c2) &
                            (car_total == 4) &
                            (latter_cars[j] == c1) & (latter_lens[j] == 5)
                        )
                    )
                    at_least_one_7 |= (
                        ((latter_cars[i+1] == c1) & 
                            (latter_cars[i] == c2) &
                            (car_total == 4) &
                            (latter_cars[j] == c1) & (latter_lens[j] == 5)
                        )
                    )
    require(at_least_one_7)

    # Rule 8
    require(sum_bools(1, [former_cars[i] == latter_cars[i] for i in range(6)]))
    for i in range(1, 5):
        require(
            (((former_cars[i-1] == 'Luigi') & (former_cars[i+1] == 'Doc Hudson')) |
             ((former_cars[i-1] == 'Luigi') & (latter_cars[i+1] == 'Doc Hudson')) |
             ((latter_cars[i-1] == 'Luigi') & (former_cars[i+1] == 'Doc Hudson')) |
             ((latter_cars[i-1] == 'Luigi') & (latter_cars[i+1] == 'Doc Hudson'))
            )
            | (former_cars[i] != latter_cars[i])
        )

    # Rule 9
    # Lightning > Ramone
    lightning_total = IntVar(0)
    ramone_total = IntVar(0)
    for i in range(6):
        lightning_total += cond(former_cars[i] == 'Lightning McQueen', former_lens[i], 0)
        lightning_total += cond(latter_cars[i] == 'Lightning McQueen', latter_lens[i], 0)

        ramone_total += cond(former_cars[i] == 'Ramone', former_lens[i], 0)
        ramone_total += cond(latter_cars[i] == 'Ramone', latter_lens[i], 0)
    require(lightning_total > ramone_total)
    # Other car < Ramone
    other_car_totals = []
    for c in cars:
        if c not in ('Lightning McQueen', 'Ramone'):
            car_total = IntVar(0)
            for i in range(6):
                car_total += cond(former_cars[i] == c, former_lens[i], 0)
                car_total += cond(latter_cars[i] == c, latter_lens[i], 0)
            other_car_totals.append(car_total)
    require(at_least(1, [other_car_totals[i] < ramone_total for i in range(len(other_car_totals))]))

    # Rule 10
    # Partial.
    multiple_3 = [6, 9]
    chick_total = IntVar(0)
    for i in range(6):
        chick_total += cond(former_cars[i] == 'Chick Hicks', former_lens[i], 0)
        chick_total += cond(latter_cars[i] == 'Chick Hicks', latter_lens[i], 0)
    require(var_in(chick_total, multiple_3))
    other_car_totals = []
    for c in cars:
        if c != 'Chick Hicks':
            car_total = IntVar(0)
            for i in range(6):
                car_total += cond(former_cars[i] == c, former_lens[i], 0)
                car_total += cond(latter_cars[i] == c, latter_lens[i], 0)
            other_car_totals.append(car_total)
    require(at_least(1, [other_car_totals[i] == chick_total for i in range(len(other_car_totals))]))

    # Rule 11
    require((latter_cars[2] == 'Doc Hudson') | (latter_cars[2] == 'Ramone'))

    # Rule 12
    require(
        ((former_cars[5] == 'Luigi') & (latter_cars[5] == 'Flik Car')) |
        ((latter_cars[5] == 'Luigi') & (former_cars[5] == 'Flik Car'))
    )
    require(
        (former_lens[5] == latter_lens[5] + 3) |
        (latter_lens[5] == former_lens[5] + 3)
    )

    # Rule 13
    require(
        ((former_cars[0] == 'Chick Hicks') & (latter_cars[0] == 'Flik Car')) |
        ((latter_cars[0] == 'Chick Hicks') & (former_cars[0] == 'Flik Car'))
    )
    require(former_lens[0] == 3)

    # Rule 14
    odd_numbers = list(range(1, 6, 2))
    require(
        sum_bools(1, [var_in(former_lens[1], odd_numbers), var_in(latter_lens[1], odd_numbers)])
    )

    # Rule 15
    require(former_total + latter_total == 35)

    sol_count = 0
    while claspy_solve():
        for i in range(6):
            print('\t'.join((str(former_cars[i].value()), 
                str(former_lens[i].value()), 
                str(latter_cars[i].value()), 
                str(latter_lens[i].value()))))
        x = BoolVar(True)
        for i in range(6):
            x &= (former_cars[i] == former_cars[i].value())
            x &= (former_lens[i] == former_lens[i].value())
            x &= (latter_cars[i] == latter_cars[i].value())
            x &= (latter_lens[i] == latter_lens[i].value())
        require(~x)
        sol_count += 1

    return []
   
def decode(solutions):
    return utils.decode(solutions)
