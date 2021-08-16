from .claspy import *

# this is from Reddothunt 2019 I think (-Michael 5/19/2021)

def solve():
    reset()
    set_max_val(100) # TODO(himawan): optimize

    adjacency_list = {
        1: [2, 3, 4, 48],
        2: [1, 5, 11],
        3: [1, 15],
        4: [16, 19, 1],
        5: [20, 7, 2],
        6: [7],
        7: [6, 5, 8, 31],
        8: [7, 9],
        9: [8, 10],
        10: [9, 11],
        11: [2, 10, 49, 32],
        12: [13],
        13: [12, 14],
        14: [13, 15],
        15: [14, 3, 23],
        16: [4, 18],
        17: [18, 27],
        18: [16, 17, 27],
        19: [4, 20, 29],
        20: [19, 5, 21, 30],
        21: [20, 50, 31, 30],
        22: [23, 35],
        23: [22, 15, 24],
        24: [23, 25, 35, 33, 43],
        25: [48, 24, 26],
        26: [25, 45, 47],
        27: [17, 18, 28],
        28: [27, 38, 29],
        29: [28, 19, 32],
        30: [20, 21, 31, 32],
        31: [7, 21, 30],
        32: [30, 29, 33, 11],
        33: [24, 32, 38, 39],
        35: [36, 24, 22],
        36: [35],
        37: [38, 39],
        38: [37, 28, 33, 39],
        39: [37, 38, 33, 42, 40],
        40: [39, 41],
        41: [40, 42],
        42: [39, 41, 43, 44, 47],
        43: [24, 42],
        44: [45, 42],
        45: [46, 26, 44],
        46: [45],
        47: [42, 26],
        48: [1, 25],
        49: [11],
        50: [21, 51],
        51: [50]
    }
    is_clicked = {}
    for region_id in adjacency_list:
        is_clicked[region_id] = BoolVar()
    is_on = {}
    for region_id in adjacency_list:
        is_on[region_id] = BoolVar()
    for region_id in adjacency_list:
        neighbors_clicked = IntVar(0)
        for neighbor_id in adjacency_list[region_id]:
            neighbors_clicked += is_clicked[neighbor_id]
        self_clicked = is_clicked[region_id]
        for i in range(len(adjacency_list[region_id])+2):
            if i % 2 == 0:
                # if neighbors_clicked + self_clicked is an even number,
                # the region must be off
                require(~is_on[region_id] | ((neighbors_clicked + self_clicked) != i))
            else:
                require(is_on[region_id] | ((neighbors_clicked + self_clicked) != i))
        require(is_on[region_id])
        
    solutions = []
    while solve():
        # form the solution
        solution = []
        for region_id in adjacency_list:
            if is_clicked[region_id].value():
                solution.append(region_id)
        
        # require that the next solution is not exactly the same as the one before
        x = True
        for region_id in adjacency_list:
            x = x & (is_clicked[region_id] == is_clicked[region_id].value())
        require(~x)
        
        # minimize the number of regions clicked
        num_regions_to_click = IntVar(0)
        num_regions_actual_clicked = 0
        for region_id in adjacency_list:
            num_regions_to_click += cond(is_clicked[region_id], 1, 0)
            if is_clicked[region_id].value():
                num_regions_actual_clicked += 1
        require(num_regions_to_click <= num_regions_actual_clicked)
        solutions.append(solution)
        
    for solution in solutions:
        print(solution)
