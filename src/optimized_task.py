import numpy as np

class OptimizedTask(object):
    def __init__(self, simulator, alpha=0.1, random_factor=0.25):
        super().__init__()
        self.simulator = simulator
        self.alpha = alpha
        self.random_factor = random_factor

        self.rewards = {}
        self.state_history = []

    def optimize(self):
        for _ in range(100):
            step_count = 0
            curr_state = self.simulator.get_start_state()
            end_state = self.simulator.get_end_state()
            while (curr_state != end_state) and (step_count < 1000):
                action = self.choose_action(curr_state, curr_state.get_possible_transition_names()) # choose an action (explore or exploit)
                curr_state = curr_state.get_transition_tree()[action]
                if curr_state == end_state:
                    reward = 0
                else:
                    reward = -1
                self.state_history.append((curr_state, reward))
                step_count += 1

            self.learn() # robot should learn after every episode

    def choose_action(self, curr_state, allowed_moves):
        max_reward = -10e15
        next_move = None
        if np.random.random() < self.random_factor:
            # if random number below random factor, choose random action
            next_move = np.random.choice(allowed_moves)
        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            next_move = self.get_optimum_action_for_state(curr_state)

        return next_move

    def learn(self):
        target = 0

        for prev, reward in reversed(self.state_history):
            self.rewards[self.state_to_str(prev)] = self.get_reward(prev) + self.alpha * (target - self.get_reward(prev))
            target += reward

        self.state_history = []

        self.random_factor -= 10e-5 # decrease random factor each episode of play

    def state_to_str(self, state):
        return str(state)

    def get_reward(self, state):
        key = self.state_to_str(state)
        if key not in self.rewards:
            self.rewards[key] = np.random.uniform(low=1.0, high=0.1)
        return self.rewards[key]

    def get_optimum_action_for_state(self, state):
        max_reward = -10e15
        next_move = None

        allowed_moves = state.get_possible_transition_names()

        for action in allowed_moves:
            new_state = state.get_transition_tree()[action]
            if self.get_reward(new_state) >= max_reward:
                next_move = action
                max_reward = self.get_reward(new_state)

        return next_move

    def get_optimum_state_array(self):
        state_array = []

        step_count = 0
        curr_state = self.simulator.get_start_state()
        state_array.append(curr_state)
        while (curr_state != self.simulator.get_end_state()) and (step_count < 1000):
            action = self.get_optimum_action_for_state(curr_state)
            curr_state = curr_state.get_transition_tree()[action]
            state_array.append(curr_state)
            step_count += 1

        return state_array
    
    def decide(self, location, possible_directions):
        state = self.simulator.state_info_to_state(location)
        return self.get_optimum_action_for_state(state)
