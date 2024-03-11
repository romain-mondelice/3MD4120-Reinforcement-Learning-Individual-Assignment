import pickle
import os, sys
import time
from monte_carlo_agent import MonteCarloAgent

# Load the agent from the file
with open('../agents/mc-agent-screen.pkl', 'rb') as f:
    loaded_agent = pickle.load(f)

def test_agent(agent, episodes=3):
    total_rewards = 0
    for _ in range(episodes):
        state = agent.env.reset()
        done = False
        while not done:
            # Assuming the agent has a method encode_state to handle the environment's states
            encoded_state = agent.encode_state(state)  
            action = agent.policy[encoded_state]
            state, reward, done, _, info = agent.env.step(action)
            total_rewards += reward

            # Render the game
            os.system("clear")
            sys.stdout.write(agent.env.render())
            time.sleep(0.2)
    
    avg_reward = total_rewards / episodes
    print(f"Average Reward over {episodes} episodes: {avg_reward}")

# Test the loaded agent
test_agent(loaded_agent)