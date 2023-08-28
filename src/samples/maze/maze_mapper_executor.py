import random

from src.simulator.simulator import Simulator
from src.samples.maze.visual_sensor import VisualSensor
from src.samples.maze.wheel_controller import WheelController
from src.samples.maze.location_sensor import LocationSensor
from src.optimized_task import OptimizedTask
from src.executor.execution_mode import ExecutionMode
from src.executor.executor import Executor
from maze_generator.src.maze_solver_actions import MazeSolverActions

class MazeMapperExecutor(Executor):
    def __init__(self, initial_execution_controller, execution_mode):
        Executor.__init__(self, initial_execution_controller, execution_mode)

        self.visual_sensor = VisualSensor(self.controller)
        self.location_sensor = LocationSensor(self.controller)
        self.wheel_controller = WheelController(self.controller)

        self.performance_mode_algorithm = self._default_performance_mode

    def execute(self):
        num_actions = 0
        self.controller.reset()
        
        max_iterations = 10000
        iter_count = 0
        while (not self.controller.is_complete()) and(iter_count < max_iterations):
            location = self.location_sensor.read()
            possible_directions = self.visual_sensor.read()
            if not (self.controller == self.simulator):
                self.simulator.add_state_info(location, possible_directions, iter_count == 0, False)
            action = self._decide(location, possible_directions)
            self.wheel_controller.execute_action(action)
            num_actions += 1
            if not (self.controller == self.simulator):
                self.simulator.add_transition_info(location, action, self.location_sensor.read())
            iter_count += 1
        location = self.location_sensor.read()
        possible_directions = self.visual_sensor.read()
        if not (self.controller == self.simulator):
            self.simulator.add_state_info(location, possible_directions, iter_count == 0, True)

        if not self.controller.is_complete():
            raise Exception("Could not complete the maze in {} iterations".format(max_iterations))

        return num_actions
    
    def set_controller(self, new_controller):
        Executor.set_controller(self, new_controller)
        self.visual_sensor.set_controller(new_controller)
        self.location_sensor.set_controller(new_controller)
        self.wheel_controller.set_controller(new_controller)
    
    def optimize_task(self):
        max_iter = 100
        counter = 0
        while (not self.simulator.is_ready_for_use()) and (counter < max_iter):
            self.set_execution_mode(ExecutionMode.EXPLORATION)
            self.execute()
            counter += 1
        if not self.simulator.is_ready_for_use():
            raise Exception("Could not get simulator ready for use within {} iterations.".format(max_iter))
        new_optimized_task = OptimizedTask(self.simulator)
        new_optimized_task.optimize()
        self.performance_mode_algorithm = new_optimized_task.decide
    
    def _get_location_sensor(self):
        return self.location_sensor
    
    def _get_visual_sensor(self):
        return self.visual_sensor

    def _decide(self, location, possible_directions):
        if self.execution_mode == ExecutionMode.EXPLORATION:
            return self._exploration_mode(location, possible_directions)
        else:
            return self.performance_mode_algorithm(location, possible_directions)
    
    def _default_performance_mode(self, location, possible_directions):
        # Algorith for "keep your right hand against the wall until you complete the maze"
        action_precedence = [MazeSolverActions.RIGHT, MazeSolverActions.UP, MazeSolverActions.LEFT, MazeSolverActions.DOWN]
        latest_action = self.wheel_controller.get_latest_action()
        if latest_action == MazeSolverActions.RIGHT:
            action_precedence = [MazeSolverActions.DOWN, MazeSolverActions.RIGHT, MazeSolverActions.UP, MazeSolverActions.LEFT]
        elif latest_action == MazeSolverActions.UP:
            action_precedence = [MazeSolverActions.RIGHT, MazeSolverActions.UP, MazeSolverActions.LEFT, MazeSolverActions.DOWN]
        elif latest_action == MazeSolverActions.DOWN:
            action_precedence = [MazeSolverActions.LEFT, MazeSolverActions.DOWN, MazeSolverActions.RIGHT, MazeSolverActions.UP]
        elif latest_action == MazeSolverActions.LEFT:
            action_precedence = [MazeSolverActions.UP, MazeSolverActions.LEFT, MazeSolverActions.DOWN, MazeSolverActions.RIGHT]

        for action in action_precedence:
            if action in possible_directions:
                return action
        return None
    
    def _exploration_mode(self, location, possible_directions):
        uncomplete_states = self.simulator.get_uncomplete_states()
        if len(uncomplete_states) > 0:
            current_state = self.simulator.state_info_to_state(location)
            for transition_name, state_after_transition in current_state.get_transition_tree().items():
                if state_after_transition is None:
                    return transition_name
            return random.choice(possible_directions)
        return self.performance_mode_algorithm(location, possible_directions)
