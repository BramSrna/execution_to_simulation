from src.simulator.data_stream_types import DataStreamTypes

class LocationSensor(object):
    def __init__(self, simulator, maze):
        self.simulator = simulator
        self.controller = maze

        self.simulator.open_data_stream(self.get_id(), DataStreamTypes.STATE_ID)

    def get_id(self):
        return id(self)

    def read(self):
        reading = self.controller.get_current_coordinate()
        self.simulator.notify_new_sensor_value(self.get_id(), reading)
        return reading
    
    def set_controller(self, new_controller):
        self.controller = new_controller
