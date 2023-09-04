import random

class Maze(object):
    OPEN_SPACE = "0"
    WALL = "|"

    def __init__(self, x_len, y_len):
        self.x_len = x_len
        self.y_len = y_len

        self._create_new_maze()

    def get_starting_coordinate(self):
        return self.starting_coordinate
    
    def get_ending_coordinate(self):
        return self.ending_coordinate
    
    def is_coordinate_free(self, x_coord, y_coord):
        if (x_coord < 0) or (y_coord < 0) or (x_coord >= self.x_len) or (y_coord >= self.y_len):
            return False
        return self.maze[x_coord][y_coord] == self.OPEN_SPACE
    
    def _create_new_maze(self):
        self.maze = []
        for x in range(self.x_len):
            col = []
            for y in range(self.y_len):
                if (x % 2 == 1) and (y % 2 == 1):
                    col.append(self.OPEN_SPACE)
                else:
                    col.append(self.WALL)
            self.maze.append(col)

        self.visited = []
        for x in range(self.x_len):
            for y in range(self.y_len):
                if (x % 2 == 1) and (y % 2 == 1):
                    self._populate(x, y)

        possible_start_end_coordinates = []
        for x in range(self.x_len):
            for y in range(self.y_len):
                on_outer_bound = (x == 0) or (x == self.x_len - 1) or (y == 0) or (y == self.y_len - 1)
                connected_to_free_spot = self.is_coordinate_free(x, y - 1) or \
                    self.is_coordinate_free(x, y + 1) or \
                    self.is_coordinate_free(x - 1, y) or \
                    self.is_coordinate_free(x + 1, y)
                if on_outer_bound and connected_to_free_spot:
                    possible_start_end_coordinates.append((x, y))
        assert(len(possible_start_end_coordinates) >= 2)

        self.starting_coordinate = random.sample(possible_start_end_coordinates, 1)[0]
        self.ending_coordinate = self.starting_coordinate
        while self.ending_coordinate == self.starting_coordinate:
            self.ending_coordinate = random.sample(possible_start_end_coordinates, 1)[0]

        self.maze[self.starting_coordinate[0]][self.starting_coordinate[1]] = self.OPEN_SPACE
        self.maze[self.ending_coordinate[0]][self.ending_coordinate[1]] = self.OPEN_SPACE

    def _populate(self, starting_x_coord, starting_y_coord):
        # https://en.wikipedia.org/wiki/Maze_generation_algorithm

        self.visited.append((starting_x_coord, starting_y_coord))
        unvisited_neighbours = self._get_unvisited_neighbours(starting_x_coord, starting_y_coord)
        while len(unvisited_neighbours) > 0:
            new_coordinate = unvisited_neighbours[random.randint(0, len(unvisited_neighbours) - 1)]
            wall_to_clear_x = int(starting_x_coord - (starting_x_coord - new_coordinate[0]) / 2)
            wall_to_clear_y = int(starting_y_coord - (starting_y_coord - new_coordinate[1]) / 2)
            self.maze[wall_to_clear_x][wall_to_clear_y] = self.OPEN_SPACE
            self._populate(new_coordinate[0], new_coordinate[1])
            unvisited_neighbours = self._get_unvisited_neighbours(starting_x_coord, starting_y_coord)

    def _get_unvisited_neighbours(self, x_coordinate, y_coordinate):
        adjacent_coordinates = [
            (x_coordinate, y_coordinate - 2),
            (x_coordinate, y_coordinate + 2),
            (x_coordinate - 2, y_coordinate),
            (x_coordinate + 2, y_coordinate)
        ]
        
        possible_coordinates = []
        for coordinate in adjacent_coordinates:
            if (coordinate[0] > 0) and (coordinate[0] < self.x_len - 1) and (coordinate[1] > 0) and (coordinate[1] < self.y_len - 1):
                if coordinate not in self.visited:
                    possible_coordinates.append(coordinate)
        return possible_coordinates
    
    def __str__(self):
        ret_str = ""
        y_coord = self.y_len - 1
        while (y_coord >= 0):
            x_coord = 0
            while (x_coord < self.x_len):
                ret_str += " " + self.maze[x_coord][y_coord]
                x_coord += 1
            ret_str += "\n"
            y_coord -= 1
        return ret_str


