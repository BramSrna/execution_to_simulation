from src.simulator.simulator_controller import SimulatorController

class MazeSimulatorController(SimulatorController):
    def __init__(self, simulator):
        SimulatorController.__init__(self, simulator)

    def get_current_coordinate(self):
        return self.current_state.get_state_key_info()
    
    def get_possible_actions(self):
        return self.current_state.get_possible_transition_names()
    
    def execute_action(self, action_name):
        return self.simulator.get_state_after_action(self.current_state, action_name)