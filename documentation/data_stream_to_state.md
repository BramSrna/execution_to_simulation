# Data Stream To State
## Discrete simulation from data streams
Say a discrete simulator has the following three states:
State 0:
- Location sensor: (0, 0)
- Visual sensor: (Up, Right)
- Wheel controller: Right
State 1:
- Location sensor: (1, 0)
- Visual sensor: (Up, Right, Left)
- Wheel controller: Up
State 2:
- Location sensor: (1, 1)
- Visual sensor: (Up, Right, Left, Down)
- Wheel controller: Left

Converted to pure data streams, this would be:
- Location sensor: (0, 0), (1, 0), (1, 1)
- Visual sensor: (Up, Right), (Up, Right, Left), (Up, Right, Left, Down)
- Wheel controller: Right, Up, Left

To map data streams to discrete states, the simulator needs to know what each datastream represents. For example, with the above, the location sensor can be used to ID the state, the visual sensor defines the possible transitions, and the wheel controller is used to define the concrete transitions. 