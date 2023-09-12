class SimulatorState(object):
    def __init__(self, state_key_info):
        self.state_key_info = state_key_info

        self.is_start_state = False
        self.is_end_state = False
        self.transition_tree = {}

    def get_state_key_info(self):
        return self.state_key_info

    def add_possible_transition_name_list(self, possible_transition_list):
        for transition_name in possible_transition_list:
            if transition_name not in self.transition_tree:
                self.transition_tree[transition_name] = None

    def add_possible_transition_end_state(self, transition_name, end_state):
        self.transition_tree[transition_name] = end_state

    def get_transition_tree(self):
        return self.transition_tree

    def get_possible_transition_names(self):
        possible_actions = list(self.transition_tree.keys())
        return possible_actions
    
    def get_is_start_state(self):
        return self.is_start_state
    
    def set_is_start_state(self, new_is_start_state_value):
        self.is_start_state = new_is_start_state_value

    def get_is_end_state(self):
        return self.is_end_state
    
    def set_is_end_state(self, new_is_end_state_value):
        self.is_end_state = new_is_end_state_value

    def is_complete(self):
        for transition_name, end_value in self.transition_tree.items():
            if end_value is None:
                return False
        return True
    
    def __str__(self):
        info = {
            "STATE_KEY_INFO": self.state_key_info,
            "IS_START_STATE": self.is_start_state,
            "IS_END_STATE": self.is_end_state,
            "POSSIBLE_TRANSITION_NAMES": self.get_possible_transition_names()
        }
        return str(info)