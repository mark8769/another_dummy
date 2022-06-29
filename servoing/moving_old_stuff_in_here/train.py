import visual_servoing_env
import numpy as np

env = visual_servoing_env.ServoingEnvironment()            

#Initialize table with all zeros
Q = np.zeros([env.num_of_states,env.num_of_actions])

# Set learning parameters
lr = .8   
y = .95
num_episodes = 2

#create lists to contain total rewards and steps per episode
#jList = []
rList = []

for i in range(num_episodes):
    print("Beginning episode",i,"...")
    #print(Q)

    #Reset environment and get first new observation
    s = env.reset()
    rAll = 0
    d = False
    j = 0

    #The Q-Table learning algorithm
    while j < 99:
        print("Starting trial",j,"in state",s,"...")
        j+=1
        #Choose an action by greedily (with noise) picking from Q table

        # random noise added to each column element in row "s"
        # then the INDEX of the maximum of those is selected
        a = np.argmax(Q[s,:] + np.random.randn(1,env.num_of_actions)*(1./(i+1)))

        print("Selected action",a)

        # Get new state and reward from environment
        s1,r,d = env.step(a)
        print("Action performed. In state",s1,". reward:",r)

        if (r==1):
            # SUCCESS. update the table and start again.
            print("Goal Achieved!!")

        print("NEW STATE",s1)

        #Update Q-Table with new knowledge
        Q[s,a] = Q[s,a] + lr*(r + y*np.max(Q[s1,:]) - Q[s,a])
        #print(Q)
        rAll += r
        #print("rAll:",rAll)
        s = s1

        # if success or fail, start a new episode
        if d == True: 
            break

    rList.append(rAll)
print("Training complete")
print(Q)
