import random
import matplotlib.pyplot as plt
import numpy as np

from scipy.spatial import distance_matrix

class Agent:
    def __init__(self, x,y, infected, infection_timer_max, resistance, resistance_factor):
        '''
        x: float; x position of the agent
        y: float; y position of the agent
        infected: bool; whether the agent will be initialized in the infected state
        '''
        self.x = x
        self.y = y
        self.infected = infected
        self.infection_timer_max = infection_timer_max
        self.resistance = resistance
        self.resistance_factor = resistance_factor
        self.infection_timer = 0
        if self.infected == True:
            self.infection_timer = self.infection_timer_max

    def move(self, meanstep, L):
        '''
        meanstep: float; the mean step an agent take in a random direction
        L: float; the length and width of the simulation box. Used to prevent the agent from moving outside
        The agent moves in a random x and y direction with an average step size of meanstep
        If the agent leaves the simulation box, its position will be moved to the edge of the box
        '''
        self.x+=meanstep*np.random.randn()
        self.y+=meanstep*np.random.randn()

        # don't let agents leave the box
        if self.x>L:
            self.x=L
        if self.x<0:
            self.x=0
        if self.y>L:
            self.y=L
        if self.y<0:
            self.y=0
    
    def expose(self):
        '''
        Function to model disease spread
        '''
        infection_chance = (1.0 - self.resistance)
        if random.random() < infection_chance:
            self.infected = True
            self.infection_timer = self.infection_timer_max

    def is_infected(self):
        '''
        Function to model disease spread
        '''
        if self.infected == True:
            return True
        else:
            return False

class World:
    def __init__(self, L, infection_radius=5.0):
        """
        L: float; the length and width of the simulation box

        The World class contains info of the simulation box length, the list of agents 
        in the simulation, functions for creating, and moving agents, as well as utility 
        functions for visualization.
        """
        self.L = L 
        self.agents = []  # list of agents
        self.infection_radius = infection_radius

    def create_agents(self, N, infected, infection_timer_max=20, resistance=0.2, resistance_factor=1.2):
        '''
        N: int; number of agents to randomly place
        is_infected: boolean; True means an Agent is infected, False means uninfected
        Randomly place N agents in the simulation box. They are infected or uninfected
        depending on the boolean parameter is_infected
        '''
        agents = self.agents + [Agent(self.L*random.random(),self.L*random.random(), infected, infection_timer_max, resistance, resistance_factor) for i in range(N)]
        self.agents = agents

    def move_agents(self, meanstep):
        '''
        meanstep: float; the mean step an agent take in a random direction
        Move every agent with randomly with an average step size of meanstep
        '''
        for agent in self.agents:
            agent.move(meanstep, self.L)

    def find_nearby_agents(self, agent_list):
        '''
        Takes in a list of agent indices (agent_list) and returns a list of
        agent indices that are close to the agents in agent_list
        An agent is "close" to another agent when they are within
        a distance of self.infection_radius (you will implement this attribute
        in Part 1B.
        '''
        positions = [[agent.x, agent.y] for agent in self.agents]
        positions = np.array(positions)
        distanceMatrix = distance_matrix(positions,positions)
        closeagents = []
        for i in range(len(self.agents)):
            closemask = distanceMatrix[i]<self.infection_radius
            closemask[i]=0
            inds = np.nonzero(closemask)
            closeagents.append(inds[0])

        return_list = []
        for agent_id in agent_list:
            return_list.append(closeagents[agent_id])

        return list(set(j for sub in return_list for j in sub))


    def init_display(self):        
        '''
        Utility function for visualizing the state of the simulation
        '''
        f, a = plt.subplots()
        sc_state_0 = a.scatter([], [])
        sc_state_1 = a.scatter([], [], c='r')
        plt.xlim([0, self.L])
        plt.ylim([0, self.L])
        a.set_aspect('equal', 'box')
        plt.draw()
  
        # save handles so they can be updated later
        self.ax = a
        self.fig = f
        self.sc = sc_state_0,sc_state_1;
    '''
    def plot_positions(self):

        xs = [agent.x for agent in self.agents if not agent.infected];
        ys = [agent.y for agent in self.agents if not agent.infected];
        self.sc[0].set_offsets(np.c_[xs, ys]) # updates positions of agents with infected=False

        xs = [agent.x for agent in self.agents if agent.infected];
        ys = [agent.y for agent in self.agents if agent.infected];
        self.sc[1].set_offsets(np.c_[xs, ys]) # updates positions of agents with infected=True

        self.fig.canvas.draw_idle()
        plt.pause(.1)
    '''
    def update_infection_timers(self):
        '''
        Function to model disease spread
        '''
        for agent in self.agents:
            if agent.infected == True:
                agent.infection_timer -= 1
                if agent.infection_timer < 0:
                    agent.infected = False
                    agent.resistance += agent.resistance_factor

    def expose_agents(self, agent_list):
        '''
        Function to model disease spread
        '''
        for index in agent_list:
            agent = self.agents[index]
            agent.expose()

    def update_exposure(self):
        '''
        Function to model disease spread
        '''
        for i, agent in enumerate(self.agents):
            if agent.infected:
                agent_index = i
                nearby_agents = self.find_nearby_agents([agent_index])
                self.expose_agents(nearby_agents)

    def get_number_infected(self):
        '''
        Function to model disease spread
        '''
        infection_counter = 0
        for agent in self.agents:
            if agent.infected == True:
                infection_counter += 1
        return infection_counter

def main():
    '''
    This function runs the simulation. Once you've added the functions
    necessary to model disease spread, edit this main function to include
    those functions so that you can run the SIR model.

    At the end of this function, the script will plot out a graph of
    infected individuals as a function of simulation steps.
    '''
    total_steps = 500

    myworld = World(L=100)
    #myworld.init_display()

    myworld.create_agents(199, infected=False)
    myworld.create_agents(1, infected=True)

    #myworld.plot_positions()
    number_infected = np.zeros(total_steps)

    for i in range(total_steps):
        myworld.move_agents(1)
        #myworld.plot_positions()
        myworld.update_infection_timers()
        number_infected[i] = myworld.get_number_infected()
        myworld.update_exposure()

    return number_infected


'''
    # data analysis
    f2, a2 = plt.subplots()
    a2.plot(number_infected)
    a2.set_title("Number Infected vs Time")
    a2.set_xlabel("Time (steps)")
    a2.set_ylabel("Number infected")
    plt.show()
'''

if __name__ == "__main__":
    main()

