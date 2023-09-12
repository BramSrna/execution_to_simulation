from src.simulator.simulator_controller import SimulatorController

class MazeSimulatorController(SimulatorController):
    def __init__(self, simulator):
        SimulatorController.__init__(self, simulator)

    def get_current_coordinate(self):
        return self.current_state.get_state_key_info()
    
    def get_possible_actions(self):
        unfiltered_names = self.current_state.get_possible_transition_names()
        filtered_names = []
        for transition_name in unfiltered_names:
            if self.simulator.get_state_after_action(self.current_state, transition_name) is not None:
                filtered_names.append(transition_name)
        return filtered_names
    
    def execute_action(self, action_name):
        self.current_state = self.simulator.get_state_after_action(self.current_state, action_name)
        return self.current_state