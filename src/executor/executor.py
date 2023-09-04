from src.simulator.simulator import Simulator

class Executor(object):
    def __init__(self, initial_execution_controller, execution_mode):
        self.controller = initial_execution_controller
        self.execution_mode = execution_mode

        self.simulator = Simulator()

    def get_simulator(self):
        return self.simulator

    def execute(self):
        raise NotImplementedError("The execute method must be implemented by the child class.")
    
    def optimize_task(self):
        raise NotImplementedError("The optimize_task method must be implemented by the child class.")
    
    def set_controller(self, new_controller):
        self.controller = new_controller

    def set_execution_mode(self, new_execution_mode):
        self.execution_mode = new_execution_mode

    def _has_visited(self, location, direction):
        return self.simulator.get_state_info_after_action(location, direction) is None