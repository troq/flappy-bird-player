from scipy import clip, asarray

from pybrain.rl.environments.task import Task

class FlappyBirdTask(Task):
    def __init__(self, environment):
        self.env = environment
        self.env.is_alive = True
        self.lastreward = 0

    def performAction(self, action):
        self.env.performAction(action)

    def getObservation(self):
        return self.env.getSensors()

    def getReward(self):
        return 0 if self.env.is_alive else -1000
