import logging
import unittest
import json
import os

from src.simulator.simulator import Simulator
    

class TestSimulatorConfiguration(unittest.TestCase):
    def test_simulator_will_use_default_config_file_if_none_given(self):
        test_sim = Simulator()
        expected_config = json.load(
            open(os.path.join(os.path.dirname(__file__), "../src/simulator/default_simulator_config.json"))
        )
        actual_config = test_sim.get_config()
        self.assertEqual(expected_config, actual_config)

    def test_extra_simulator_configuration_can_be_specified_using_a_dictionary(self):
        expected_config = json.load(
            open(os.path.join(os.path.dirname(__file__), "../src/simulator/default_simulator_config.json"))
        )
        expected_config["ready_for_use_threshold_percentage"] = expected_config["ready_for_use_threshold_percentage"] - 1
        test_sim = Simulator(additional_config_dict=expected_config)
        actual_config = test_sim.get_config()
        self.assertEqual(expected_config, actual_config)

    def test_extra_simulator_configuration_can_be_specified_using_a_file(self):
        expected_config = json.load(
            open(os.path.join(os.path.dirname(__file__), "../src/simulator/default_simulator_config.json"))
        )
        expected_config["ready_for_use_threshold_percentage"] = expected_config["ready_for_use_threshold_percentage"] - 1
        file_path = os.path.join(os.getcwd(), "test.txt")
        with open(file_path, 'w') as json_file:
            json.dump(expected_config, json_file)
        test_sim = Simulator(additional_config_path=file_path)
        actual_config = test_sim.get_config()
        self.assertEqual(expected_config, actual_config)
        os.remove(file_path)



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()