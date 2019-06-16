'''
Assignment1
Daniel Bellissimo
500749419
'''
import random
import time
#import matplotlib.pyplot as plt
import sys
class linear_algorithm(object):
    def __init__(self,alpha,k,beta):
        self.arms_env = generate_q2_env(k)
        self.arms_prob =   [1.0/k] * k #give every action an equal probability of selection at the start
        self.arms_num = k
        self.pull_number = 0.0
        self.alpha = alpha
        self.beta = beta
        self.avg_rw_t = [] #for evaluating performance at time step t
        self.total_rewards = [] #for evaluating performance
        self.avg_rw = 0.0 #for evaluating performance
        self.optimal_pull_num = 0

    def select_action(self):
        #randomly selects an action
        random.seed(time.time())
        low_bound = 0
        upper_bound = 0
        rand_num = random.randrange(0,100)/100.0
        for i in range(0,self.arms_num):
            upper_bound += self.arms_prob[i]
            
            if low_bound < rand_num and rand_num <= upper_bound:
                return i
            low_bound += self.arms_prob[i]
        return 0
        
        #action = self.arms_prob.index(max(self.arms_prob)) #gets action index with highest value -> index of arm
        #return action
    def execute_and_update(self,action):
        if action == self.arms_env.index(max(self.arms_env)): #Performance metric
            self.optimal_pull_num += 1
        num = random.randrange(0,100)/100.0 #Take random number
        signal = 0
        if num <= self.arms_env[action]:
            signal = 1
            if  self.arms_prob[action] < 1: #if random number is within the probability range (success), only updates if pt < 1
                self.arms_prob[action] = self.arms_prob[action] + self.alpha * (1-self.arms_prob[action])
                
                for j in range(0,len(self.arms_env)):
                    if j != action:
                        self.arms_prob[j] = (1-self.alpha) * self.arms_prob[j]
                    
                
        else:
            if self.arms_prob[action] > 0: #else if (fail)
                self.arms_prob[action] = (1-self.beta) * self.arms_prob[action]
                for j in range(0,len(self.arms_env)):
                    if j != action:
                        self.arms_prob[j] = self.beta/(self.arms_num-1) + (1-self.beta) * self.arms_prob[j]
        
        
        ##Performance evaluation metrics
        self.pull_number += 1
        self.total_rewards.append(signal)
        self.avg_rw = sum(self.total_rewards)/self.pull_number
        self.avg_rw_t.append(self.avg_rw)
        

    def get_arms_prob(self):
        return self.arms_prob
    def get_env(self):
        return self.arms_env
    def set_env(self,env):
        self.arms_env = env
    def get_avg_rw(self):
        return self.avg_rw
    def get_avg_rw_t(self):
        return self.avg_rw_t
    def get_optimal(self):
        return self.optimal_pull_num
    def get_k(self):
        return self.arms_num
    
'''
Generates an array of k numbers which sum to 1
'''
def generate_q2_env(k):
    random.seed(time.time())
    qk = []
    for i in range(0,k):
        a = random.randrange(0,100)/100.0
        qk.append(a)
    return qk
##----------------------------------------------------------------------------------------------------------------------------------------------------------##
if __name__ == '__main__':
    if len(sys.argv) == 6:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
        arg4 = sys.argv[4]
        arg5 = sys.argv[5]

        if int(arg1) and float(arg2) and float(arg3) and float(arg4) and float(arg5):
            time_range = int(arg1)
            alpha1 = float(arg2)
            beta1 = float(arg3)
            alpha2 = float(arg4)
            beta2 = float(arg5)
        else: #standard config
            time_range = 10000
            alpha1 = 0.1
            beta1 = 0.1
            alpha2 = 0.1
            beta2 = 0
    else: #standard config
        time_range = 10000
        alpha1 = 0.1#setting c value to 0.5
        beta1 = 0.1    
        alpha2 = 0.1
        beta2 = 0
    #LRP
    linear_reward_action = linear_algorithm(alpha1,10,beta1)
    for t in range(1,time_range+1):
        action = linear_reward_action.select_action()
        linear_reward_action.execute_and_update(action)
        if t % 100 == 0:
            print("t={}\nOptimal Pull Number: {}\nAverage Reward: {}\n" .format(t,linear_reward_action.get_optimal(),linear_reward_action.get_avg_rw()))

    #LRI
    linear_reward_inaction = linear_algorithm(alpha2,10,beta2)
    linear_reward_inaction.set_env(linear_reward_action.get_env())
    for t in range(1,time_range+1):
        action = linear_reward_inaction.select_action()
        linear_reward_inaction.execute_and_update(action)
        if t % 100 == 0:
            print("t={}\nOptimal Pull Number: {}\nAverage Reward: {}\n" .format(t,linear_reward_inaction.get_optimal(),linear_reward_inaction.get_avg_rw()))

    print("Environment for LRP: {}" .format(linear_reward_action.get_env()))
    print("Number of Optimal Pulls: {}\nAverage Reward: {}\n" .format(linear_reward_action.get_optimal(),linear_reward_action.get_avg_rw()))
    print("Environment for LRI: {}" .format(linear_reward_inaction.get_env()))
    print("Number of Optimal Pulls: {}\nAverage Reward: {}\n" .format(linear_reward_inaction.get_optimal(),linear_reward_inaction.get_avg_rw()))


    #plt.plot(range(1,time_range+1),linear_reward_action.get_avg_rw_t()) #LRP
    #plt.plot(range(1,time_range+1),linear_reward_inaction.get_avg_rw_t(),color='green') #LRI
    #plt.xlabel("Timesteps")
    #plt.ylabel("Average Reward")
    #plt.show()
