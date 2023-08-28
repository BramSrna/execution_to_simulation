import logging
import unittest

from maze_generator.src.maze import Maze
from maze_generator.src.maze_solver_actions import MazeSolverActions
from maze_generator.src.maze_solver import MazeSolver
    
def simple_solver_algorithm(previous_action, possible_actions):
    # Algorith for "keep your right hand against the wall until you complete the maze"
    action_precedence = [MazeSolverActions.RIGHT, MazeSolverActions.UP, MazeSolverActions.LEFT, MazeSolverActions.DOWN]
    if previous_action == MazeSolverActions.RIGHT:
        action_precedence = [MazeSolverActions.DOWN, MazeSolverActions.RIGHT, MazeSolverActions.UP, MazeSolverActions.LEFT]
    elif previous_action == MazeSolverActions.UP:
        action_precedence = [MazeSolverActions.RIGHT, MazeSolverActions.UP, MazeSolverActions.LEFT, MazeSolverActions.DOWN]
    elif previous_action == MazeSolverActions.DOWN:
        action_precedence = [MazeSolverActions.LEFT, MazeSolverActions.DOWN, MazeSolverActions.RIGHT, MazeSolverActions.UP]
    elif previous_action == MazeSolverActions.LEFT:
        action_precedence = [MazeSolverActions.UP, MazeSolverActions.LEFT, MazeSolverActions.DOWN, MazeSolverActions.RIGHT]

    for action in action_precedence:
        if action in possible_actions:
            return action
    return None

class TestMazeSolver(unittest.TestCase):
    def test_maze_solver_can_solve_maze(self):
        for _ in range(100):
            num_rows = 11
            num_cols = 11
            generated_maze = Maze(num_rows, num_cols)
            print(generated_maze)
            maze_solver = MazeSolver(generated_maze)
            maze_solver.reset()
            self.assertFalse(maze_solver.is_complete())
            self.assertEqual(generated_maze.get_starting_coordinate(), maze_solver.get_current_coordinate())
            max_iter = 1000
            curr_iter = 0
            prev_action = None
            while (not maze_solver.is_complete()) and (curr_iter < max_iter):
                possible_actions = maze_solver.get_possible_actions()
                next_action = simple_solver_algorithm(prev_action, possible_actions)
                maze_solver.execute_action(next_action)
                prev_action = next_action
                curr_iter += 1
            self.assertTrue(maze_solver.is_complete())
            self.assertEqual(generated_maze.get_ending_coordinate(), maze_solver.get_current_coordinate())

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()