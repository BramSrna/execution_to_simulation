from src.simulator.data_stream_types import DataStreamTypes

class WheelController(object):
    def __init__(self, simulator, controller):
        self.simulator = simulator
        self.controller = controller

        self.previous_action = None

        self.simulator.open_data_stream(self.get_id(), DataStreamTypes.CONCRETE_TRANSITIONS)

    def execute_action(self, action):
        self.previous_action = action
        self.controller.execute_action(action)
        self.simulator.notify_new_sensor_value(self.get_id(), action)

    def get_id(self):
        return id(self)        
    
    def get_previous_action(self):
        return self.previous_action
    
    def set_controller(self, new_controller):
        self.controller = new_controller