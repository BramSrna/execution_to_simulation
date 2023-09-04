# execution_to_simulation
A proof of concept for generating a simulator using data retrieved during program execution


There are three parts to the project:
- Execution to simulation
- Simulator core (scaling, state prediction, etc)
- Task improvement using simulator

What would I define version 1.0 as?
- Simulator hyperparameters defined using metadata (YAML?) (ex. When is simulator "done"? What other simulators is it compatable with?)
- Simulator can be entirely initialized using sensor data, using synthetic data, or a combination
- Datastreams can be connected to simulator to provide new data read from production (ex. cameras, GPS)
- New synthetic data can be added to the simulator using datastreams (chain simulators together?)
- Simulator supports both discrete state simulation as well as continuous simulation (state vs. stateless)
- Support state prediction using ML (i.e. I don't know what the new state would be after the given action, but here's a best guess). This can be done JIT at read-time.
- Support multi-client simulation (i.e. multiple "users" (bots) using a simulator simultaneously)
- Can combine compatable simulators or break up simulators into seperate components
- Support task execution and iteration against the simulator (ML library)
- Integrate and support proof of simulation for iteration proof and federated simulator creation
- Support simulator test cases for proof of simulation
- Simulation can be visualized
- Simulator can be fast-forwarded, rewound, and paused. Alternatively, single states can be simulated.

What is out-of-scope for the simulator?
- Starts with monitoring initial execution for simulator creation
- Ends with task optimization
- Anything that pertains to only one simulator instance
- Avoid UI outside of the simulation visualizer. Visualizer shall be read-only

Sample simulator life cycle:
- Define initial simulator hyper parameters and bounds
- Initialize proof of simulation chain
- Define initial datastreams for task monitoring
- Allow task to run a few times to build up initial simulator
- Add some synthetic data to round out simulator corner cases
- Define task optimization test cases
- Iterate on simulator and task
- User monitors optimization using visualizer
- User provides new synthetic data and manual task manipulations as needed
