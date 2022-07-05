import servoingEnvironment
import numpy as np
import cv2 as cv
from videoGet import VideoGet
from datetime import datetime

env = servoingEnvironment.ServoingEnvironment()            

#Initialize Q-table with all zeros
Q = np.zeros([env.numStates,env.numActions])

# Set learning parameters
learningRate = .8   
gamma = .95 # Gamma setting for updating the Q-table  
numEpisodes = 40

#create lists to contain total rewards and steps per episode
rList = []

# Creates VideoCapture thread
# videoGetter = VideoGet()
# videoGetter.start()

def trainerFunc():    
    for i in range(numEpisodes):
        stepNumber = 0

        print("Beginning episode",i,"...")
        currentState = env.reset() # Defines initial state of the system
        rAll = 0 # Quantifies rewards over time
        completeStatus = False # Defines if episode succeeded or failed

        # The Q-Table learning algorithm
        while stepNumber < 99: # Max amount of steps allowed before episode times out and fails

            print("Starting trial",stepNumber,"in state",currentState,"...")
            stepNumber += 1
            #Choose an action by greedily (with noise) picking from Q table

            # random noise added to each column element in row "s"
            # then the INDEX of the maximum of those is selected
            # np.argmax(Q[s,:] -- Searches table for action that is most likely to succeed given the state
            # np.random.randn(1,env.numActions)*(1./(i+1))) -- creates random noise in action selection that becomes less random as episodes continue
            # Selects an action to take
            action = np.argmax(Q[currentState,:] + np.random.randn(1,env.numActions)*(1./(i+1)))
            
            # Displays selected action
            print("Performing Action:",action)

            # Get new state and reward from environment
            # Takes new step using the action 'a', gets new state, reward (1 or 0), and whether or not the episode succeeded (True/False)
            # newState,reward,completeStatus = asyncio.run(asyncio.gather(env.step(action)))
            newState,reward,completeStatus = env.step(action)
            if (reward==1):
                # SUCCESS. update the table and start again.
                print(f"New State: {newState}. Reward: {reward}, Goal Achieved!!\n")
            else:
                print(f"New State: {newState}. Reward: {reward}\n")

            #Update Q-Table with new knowledge
            Q[currentState,action] = Q[currentState,action] + learningRate*(reward + gamma*np.max(Q[newState,:]) - Q[currentState,action])
            rAll += reward
            currentState = newState

            # if success or fail, start a new episode
            if completeStatus == True:
                break

        rList.append(rAll)

    # Rotates the Q table 90 degrees, rounds values to fourth decimal, and prints table
    print(np.round(np.rot90(Q), decimals=4))
    
# def write_to_file():
    
#     current_time = datetime.now()
#     current_time = current_time.strftime("%H_%M_%S")
#     current_time = current_time + ".txt"
#     file_string = current_time
#     f = open(file_string, "w")
    
#     for i in range (len(Q)):
#         for j in range (len(Q[0])):
        
#             if j == len(Q[0] - 1):
#                 f.write(Q[i][j]) + "\n"
#             else:
#                 f.write(Q[i][j]) + " "

# def read_from_file(some_file):
    
#     f = open(some_file, "r")
    
#     # will put each row in a list, each row would be another list
#     read_lines = f.readlines()
    
#     for i in range (len(Q)):
#         # splits list at space
#         read_lines([i]).split()
#         for j in range (len(Q[0])):
            
#             Q[i][j] = read_lines[i][j]
        
def main():
    trainerFunc()
    print(Q)
    
main()

