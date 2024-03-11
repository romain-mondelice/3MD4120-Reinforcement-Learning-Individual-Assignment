from collections import defaultdict
import numpy as np

class OffPolicyMonteCarloAgent:
    def __init__(self, env, gamma=0.9, epsilon=0.1):
        self.env = env
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = defaultdict(self.zero_action_value)
        self.C = defaultdict(self.zero_action_value)
        self.target_policy = defaultdict(int)

    def zero_action_value(self):
        """Returns a default value for actions, a zero array with the size of the action space."""
        return np.zeros(self.env.action_space.n)
        
    def generate_episode(self, policy):
        episode = []
        state = self.env.reset()
        done = False
        while not done:
            # Convert state to a string representation.
            str_state = str(state)

            if str_state in policy:
                action_probs = policy[str_state]
                action = np.random.choice(np.arange(len(action_probs)), p=action_probs)
            else:
                # Fallback if the state is not in the policy, use uniform random selection
                action = self.env.action_space.sample()

            next_state, reward, done, _, info = self.env.step(action)
            episode.append((str_state, action, reward))
            state = next_state
        return episode
    
    def get_probs(self, Q_s, epsilon, nA):
        """Obtains the policy for a given state"""
        policy_s = np.ones(nA) * epsilon / nA
        best_a = np.argmax(Q_s)
        policy_s[best_a] = 1 - epsilon + (epsilon / nA)
        return policy_s
    
    def update_Q(self, episode):
        G = 0.0
        W = 1.0
        for t in reversed(range(len(episode))):
            state, action, reward = episode[t]
            G = self.gamma * G + reward
            self.C[state][action] += W
            self.Q[state][action] += (W / self.C[state][action]) * (G - self.Q[state][action])
            self.target_policy[state] = np.argmax(self.Q[state])
            
            if action != self.target_policy[state]:
                break
            W = W * 1./self.get_probs(self.Q[state], self.epsilon, self.env.action_space.n)[action]
            
    def train(self, num_episodes):
        for i_episode in range(1, num_episodes + 1):
            episode = self.generate_episode(policy=self.create_behavior_policy(self.Q))
            self.update_Q(episode)
    
    def create_behavior_policy(self, Q):
        """Creates a behavior policy using ε-greedy approach based on Q."""
        behavior_policy = {}
        for state, actions in Q.items():
            behavior_policy[state] = self.get_probs(actions, self.epsilon, self.env.action_space.n)
        return behavior_policy