from .claspy import *

def solve():

    # TODO(himawan): fix the references to '3' everywhere

    # TODO(himawan): figure out how to get input from the frontend
    shapes = {
        1: ((0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0), (0, 0, 1)),
        2: ((0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (2, 1, 1)),
        3: ((0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (0, 1, 1)),
        4: ((0, 0, 0), (1, 0, 0), (1, 0, 1), (1, 0, 2), (0, 1, 0), (0, 1, 1)),
        5: ((0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (0, 2, 0), (0, 2, 1)),
    }

    reset()
    set_max_val(27) # TODO(himawan): parameterize this for the shape of the cube / prism
    
    # --- HELPER METHODS ---
    def canonicalize_shape(shape):
        '''
        Given a shape (a tuple of tuples, where each inner tuple is an
        (x, y, z) coordinate,
        
        Returns a canonicalized version of the shape, which is a tuple
        of (x, y, z) coordinates in sorted order, where the first
        coordinate is (0, 0, 0).
        '''
        shape = sorted(shape)
        root_x, root_y, root_z = shape[0]
        dx, dy, dz = -1*root_x, -1*root_y, -1*root_z
        return tuple((x+dx, y+dy, z+dz) for x, y, z in shape)
    
    def rotate_flat(shape):
        '''
        Return the canonical representation of a shape,
        after the shape has been rotated in the xy plane.
        '''
        return canonicalize_shape((-y, x, z) for x, y, z in shape)
    
    def rotate_z(shape):
        '''
        Return the canonical representation of a shape,
        after the shape has been rotated in the yz plane.
        '''
        return canonicalize_shape((x, -z, y) for x, y, z in shape)
    
    def get_variants(shape):
        '''
        Return all of the variants of a shape which can be achieved
        through rotations (no reflections).
        '''
        functions = [canonicalize_shape, rotate_flat, rotate_z]
        
        # make a set of currently found shapes
        result = set()
        result.add(canonicalize_shape(shape))
        
        # apply our functions to the items in this set,
        # then add the results (new shapes) into the set,
        # and do this repeatedly until the set stops growing
        all_shapes_covered = False
        while not all_shapes_covered:
            new_shapes = set()
            current_num_shapes = len(result)
            for f in functions:
                for s in result:
                    new_shapes.add(f(s))
            result = result.union(new_shapes)
            all_shapes_covered = (current_num_shapes == len(result))
        return result

    def place_shape_in_cube(shape, anchor_x, anchor_y, anchor_z):
        '''
        Place a shape in a cube, where the first coordinate in the shape
        is located at (anchor_x, anchor_y, anchor_z).
        
        Returns None if this is not possible.
        '''
        absolute_coords = []
        for dx, dy, dz in shape:
            x, y, z = anchor_x + dx, anchor_y + dy, anchor_z + dz
            if 0 <= x < 3 and 0 <= y < 3 and 0 <= z < 3:
                absolute_coords.append((x, y, z))
            else:
                return None
        return tuple(absolute_coords)
        
    def rotate_assembled_shapes_flat(shape_ids_tuple):
        '''
        Given a 3D tuple, shape_ids_tuple, where:
         - shape_ids_tuple[0] represents the plane of cells with x-coordinate 0
         - shape_ids_tuple[0][0] represents the line of cells with
         x-coordinate 0 and y-coordinate 0
         
        Returns a rotation of this shape in the xy plane, also in 3D tuple representation.
        '''
        new_shape_ids = {}
        for x in range(0, 3):
            for y in range(0, 3):
                for z in range(0, 3):
                    new_shape_ids[(x, y, z)] = shape_ids_tuple[2-y][x][z]
        return get_assembled_shape_tuples(new_shape_ids)
    
    def rotate_assembled_shapes_z(shape_ids_tuple):
        '''
        Given a 3D tuple, shape_ids_tuple, where:
         - shape_ids_tuple[0] represents the plane of cells with x-coordinate 0
         - shape_ids_tuple[0][0] represents the line of cells with
         x-coordinate 0 and y-coordinate 0
         
        Returns a rotation of this shape in the yz plane, also in 3D tuple representation.
        '''
        new_shape_ids = {}
        for x in range(0, 3):
            for y in range(0, 3):
                for z in range(0, 3):
                    new_shape_ids[(x, y, z)] = shape_ids_tuple[x][2-z][y]
        return get_assembled_shape_tuples(new_shape_ids)
    
    def get_assembled_shape_tuples(shape_ids):
        '''
        Converts a dictionary mapping (x, y, z) to shape id values into
        a 3D tuple representation.
        '''
        shape = [[] for x in range(0, 3)]
        for x in range(0, 3):
            x_layer = [tuple() for y in range(0, 3)]
            for y in range(0, 3):
                y_layer = tuple(shape_ids[(x, y, z)] for z in range(0, 3))
                x_layer[y] += y_layer
            shape[x] = tuple(x_layer)
        return tuple(shape)
        
    def get_assembled_shape_rotations(shape_ids):
        '''
        Given a dictionary of shape_ids, returns 3D tuple representations of
        all of the possible rotations.
        '''
        functions = [rotate_assembled_shapes_flat, rotate_assembled_shapes_z]
        
        # make a set of currently found shapes
        result = set()
        result.add(get_assembled_shape_tuples(shape_ids))
        
        # apply our functions to the items in this set,
        # then add the results (new shapes) into the set,
        # and do this repeatedly until the set stops growing
        all_shapes_covered = False
        while not all_shapes_covered:
            new_shapes = set()
            current_num_shapes = len(result)
            for f in functions:
                for s in result:
                    new_shapes.add(f(s))
            result = result.union(new_shapes)
            all_shapes_covered = (current_num_shapes == len(result))
        return result
    
    # --- BODY OF SOLVE METHOD STARTS HERE ---
    
    # dictionary mapping a shape id to all of its shape variants
    variants = {}
    for shape_id in shapes:
        variants[shape_id] = get_variants(shapes[shape_id])
    
    # dictionary mapping (x, y, z) coordinates to shape ids
    shape_ids = {}
    for x in range(0, 3):
        for y in range(0, 3):
            for z in range(0, 3):
                shape_ids[(x, y, z)] = IntVar(1, 5)
    
    possible_shape_conditions = []
    for x in range(0, 3):
        for y in range(0, 3):
            for z in range(0, 3):
                # for each "type" / shape_id
                for type in variants:
                    # for each variant (a canonical shape representation of one of the type's variants)
                    for variant in variants[type]:
                        # get a list of cells that this variant occupies when its anchor point is (x, y, z)
                        occupied_cells = place_shape_in_cube(variant, x, y, z)
                        # if the shape actually fits in the region
                        if occupied_cells != None:
                            # set all of the occupied cells' values
                            shape_cells = sum_bools(len(variant), [shape_ids[(x2, y2, z2)] == type for (x2, y2, z2) in occupied_cells])
                            # all other cells must not be part of this shape
                            non_shape_cells = []
                            for x2 in range(0, 3):
                                for y2 in range(0, 3):
                                    for z2 in range(0, 3):
                                        if (x2, y2, z2) not in occupied_cells:
                                            non_shape_cells.append(shape_ids[(x2, y2, z2)] != type)
                            non_shape_cells = sum_bools(len(non_shape_cells), non_shape_cells)
                            # the "shape condition" requires that we have a exactly one shape in the region
                            shape_cond = shape_cells & non_shape_cells
                            # keep track of this particular shape condition
                            possible_shape_conditions.append(shape_cond)
    # of the possible shapes, exactly 5 of them are actually correct
    require(sum_bools(5, possible_shape_conditions)) # TODO(himawan): parameterize
    
    solutions = []
    while solve():
        sol = {}
        for x in range(0, 3):
            for y in range(0, 3):
                for z in range(0, 3):
                    sol[(x, y, z)] = shape_ids[(x, y, z)].value()
        solutions.append(sol)
        
        is_same_as_some_rotation = False
        for rotation in get_assembled_shape_rotations(sol):
            is_same_as_this_rotation = True
            for x in range(0, 3):
                for y in range(0, 3):
                    for z in range(0, 3):
                        is_same_as_this_rotation = is_same_as_this_rotation & (shape_ids[(x, y, z)] == rotation[x][y][z])
            is_same_as_some_rotation |= is_same_as_this_rotation
            
        require(~is_same_as_some_rotation)
        
    print(solutions)
    return solutions
