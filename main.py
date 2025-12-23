from experiment.experiments.adapters import *
from experiment.experiments.scene import Scene
from experiment.manager import Manager
from experiment.engine.pygame import PygameManager
from experiment.trial import Trial, TrialResult

from pathlib import Path
import time

SIZE = (200, 200)
PAD = 100
ITI = 1.0

class BasicTrial(Trial):
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
        data = {}
        im = self.get_target()
        ta = TouchAdapter(
            None,
            {'target': im},
            allow_outside_touch=True
        )
        scene = Scene(mgr, ta)
        scene.run()
        if scene.quit:
            return TrialResult(continue_session=False, outcome='quit', data=data)
        if ta.chosen == 'target':
            outcome = 'correct'
            mgr.renderer.set_background('GREEN')
            mgr.good_monkey(**self.reward_params)
            mgr.renderer.set_background()
        else:
            outcome = 'incorrect'
            mgr.renderer.set_background('RED')
            time.sleep(0.5)
            mgr.renderer.set_background()
        mgr.record(outcome=outcome)
        return TrialResult(continue_session=True, outcome=outcome, data=data)

class ImageTrial(BasicTrial):
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

class RectTrial(BasicTrial):
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
    params = dict(
        trialtype = 'rect',
        position = (1080/2, 1920/2),
        size = (1080, 1920),
        colour = (255,0,0)
    )
    if params['trialtype'] == 'image':
        trial = ImageTrial(params['image_path'], params['position'], size=params['size'])
    else:
        trial = RectTrial(params['colour'], params['position'], size=params['size'])
    mgr.record(**params)
    return trial

def main(monkey):
    SIZE = 1080, 1920
    FULLSCREEN = True
    DISPLAY = 0
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

    continue_session = True
    taskstate = {'correct': []} # You can use this to store info about the task between trials
    while continue_session:
        trial = get_trial(mgr, taskstate)
        mgr.record(block=1, block_number=1)
        result = mgr.run_trial(trial)
        continue_session = result.continue_session
        taskstate['correct'].append(result.outcome=='correct')
        time.sleep(ITI)
    mgr.cleanup()
if __name__ == '__main__':
    import sys
    monkey = sys.argv[1] if len(sys.argv) > 1 else None
    main(monkey)