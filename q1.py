'''
Assignment1
Daniel Bellissimo
500749419
'''
import sys
import random
import time
import numpy
#import matplotlib.pyplot as plt
#import matplotlib.patches as mpatches

class ucb_bandit(object):
    def __init__(self,const):
        self.arms_env = generate_env()
        self.pull_number = [0.0] * 10 #number of times each arm has been pulled
        self.avg_ex_rw = [0.0] * 10 #starting expected value for all arms at 0
        self.avg_rw_t = [] #for evaluating performance at time step t
        self.avg_rw = 0.0 #for evaluating performance
        self.const = const
        self.optimal_a = self.arms_env.index(max(self.arms_env))

    '''(time_step) int -> int (index of arm)
    using UCB formula, selects which action to take
    '''
    def select_action(self,time_step):
        At = []
        for i in range(0,10):
            #calculate the At of every arm i at time_step t and add them all to a list
            action_value = self.avg_ex_rw[i] + (self.const * (numpy.log(time_step)/self.pull_number[i])**0.5)
            At.append(action_value)
        action = At.index(max(At)) #gets action index with highest value -> index of arm
        return action

    '''(arm_index) int -> None
    'pulls' arm at the provided index, increments number of times the arm has been pulled, updates the expected value
    '''
    def execute_action(self,arm_index):
        n = self.pull_number[arm_index] + 1
        self.pull_number[arm_index] = n #increment

        expected_rw = self.avg_ex_rw[arm_index] 
        
        prob = self.arms_env[arm_index]
        rand_num = random.randrange(0,100) #random numbers for this program are between 0 and 100 not 0 and 1
        reward = 0.0
        if rand_num <= prob:
            reward = 1.0
        self.avg_ex_rw[arm_index] = expected_rw + (1/n)*(reward-expected_rw) 
        avg = self.avg_rw + (reward-self.avg_rw)/sum(self.pull_number)
        self.avg_rw = avg
        self.avg_rw_t.append(avg)


    def get_avg_rw(self):
        return self.avg_rw
    def get_avg_rw_t(self):
        return self. avg_rw_t
    def get_pull_num(self):
        return self.pull_number
    def get_avg_ex_rw(self):
        return self.avg_ex_rw
    def get_env(self):
        return self.arms_env
    def get_optimal_actions(self):
        return self.pull_number[self.optimal_a]
    def reset(self):
        self.pull_number = [0.0] * 10
        self.avg_ex_rw = [0.0] * 10
        self.avg_rw_t = [] #for evaluating performance at time step t
        self.avg_rw = 0.0
    def set_c(self,c):
        self.const = c
    def set_env(self,env):
        self.arms_env = env
'''None -> list
Generates a set of 10 random numbers (qk) representing the probability of an arm pull returning a 1.
-Uses time since the epoch as a random seed
'''
def generate_env():
    random.seed(time.time())
    qk = []
    for i in range(0,10):
        a = random.randrange(0,100)
        qk.append(a)
    return qk
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    if len(sys.argv) == 3:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        if int(arg1) and float(arg2):
            time_range = int(arg1)
            c = float(arg2)
        else:
            time_range = 10000
            c = 0.05#setting c value to 0.5
    else:
        time_range = 10000
        c = 0.05#setting c value to 0.5
    bandit = ucb_bandit(c) 
    for t in range(1,time_range+1):
        action = bandit.select_action(t)
        bandit.execute_action(action)
        prev = 0
        if t % 100 == 0:
            optimal = bandit.get_optimal_actions()
            avg = bandit.get_avg_rw()
            print("t={}\nOptimal Actions: {}\nAverage Reward: {}\n\n" .format(t,optimal,avg))
            prev = avg
    avg1 = bandit.get_avg_rw_t()
    print("Environment Probabilities: {}" .format(bandit.get_env()))
    
    #plt.plot(range(1,time_range+1),avg1)
    #plt.plot(range(1,5001),avg2, color="green")
    #plt.plot(range(1,1001),avg3, color="red")
    #plt.plot(range(1,5001),avg4, color="orange")
    #plt.xlabel("Timesteps")
    #plt.ylabel("Average Reward")
    #plt.show()