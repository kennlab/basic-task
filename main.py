from experiment.experiments.adapters import *
from experiment.experiments.scene import Scene
from experiment.manager import Manager
from experiment.engine.pygame import PygameManager

from pathlib import Path
import time

SIZE = (200, 200)
PAD = 100
ITI = 1.0

class Trial:
    DEFAULT_REWARD_PARAMS = {
        'duration': 0.5,
        'interpulse_interval': 0.2,
        'n_pulses': 3
    }
    def __init__(self, position, size=SIZE, reward_params=None):
        self.position = position
        self.size = size
        self.reward_params = reward_params or self.DEFAULT_REWARD_PARAMS
    def get_bbox(self):
        w, h = self.size
        return dict(width=w+PAD, height=h+PAD)
    def get_target(self):
        raise NotImplementedError
    def run(self, mgr: Manager):
        im = self.get_target()
        ta = TouchAdapter(
            None,
            {'target': im},
            allow_outside_touch=True
        )
        scene = Scene(mgr, ta)
        scene.run()
        if scene.quit:
            return False
        if ta.chosen == 'target':
            mgr.record(outcome='correct')
            mgr.renderer.set_background('GREEN')
            mgr.good_monkey(**self.reward_params)
            mgr.renderer.set_background()
        else:
            mgr.record(outcome='incorrect')
            mgr.renderer.set_background('RED')
            time.sleep(0.5)
            mgr.renderer.set_background()
        return True

class ImageTrial(Trial):
    def __init__(self, image_path, position, size=SIZE, reward_params=None):
        super().__init__(position, size, reward_params)
        self.image_path = image_path
    def get_target(self):
        im = ImageAdapter(
            self.image_path,
            position=self.position,
            bbox=self.get_bbox(),
            size=self.size
        )
        return im

class RectTrial(Trial):
    def __init__(self, colour, position, size=SIZE, reward_params=None):
        super().__init__(position, size, reward_params)
        self.colour = colour
    def get_target(self):
        im = RectAdapter(
            colour=self.colour,
            position=self.position,
            bbox=self.get_bbox(),
            size=self.size
        )
        return im
    
import pandas as pd
def get_trial(mgr, taskstate=None):
    IMAGE = 'C:/Users/Administrator/Desktop/task01/stimuli/an.png'
    # ANALYTIC METHOD
    # beh = pd.DataFrame(mgr.datastore.records)
    # if beh.iloc[-5:]['outcome'].value_counts()['correct'] >= 3: 
    #     params = dict(
    #         trialtype = 'rect',
    #         position = (300, 300),
    #         size = (300, 300),
    #         colour = (0, 255, 0)
    #     )
    # else:
    #     params = dict(
    #         trialtype = 'image',
    #         position = (600, 300),
    #         size = (300, 300),
    #         image_path = IMAGE
    #     )

    # RANDOM METHOD
    import random
    params = dict(
        trialtype = random.choice(['image', 'rect']),
        position = (random.randint(200, 1166), random.randint(200, 568)),
        size = (300, 300)
    )
    if params['trialtype'] == 'image':
        params['image_path'] = IMAGE
    else:
        params['colour'] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))


    if params['trialtype'] == 'image':
        trial = ImageTrial(params['image_path'], params['position'], size=params['size'])
    else:
        trial = RectTrial(params['colour'], params['position'], size=params['size'])
    mgr.record(**params)
    return trial

def main(monkey):
    SIZE = 1366, 768
    FULLSCREEN = False
    DISPLAY = 1
    if monkey is not None:
        data_dir = Path('data') / monkey
    else:
        data_dir = Path('data') / 'test'
    mgr = PygameManager(
        data_directory=data_dir,
        config={
            'display': {
                'size': SIZE, 
                'display': DISPLAY, 
                'fullscreen': FULLSCREEN, 
            },
            'background': (200, 200, 200),
            'io': {
                'reward': {
                    'type': 'ISMATEC_SERIAL',
                    'address': 'COM5',
                    'channels': [
                        {'channel': '2', 'clockwise': True, 'speed': 100},
                        {'channel': '3', 'clockwise': True, 'speed': 100}
                    ]
                }
            },
            'remote_server': {
                'enabled': True,
                'show': True,
                'template_path': Path('server').absolute(),
            }
        }
    )

    continue_experiment = True
    taskstate = {} # You can use this to store info about the task between trials
    while continue_experiment:
        trial = get_trial(mgr, taskstate)
        continue_experiment = mgr.run_trial(trial)
        time.sleep(ITI)
    mgr.cleanup()
if __name__ == '__main__':
    import sys
    monkey = sys.argv[1] if len(sys.argv) > 1 else None
    main(monkey)