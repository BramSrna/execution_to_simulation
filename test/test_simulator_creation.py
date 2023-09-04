import logging
import unittest

from maze_generator.src.maze import Maze
from src.samples.maze.maze_mapper_executor import MazeMapperExecutor
from src.executor.execution_mode import ExecutionMode
from maze_generator.src.maze_solver import MazeSolver
from src.samples.maze.maze_simulator_controller import MazeSimulatorController
    

class TestSimulatorCreation(unittest.TestCase):
    def setUp(self):
        self.maze = Maze(11, 11)
        self.maze_solver = MazeSolver(self.maze)

    def test_executor_will_generate_a_simulator_while_executing(self):
        test_executor = MazeMapperExecutor(self.maze_solver, ExecutionMode.PERFORMANCE)
        test_executor.execute()
        simulator = test_executor.get_simulator()

        start_state = simulator.get_start_state()

        expected_start_location = self.maze_solver.get_starting_coordinate()
        actual_start_location = start_state.get_state_key_info()
        self.assertEqual(expected_start_location, actual_start_location)

        self.maze_solver.reset()
        expected_start_actions = self.maze_solver.get_possible_actions()
        actual_start_actions = start_state.get_possible_transition_names()
        self.assertEqual(expected_start_actions, actual_start_actions)

    def test_simulator_will_arrive_at_final_state_after_executor_runs_using_simulator_as_execution_context(self):
        test_executor = MazeMapperExecutor(self.maze_solver, ExecutionMode.PERFORMANCE)
        test_executor.execute()
        simulator = test_executor.get_simulator()
        simulator_controller = MazeSimulatorController(simulator)

        test_executor.set_controller(simulator_controller)
        simulator_controller.reset()
        self.assertFalse(simulator_controller.is_complete())
        test_executor.execute()
        self.assertTrue(simulator_controller.is_complete())

    def test_simulator_will_be_marked_ready_when_exploration_threshold_is_hit(self):
        test_executor = MazeMapperExecutor(self.maze_solver, ExecutionMode.PERFORMANCE)
        simulator = test_executor.get_simulator()
        self.assertFalse(simulator.is_ready_for_use())
        test_executor.set_execution_mode(ExecutionMode.EXPLORATION)
        max_iterations = 100
        curr_iteration = 0
        while (curr_iteration < max_iterations) and (not simulator.is_ready_for_use()):
            self.maze_solver.reset()
            test_executor.execute()
            curr_iteration += 1
        self.assertTrue(simulator.is_ready_for_use())

    def test_simulator_can_be_used_to_generate_better_execution_strategies(self):
        test_executor = MazeMapperExecutor(self.maze_solver, ExecutionMode.EXPLORATION)
        test_executor.execute()

        test_executor.set_execution_mode(ExecutionMode.PERFORMANCE)
        start_num_actions = test_executor.execute()

        test_executor.optimize_task()
        
        end_num_actions = test_executor.execute()

        self.assertLessEqual(end_num_actions, start_num_actions)




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()