class SimulatorController(object):
    def __init__(self, simulator):
        self.simulator = simulator

        self.current_state = self.simulator.get_start_state()

        self.reset()

    def reset(self):
        self.current_state = self.simulator.get_start_state()

    def is_complete(self):
        print(self.current_state, self.simulator.get_end_state())
        return self.current_state == self.simulator.get_end_state()
    
    def get_current_state(self):
        return self.current_state
    
    def set_state(self, new_state):
        self.current_state = new_state