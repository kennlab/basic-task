from experiment.experiments.adapters import *
from experiment.experiments.scene import Scene
from experiment.manager import Manager
from experiment.trial import Trial, TrialResult

class BasicTrial(Trial):
    DEFAULT_REWARD_PARAMS = {
        'duration': 0.5,
        'interpulse_interval': 0.2,
        'n_pulses': 3
    }
    DEFAULT_SIZE = (200, 200)
    PAD = 100
    def __init__(self, position, duration=None, size=None, reward_params=None):
        self.position = position
        if size is None:
            size = self.DEFAULT_SIZE
        self.size = size
        self.duration = duration
        self.reward_params = reward_params or self.DEFAULT_REWARD_PARAMS
    @classmethod
    def from_config(cls, config):
        position = config['position']
        size = config.get('size')
        reward_params = config.get('reward_params')
        duration = config.get('duration')
        return cls(position, duration, size, reward_params)
    def get_bbox(self):
        w, h = self.size
        return dict(width=w+self.PAD, height=h+self.PAD)
    def get_target(self):
        raise NotImplementedError
    def run(self, mgr: Manager):
        data = {}
        im = self.get_target()
        ta = TouchAdapter(
            self.duration,
            {'target': im},
            allow_outside_touch=True
        )
        scene = Scene(mgr, ta)
        error_scene = Scene(mgr, TimeCounter(0.5), background=(255,0,255))
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
            error_scene.run()
        mgr.record(outcome=outcome)
        return TrialResult(continue_session=True, outcome=outcome, data=data)

class ImageTrial(BasicTrial):
    def __init__(self, image_path, position, duration=None, size=None, reward_params=None):
        super().__init__(position, duration, size, reward_params)
        self.image_path = image_path
    @classmethod
    def from_config(cls, config):
        image_path = config['image_path']
        position = config['position']
        size = config.get('size')
        reward_params = config.get('reward_params')
        duration = config.get('duration')
        return cls(image_path, position, duration, size, reward_params)
    def get_target(self):
        im = ImageAdapter(
            self.image_path,
            position=self.position,
            bbox=self.get_bbox(),
            size=self.size
        )
        return im

class RectTrial(BasicTrial):
    def __init__(self, colour, position, duration, size=None, reward_params=None):
        super().__init__(position, duration, size, reward_params)
        self.colour = colour
    @classmethod
    def from_config(cls, config):
        colour = config['colour']
        position = config['position']
        size = config.get('size')
        reward_params = config.get('reward_params')
        duration = config.get('duration')
        return cls(colour, position, duration, size, reward_params)
    def get_target(self):
        im = RectAdapter(
            colour=self.colour,
            position=self.position,
            bbox=self.get_bbox(),
            size=self.size
        )
        return im
    
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
