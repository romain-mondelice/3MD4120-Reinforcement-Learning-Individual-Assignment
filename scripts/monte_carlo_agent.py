from collections import defaultdict

class MonteCarloAgent:
    def __init__(self, env, gamma=0.9):
        self.env = env
        self.gamma = gamma  # discount factor
        self.value_table = defaultdict(float)  # state value table
        self.returns = defaultdict(list)  # store returns for each state
        self.policy = defaultdict(self.default_policy_action)
    
    def default_policy_action(self):
        return self.env.action_space.sample()

    def encode_state(self, state):
        return str(state)

    def generate_episode(self):
        episode = []
        state = self.env.reset()
        done = False
        while not done:
            encoded_state = self.encode_state(state)
            action = self.policy[encoded_state]
            next_state, reward, done, _, info = self.env.step(action)
            episode.append((encoded_state, action, reward))
            state = next_state
        return episode
    
    def update_value_function(self, episode):
        G = 0
        for encoded_state, action, reward in reversed(episode):
            G = self.gamma * G + reward
            if not encoded_state in [x[0] for x in episode[:-1]]:
                self.returns[encoded_state].append(G)
                self.value_table[encoded_state] = np.mean(self.returns[encoded_state])
    
    def improve_policy(self):
        for encoded_state in self.value_table.keys():
            self.policy[encoded_state] = self.env.action_space.sample()