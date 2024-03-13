import pickle
import os, sys
import time
from sarsa_lambda_agent import SarsaLambdaAgent

# Load the agent from the file
with open('../agents/sarsa-agent.pkl', 'rb') as f:
    loaded_agent = pickle.load(f)


def test_sarsa_lambda_agent(agent):
    state = agent.env.reset()
    done = False
    while not done:
        action = agent.choose_action(str(state))  # Directly choose action from agent's policy
        
        next_state, reward, done, _, info = agent.env.step(action)
        state = next_state  # Update the state
        
        # Render the game
        os.system("clear")
        sys.stdout.write(agent.env.render())
        time.sleep(0.1) # FPS

# Test the loaded agent
test_sarsa_lambda_agent(loaded_agent)