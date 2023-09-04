from src.observer_pattern.observable import Observable

class WheelController(Observable):
    def __init__(self, controller):
        Observable.__init__(self)
        self.previous_actions = []
        self.controller = controller

    def execute_action(self, action):
        self.previous_actions.append(action)
        self.controller.execute_action(action)

    def get_id(self):
        return id(self)        
    
    def get_latest_action(self):
        if len(self.previous_actions) > 0:
            return self.previous_actions[-1]
        return None
    
    def set_controller(self, new_controller):
        self.controller = new_controller