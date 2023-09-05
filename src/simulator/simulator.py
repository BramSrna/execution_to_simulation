import os
import json

from sklearn.tree import DecisionTreeClassifier
from tensorflow import keras
from keras import models, layers
import numpy as np
from src.simulator.simulator_state import SimulatorState

class Simulator(object):
    def __init__(self, additional_config_path = None, additional_config_dict = None):
        self.known_states = []
        self.all_possible_actions = []
        self.previous_predictions = {}
        self.action_predictor_model = None
        self.state_transition_predictor_model = None
        self.end_state = None

        self.config = json.load(
            open(os.path.join(os.path.dirname(__file__), "./default_simulator_config.json"))
        )
        additional_config = {}
        if additional_config_path is not None:
            additional_config = json.load(
                open(os.path.join(os.path.dirname(__file__), additional_config_path))
            )

        for key, value in additional_config.items():
            self.config[key] = value

        if additional_config_dict is not None:
            for key, value in additional_config_dict.items():
                self.config[key] = value

        self.ready_for_use_threshold_percentage = self.config["ready_for_use_threshold_percentage"]

        self._reset_models()

    def export_configuration(self):
        return self.config

    def add_state_info(self, state_key_info, possible_transition_list, is_start_state, is_end_state):
        state = self.state_info_to_state(state_key_info)
        state.add_possible_transition_name_list(possible_transition_list)
        if is_start_state:
            for known_state in self.known_states:
                known_state.set_is_start_state(False)
            state.set_is_start_state(True)
        if is_end_state:
            for known_state in self.known_states:
                known_state.set_is_end_state(False)
            state.set_is_end_state(True)
        self._reset_models()

    def add_transition_info(self, start_state_key_info, transition_name, end_state_key_info):
        start_state = self.state_info_to_state(start_state_key_info)
        end_state = self.state_info_to_state(end_state_key_info)
        start_state.add_possible_transition_end_state(transition_name, end_state)
        self._reset_models()

    def get_start_state(self):
        for state in self.known_states:
            if state.get_is_start_state():
                return state
        return None

    def get_end_state(self):
        for state in self.known_states:
            if state.get_is_end_state():
                return state
        return None

    def get_state_after_action(self, start_state_key_info, transition_name):
        start_state = self.state_info_to_state(start_state_key_info)
        if start_state is None:
            return None
        
        new_state = start_state
        transition_tree = start_state.get_transition_tree()
        if transition_name in transition_tree:
            new_state = transition_tree[transition_name]
        return new_state

    def is_ready_for_use(self):
        if len(self.known_states) == 0:
            return False

        unknown_transitions = 0
        total_transitions = 0
        for state in self.known_states:
            for _, new_state in state.get_transition_tree().items():
                if new_state is None:
                    unknown_transitions += 1
            total_transitions += 1
        unknown_percentage = float(unknown_transitions) / float(total_transitions)
        return unknown_percentage <= (100 - self.ready_for_use_threshold_percentage / 100.0)
    
    def get_uncomplete_states(self):
        uncomplete_states = []
        for state in self.known_states:
            if not state.is_complete():
                uncomplete_states.append(state)
        return uncomplete_states

    def state_info_to_state(self, state_info):
        for state in self.known_states:
            if state.get_state_key_info() == state_info:
                return state
        new_state = SimulatorState(state_info)
        self.known_states.append(new_state)
        return new_state

    def _get_all_known_states(self):
        ret_arr = []
        for state in self.known_states:
            ret_arr.append(state)
        return ret_arr

    def _construct_state_prediction(self, state_info):
        if str(state_info) in self.previous_predictions:
            return self.previous_predictions[str(state_info)]

        predicted_state = SimulatorState(state_info)

        if self.action_predictor_model is None:
            self.train_action_predictor_model()

        actions = self.action_model_array_to_method_array(self.action_predictor_model.predict([state_info])[0])
        predicted_state.add_possible_action_info(actions)

        if self.state_transition_predictor_model is None:
            self.train_state_transition_predictor_model()

        for action in actions:
            predict_input = state_info + self.action_method_array_to_model_array([action])
            new_state_info = self.state_transition_predictor_model.predict([predict_input])
            predicted_state.add_state_transition_info(action, SimulatorState(new_state_info))

        self.previous_predictions[str(state_info)] = predicted_state
        return predicted_state

    def _train_action_predictor_model(self):
        training_data = []
        training_targets = []

        for state in self.known_states:
            state_info = state.get_state_info()
            training_data.append(state_info)

            curr_possible_actions = state.get_possible_actions()
            training_targets.append(self.action_method_array_to_model_array(curr_possible_actions))

        self.action_predictor_model = DecisionTreeClassifier()
        self.action_predictor_model = self.action_predictor_model.fit(training_data, training_targets)

    def _train_state_transition_predictor_model(self):
        # https://towardsdatascience.com/deep-learning-with-python-neural-networks-complete-tutorial-6b53c0b06af0
        base_input_size = len(self.known_states[0].get_state_info()) + len(self.all_possible_actions)
        output_size = len(self.known_states[0].get_state_info())

        # Define the model
        self.state_transition_predictor_model = models.Sequential(name="ActionPredictorModel", layers=[
            layers.Dense(name="h1", input_dim=base_input_size, units=int(round((base_input_size + 1) / 2)), activation='relu'),
            layers.Dropout(name="drop1", rate=0.2),

            layers.Dense(name="h2", units=int(round((base_input_size + 1) / 4)), activation='relu'),
            layers.Dropout(name="drop2", rate=0.2),

            layers.Dense(name="output", units=output_size, activation='sigmoid')
        ])
        self.state_transition_predictor_model.summary()

        # Compile the model
        self.state_transition_predictor_model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['accuracy'])

        # Prepare the data
        training_data = []
        training_targets = []

        for state in self.known_states:
            state_info = state.get_state_info()
            transition_tree = state.get_transition_tree()
            for action, new_state in transition_tree.items():
                if new_state is not None:
                    training_data.append(state_info + self.action_method_array_to_model_array([str(action)]))
                    training_targets.append(new_state.get_state_info())

        # Train the model
        self.state_transition_predictor_model.fit(
            x=np.array(training_data),
            y=np.array(training_targets),
            batch_size=32,
            epochs=100,
            shuffle=True,
            validation_split=0.3
        )

    def _get_possible_actions_for_state(self, state_info):
        saved_state = self.state_info_to_state(state_info)
        if saved_state is not None:
            return saved_state.get_possible_actions()
        else:
            return None

    def _action_model_array_to_method_array(self, model_array):
        method_array = []
        for i in range(len(model_array)):
            if model_array[i] == 1:
                method_array.append(self.all_possible_actions[i])
        return method_array

    def _reset_models(self):
        self.previous_predictions = {}
        self.action_predictor_model = None
        self.state_transition_predictor_model = None