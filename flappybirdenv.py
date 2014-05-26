from pybrain.rl.environments.environment import Environment
from scipy import zeros

from SimpleCV import Image

from screenshot import screenshot
from simulate import mouseclick
from features import Features
from settings import PARAMS, REGION, PATH, CLICK_POS, RESTART_BTN_POS

f = Features(**PARAMS)

class FlappyBirdEnv(Environment):
    indim = 2
    outdim = 4

    def getSensors(self):
        screenshot(PATH, REGION)
        im = Image(PATH)
        f.set_image(im)
        return f.extract()

    def performAction(self, action):
        #if action is True, then click, otherwise do nothing
        if action:
            mouseclick(CLICK_POS)

    def reset(self):
        for x in range(2):
            mouseclick(RESTART_BTN_POS)
