from src.simulator.data_stream_types import DataStreamTypes

class VisualSensor(object):
    def __init__(self, simulator, maze):
        self.simulator = simulator
        self.controller = maze

        self.simulator.open_data_stream(self.get_id(), DataStreamTypes.POSSIBLE_TRANSITIONS)

    def get_id(self):
        return id(self)

    def read(self):
        reading = self.controller.get_possible_actions()
        self.simulator.notify_new_sensor_value(self.get_id(), reading)
        return reading
    
    def set_controller(self, new_controller):
        self.controller = new_controller
