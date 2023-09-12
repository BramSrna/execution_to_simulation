import logging
import unittest
import pytest

from maze_generator.src.maze import Maze
from src.samples.maze.maze_mapper_executor import MazeMapperExecutor
from src.executor.execution_mode import ExecutionMode
from maze_generator.src.maze_solver import MazeSolver
from src.samples.maze.maze_simulator_controller import MazeSimulatorController
from maze_generator.src.maze_solver_actions import MazeSolverActions
    

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

    def test_states_mapped_by_simulator_match_actual_states(self):
        test_executor = MazeMapperExecutor(self.maze_solver, ExecutionMode.PERFORMANCE)
        test_executor.execute()
        simulator = test_executor.get_simulator()
        simulator_controller = MazeSimulatorController(simulator)

        simulator_states = simulator.get_known_states()
        self.assertGreater(len(simulator_states), 0)
        for state in simulator_states:
            simulator_controller.set_state(state)
            original_location = simulator_controller.get_current_coordinate()
            possible_actions = simulator_controller.get_possible_actions()
            if not simulator_controller.is_complete():
                self.assertGreater(len(possible_actions), 0)
            else:
                self.assertEqual(0, len(possible_actions))
            original_state = state
            for action in possible_actions:
                simulator_controller.set_state(original_state)
                simulator_controller.execute_action(action)
                new_location = simulator_controller.get_current_coordinate()
                if action == MazeSolverActions.RIGHT:
                    self.assertEqual(original_location[0] + 1, new_location[0])
                    self.assertEqual(original_location[1], new_location[1])
                elif action == MazeSolverActions.LEFT:
                    self.assertEqual(original_location[0] - 1, new_location[0])
                    self.assertEqual(original_location[1], new_location[1])
                elif action == MazeSolverActions.UP:
                    self.assertEqual(original_location[0], new_location[0])
                    self.assertEqual(original_location[1] + 1, new_location[1])
                elif action == MazeSolverActions.DOWN:
                    self.assertEqual(original_location[0], new_location[0])
                    self.assertEqual(original_location[1] - 1, new_location[1])
                else:
                    raise Exception("Unknown action: {}".format(action))

    def test_simulator_will_arrive_at_final_state_after_executor_runs_using_simulator_as_execution_context(self):
        test_executor = MazeMapperExecutor(self.maze_solver, ExecutionMode.PERFORMANCE)
        test_executor.execute()
        simulator = test_executor.get_simulator()
        simulator_controller = MazeSimulatorController(simulator)

        test_executor.set_controller(simulator_controller)
        simulator_controller.reset()
        self.assertFalse(simulator_controller.is_complete())
        simulator.set_accept_new_data(False)
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

    @pytest.mark.skip(reason="https://stackoverflow.com/questions/38442897/how-do-i-disable-a-test-using-pytest")
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