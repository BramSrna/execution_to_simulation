from maze_generator.src.maze_solver_actions import MazeSolverActions

class MazeSolver(object):
    def __init__(self, maze_to_solve):
        self.maze = maze_to_solve

        self.current_coordinate = self.maze.get_starting_coordinate()

        self.reset()
    
    def reset(self):
        self.current_coordinate = self.maze.get_starting_coordinate()
    
    def is_complete(self):
        return self.current_coordinate == self.maze.get_ending_coordinate()
    
    def execute_action(self, action_to_execute):
        if action_to_execute == MazeSolverActions.RIGHT:
            self._move_right()
        elif action_to_execute == MazeSolverActions.UP:
            self._move_up()
        elif action_to_execute == MazeSolverActions.LEFT:
            self._move_left()
        elif action_to_execute == MazeSolverActions.DOWN:
            self._move_down()
        else:
            raise Exception("Unknown action to execute: {}".format(action_to_execute))
        
    def get_possible_actions(self):
        if self.current_coordinate == self.maze.get_ending_coordinate():
            return []
        
        possible_actions = []
        if self.maze.is_coordinate_free(self.current_coordinate[0] - 1, self.current_coordinate[1]):
            possible_actions.append(MazeSolverActions.LEFT)
        if self.maze.is_coordinate_free(self.current_coordinate[0] + 1, self.current_coordinate[1]):
            possible_actions.append(MazeSolverActions.RIGHT)
        if self.maze.is_coordinate_free(self.current_coordinate[0], self.current_coordinate[1] - 1):
            possible_actions.append(MazeSolverActions.DOWN)
        if self.maze.is_coordinate_free(self.current_coordinate[0], self.current_coordinate[1] + 1):
            possible_actions.append(MazeSolverActions.UP)

        return possible_actions
    
    def get_current_coordinate(self):
        return self.current_coordinate
    
    def get_starting_coordinate(self):
        return self.maze.get_starting_coordinate()
    
    def get_maze(self):
        return self.maze
    
    def _move_left(self):
        new_x = self.current_coordinate[0] - 1
        new_y = self.current_coordinate[1]
        if self.maze.is_coordinate_free(new_x, new_y):
            self.current_coordinate = (new_x, new_y)
        return self.current_coordinate
    
    def _move_right(self):
        new_x = self.current_coordinate[0] + 1
        new_y = self.current_coordinate[1]
        if self.maze.is_coordinate_free(new_x, new_y):
            self.current_coordinate = (new_x, new_y)
        return self.current_coordinate
    
    def _move_down(self):
        new_x = self.current_coordinate[0]
        new_y = self.current_coordinate[1] - 1
        if self.maze.is_coordinate_free(new_x, new_y):
            self.current_coordinate = (new_x, new_y)
        return self.current_coordinate
    
    def _move_up(self):
        new_x = self.current_coordinate[0]
        new_y = self.current_coordinate[1] + 1
        if self.maze.is_coordinate_free(new_x, new_y):
            self.current_coordinate = (new_x, new_y)
        return self.current_coordinate