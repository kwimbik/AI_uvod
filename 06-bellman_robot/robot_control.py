import numpy, scipy, networkx # You can use everything from these libraries if you find them usefull.
import scipy.sparse as sparse # Calling scipy.sparse.csc_matrix does not work on Recodex, so call sparse.csc_matrix(...) instead
import scipy.sparse.linalg as linalg # Also, call linalg.spsolve
import numpy as np

"""
    TODO: Improve the strategy controlling the robot.
    A recommended approach is implementing the function RobotControl.precompute_probability_policy.
    You can adopt this file as you like but you have to keep the interface so that your player properly works on recodex; i.e.
        * RobotControl.__init__ is called in for every environment (test).
        * RobotControl.get_command is called to obtain command for movement on a given position.
    Furthermore, get_survivability and get_policy is used by tests in the file probability_test.py.
"""

class RobotControl:
    def __init__(self, environment):
        self.env = environment
        self.survivability,self.policy = self.precompute_probability_policy()

    # Returns a matrix of maximal probabilities of reaching the station from every cell
    def get_survivability(self):
        return self.survivability

    # Returns a matrix of commands for every cell
    def get_policy(self):
        return self.policy

    # Returns command for movement from the current position.
    # This function is called quite a lot of times, so it is recommended to avoid any heavy computation here.
    def get_command(self, current):
        return self.policy[tuple(current)]

    # Place all your precomputation here.
    def precompute_probability_policy(self):
        env = self.env
        safetyMap = env.safety_map
        destination = env.destination
        survivability = numpy.zeros((env.rows, env.columns)) # No probability is computed
        survivability[tuple(destination)] = 1 #initial survivability is zero except destination point
        policy = numpy.zeros((env.rows, env.columns), dtype=int)
        actions = [env.FORWARD,env.EAST, env.BACKWARD, env.WEST]
        actionsProbability = [env.forward_probability, env.right_probability, env.backward_probability, env.left_probability]
        rotation = env.ROTATION

        policyUpdated = True
        next_state_reward = np.zeros(4)
        #policy update
        while policyUpdated:
            policyUpdated = False #we can stop computation once no change in policy is made
            for i in range(1,env.rows-1):
                for j in range(1,env.columns-1):
                        if (i,j) == tuple(destination): continue
                        #for every cell, compute reward function u = as P(moveToNextCell)*R(nextCell)*safety(nextCell)
                        for x, rot in enumerate(rotation):
                            reward = 0
                            for action in actions:
                                nextCell = i + env.DIRECTION[rot[action]][0], j + env.DIRECTION[rot[action]][1]
                                reward += survivability[nextCell] * safetyMap[nextCell]*actionsProbability[action]
                            next_state_reward[x] = reward
                        #calculateing maxium of rewards and choosing policy for that action
                        #if policy is updated, keep iterating
                        bestMove = np.argmax(next_state_reward)
                        if (policy[i,j] != bestMove) : policyUpdated = True
                        policy[i,j] = bestMove
                        survivability[i,j] = next_state_reward[bestMove]
        return survivability, policy