from flappybirdtask import FlappyBirdTask
from flappybirdenv import FlappyBirdEnv
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer

av_table = ActionValueTable(40000,3)
av_table.initialize(0.)

learner = Q(0.5, 0.0)
learner._setExplorer(EpsilonGreedyExplorer(0.1))
agent = LearningAgent(av_table, learner)

env = FlappyBirdEnv()

task = FlappyBirdTask(env)

experiment = Experiment(task, agent)

while True:
    experiment.doInteractions(1)
    agent.learn()
    agent.reset()
