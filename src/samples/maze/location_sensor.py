from src.observer_pattern.observable import Observable

class LocationSensor(Observable):
    def __init__(self, maze):
        Observable.__init__(self)
        self.controller = maze
        
        self.readings = []

    def get_id(self):
        return id(self)

    def read(self):
        reading = self.controller.get_current_coordinate()
        self.readings.append(reading)
        self.notify()
        return reading
    
    def get_latest_reading(self):
        if len(self.readings) > 0:
            return self.readings[-1]
        return None
    
    def set_controller(self, new_controller):
        self.controller = new_controller
