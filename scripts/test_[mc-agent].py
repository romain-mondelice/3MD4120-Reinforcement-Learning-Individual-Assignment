import pickle
import os, sys
import time
from monte_carlo_agent import OffPolicyMonteCarloAgent

# Load the agent from the file
with open('../agents/mc-agent.pkl', 'rb') as f:
    loaded_agent = pickle.load(f)

def test_agent(agent, episodes=3):
    total_rewards = 0
    for _ in range(episodes):
        state = agent.env.reset()
        done = False
        while not done:
            # Convert state to a string representation for consistency.
            str_state = str(state)
            
            # Use the target_policy for action selection if this state has been seen.
            # Otherwise, select a random action.
            if str_state in agent.target_policy:
                action = agent.target_policy[str_state]
            else:
                action = agent.env.action_space.sample()

            state, reward, done, _, info = agent.env.step(action)
            total_rewards += reward

            # Render the game
            os.system("clear")
            sys.stdout.write(agent.env.render())
            time.sleep(0.1) # FPS
            
    print("Total reward: ", total_rewards)
    avg_reward = total_rewards / episodes
    print(f"Average Reward over {episodes} episodes: {avg_reward}")

# Test the loaded agent
test_agent(loaded_agent)