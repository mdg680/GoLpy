"""
This module contains the the grid and its methods
"""

class Grid(object):
    """
    This class represents the grid/board, and the methods for manipulating it
    and its contents
    """

    def __init__(self, spec=None):
        """ Creates an grid instance

        Args:
            spec (tuple(int, int)): Initialises the Grid object as an empty grid
                , with the dimensions given in the tuple (height, width)

                OR

            spec (list): Initialises the Grid object as a predefined grid, given
                by a list
        """

        import numpy as np
        from sets import Set

        if isinstance(spec, tuple):
            if not isinstance(spec[0], int) or not isinstance(spec[1], int):
                raise Exception('Arguments in touple must be integers')
            self.height = spec[0]
            self.width = spec[1]
            self.array = np.zeros((self.height, self.width), dtype='int32')
            self.cell_neighbor_table = self.get_cell_neighbor_table(self.array)
            self.cell_visits = Set([])
            self.cell_is_alive = Set([])

        elif isinstance(spec, list):
            list_length_check = len(spec[0])
            for i in spec:
                if not isinstance(i, list):
                    raise Exception('Must be a list of lists')
                if len(i) != list_length_check:
                    raise Exception('lists in list must be of equal length')
            self.array = spec
            self.height = self.get_height()
            self.width = self.get_width()

        elif spec is None:
            raise Exception('No arguments given.')

        else:
            raise Exception('invalid arguments.')

    def get_array(self):
        return self.array

    def get_height(self):
        return len(self.array)

    def get_width(self):
        return len(self.array[0])

    def rand_fill(self):
        """
        Fills up the grid with random values of either 0 (dead cell) or 1 (live cell)
        """
        import random
        for(i, row) in enumerate(self.array):
            for (j, value) in enumerate(row):
                self.array[i][j] = random.randrange(2)
                if self.array[i][j] == 1:
                    self.cell_visits.add((i, j))
                    self.cell_is_alive.add((i, j))
                    self.cell_visits.update(self.cell_neighbors(i, j))

    def iterate(self):

        import numpy as np
        tmp_array = np.zeros((self.get_height(), self.get_width()), dtype='int32')
        for (i, row) in enumerate(self.array):
            for(j, value) in enumerate(row):
                #live_neigbors = self.number_of_live_cells(self.cell_neighbors(i, j))
                live_neigbors = self.number_of_live_cells(self.cell_neighbor_table[i][j])
                if value == 1 and live_neigbors < 2:
                    tmp_array[i][j] = 0
                if value == 1 and live_neigbors == 2 or live_neigbors == 3:
                    tmp_array[i][j] = 1
                if value == 1 and live_neigbors > 3:
                    tmp_array[i][j] = 0
                if value == 0 and live_neigbors == 3:
                    tmp_array[i][j] = 1
        self.array = tmp_array

    def iterate_optimized(self):

        import numpy as np
        from sets import Set
        tmp_array = np.zeros((self.get_height(), self.get_width()), dtype='int32')
        v_set = Set([])
        for x in self.cell_visits:
            i = x[0]
            j = x[1]
            live_neigbors = self.number_of_live_cells(self.cell_neighbor_table[i][j])
            if self.array[i][j] == 1 and live_neigbors < 2:
                tmp_array[i][j] = 0
            if self.array[i][j] == 1 and live_neigbors == 2 or live_neigbors == 3:
                tmp_array[i][j] = 1
                v_set.update(self.cell_neighbor_table[i][j])
                v_set.add((i, j))
            if self.array[i][j] == 1 and live_neigbors > 3:
                tmp_array[i][j] = 0
            if self.array[i][j] == 0 and live_neigbors == 3:
                tmp_array[i][j] = 1
                v_set.update(self.cell_neighbor_table[i][j])
                v_set.add((i, j))
        self.cell_visits = v_set
        self.array = tmp_array

    

    
    def parallel_chunk(self, tmp_array, v_set, index_start, index_end):
        for x in self.array[index_start:index_end]:
            i = x[0]
            j = x[1]
            live_neigbors = self.number_of_live_cells(self.cell_neighbor_table[i][j])
            if self.array[i][j] == 1 and live_neigbors < 2:
                tmp_array[i][j] = 0
            if self.array[i][j] == 1 and live_neigbors == 2 or live_neigbors == 3:
                tmp_array[i][j] = 1
                v_set.update(self.cell_neighbor_table[i][j])
                v_set.add((i, j))
            if self.array[i][j] == 1 and live_neigbors > 3:
                tmp_array[i][j] = 0
            if self.array[i][j] == 0 and live_neigbors == 3:
                tmp_array[i][j] = 1
                v_set.update(self.cell_neighbor_table[i][j])
                v_set.add((i, j))

    def iterate_parallel(self):
        import numpy as np
        import multiprocessing as mp
        from sets import Set
        tmp_array = np.zeros((self.get_height(), self.get_width()), dtype='int32')
        v_set = Set([])

        p1 = mp.Process(target=self.parallel_chunk, args=(tmp_array, v_set, 0, len(self.cell_visits),))
        p1.start()
        p1.join()

        self.cell_visits = v_set
        self.array = tmp_array

    def cell_neighbors(self, x_pos, y_pos):
        """
        Returns a list of tuples, representing the positions on the grid of
        the neighbors of the cell of index[x_pos][y_pos]

        Args:
            x_pos (int): the x position of the cell in the grid
            y_pos (int): the y position of the cell in the grid
        Returns:
            list(tuple): list of positions in tuples

            TO DO: do something
        """
        neighbors = [(neigbor_x_pos, neighbor_y_pos) for neigbor_x_pos in range(x_pos-1, x_pos+2)
                     for neighbor_y_pos in range(y_pos-1, y_pos+2)
                     # ignore if any of the indices sits outside the current grid
                     if (-1 < x_pos <= self.get_height() and # TODO: height and width have been swapped in this function, might be worth looking into it further!
                         -1 < y_pos <= self.get_width() and
                         # skip the indice itself, as we only want the sorrounding neighbors
                         (x_pos != neigbor_x_pos or y_pos != neighbor_y_pos) and
                         # dont add any positions outside the bounds of the array
                         (0 <= neigbor_x_pos < self.get_height()) and
                         (0 <= neighbor_y_pos < self.get_width()))]
        return neighbors

    def number_of_live_cells(self, positions):
        """
        Calculates the sum of live cells present in the position range

        Args:
            positions (tuple(int, int)): List of positions
        Returns:
            _sum (int): Total number of live cells in position range
        """
        _sum = 0
        for (x_pos, y_pos) in positions:
            _sum += self.array[x_pos][y_pos]
        return _sum

    # this is faste (almost 3 times faster), but doesnt work correctly
    def number_of_live_cells2(self, x_pos, y_pos):
        _sum = 0

        if x_pos != 0:
            _sum += self.array[y_pos][x_pos -1]
        if x_pos < self.get_width() -1:
            _sum += self.array[y_pos][x_pos +1]
        if y_pos != 0:
            _sum += self.array[y_pos -1][x_pos]
        if y_pos < self.get_height() -1:
            _sum += self.array[y_pos +1][x_pos]
        if y_pos != 0 and x_pos != 0:
            _sum += self.array[y_pos -1][x_pos -1]
        if y_pos < self.get_height() -1 and x_pos < self.get_width() -1:
            _sum += self.array[y_pos +1][x_pos +1]
        if y_pos != 0 and x_pos < self.get_width() -1:
            _sum += self.array[y_pos -1][x_pos +1]
        if y_pos < self.get_height() -1 and x_pos != 0:
            _sum += self.array[y_pos +1][x_pos -1]
        
        return _sum

    def get_cell_neighbor_table(self, array):
        import numpy as np

        table = np.zeros((self.get_height(), self.get_width()), dtype='object')
        for(i, row) in enumerate(array):
            for(j, value) in enumerate(row):
                table[i][j] = self.cell_neighbors(i, j)
        return table

"""
        if x == 0 and y == 0:
            sum =  self.array[y_pos][x_pos + 1] 
                 + self.array[y_pos + 1][x_pos] 
                 + self.array[y_pos + 1][x_pos + 1]
        elif x == 0 and y == self:
            sum = self.array[]
"""
