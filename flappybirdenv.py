from pybrain.rl.environments.environment import Environment
from scipy import zeros, asarray

from SimpleCV import Image

from screenshot import screenshot
from simulate import mouseclick
from features import Features
from settings import PARAMS, REGION, PATH, CLICK_POS, RESTART_BTN_POS

f = Features(**PARAMS)

class FlappyBirdEnv(Environment):
    indim = 1
    outdim = 4

    discreteActions = True
    numActions = 2

    def getSensors(self):
        screenshot(PATH, REGION)
        im = Image(PATH)
        f.set_image(im)
        sensors = asarray(f.extract())
        self.is_alive = sensors[2]
        return sensors

    def performAction(self, action):
        #if action is True, then click, otherwise do nothing
        if action:
            mouseclick(CLICK_POS)

    def reset(self):
        for x in range(2):
            mouseclick(RESTART_BTN_POS)
