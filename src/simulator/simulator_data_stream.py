class SimulatorDataStream(object):
    def __init__(self, simulator):
        self.simulator = simulator
        self.simulator.register_data_stream(self)