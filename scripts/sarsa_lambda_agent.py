from collections import defaultdict
import numpy as np

class SarsaLambdaAgent:
    def __init__(self, env, gamma=0.9, lambda_=0.9, epsilon=0.1, alpha=0.5):
        self.env = env
        self.gamma = gamma
        self.lambda_ = lambda_
        self.epsilon = epsilon
        self.alpha = alpha
        self.Q = defaultdict(self.zero_action_value)
        self.E = defaultdict(self.zero_action_value)

    def zero_action_value(self):
        return np.zeros(self.env.action_space.n)

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return self.env.action_space.sample()
        else:
            return np.argmax(self.Q[state])

    def update(self, state, action, reward, next_state, next_action, done):
        delta = reward + self.gamma * self.Q[next_state][next_action] * (not done) - self.Q[state][action]
        self.E[state][action] += 1  # Increment eligibility trace

        for s, values in self.Q.items():
            for a in range(len(values)):
                self.Q[s][a] += self.alpha * delta * self.E[s][a]
                self.E[s][a] *= self.gamma * self.lambda_

    def reset_eligibility_traces(self):
        for s in self.E:
            for a in range(len(self.E[s])):
                self.E[s][a] = 0

    def train(self, num_episodes):
        for i_episode in range(num_episodes):
            state = self.env.reset()
            action = self.choose_action(str(state))
            self.reset_eligibility_traces()
            done = False

            while not done:
                next_state, reward, done, _, _ = self.env.step(action)
                next_action = self.choose_action(str(next_state))
                self.update(str(state), action, reward, str(next_state), next_action, done)
                state = next_state
                action = next_action