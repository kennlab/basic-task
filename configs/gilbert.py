import numpy as np
from typing import Dict, Any
from itertools import product
import os

W, H = 1080, 1920
config: Dict[str, Any] = dict(
    name='gilbert',
    coordinate_space='ndc',
    storage={'type':'sqlite', 'path':'data/data.db'},
    ITI=1.5,
    duration=60,
    size=(.75,.75),
    display={
        'size': (W, H),
        'display': 0,
        'fullscreen': True
    },
    remote_server={
        'enabled': True,
        'show': False,
        'template_path': 'server'
    },
    io={
        'reward': {
            'type': 'ISMATEC_SERIAL',
            'address': os.environ.get('PUMP', '/dev/ttyACM0'),
            'channels': [
                {'channel': 1, 'clockwise': True, 'speed': 100},
                {'channel': 4, 'clockwise': True, 'speed': 100}
            ]
        }
    },
    reward_params=dict(duration=4,n_pulses=1)
)

CENTER = 0, 0
W, H = 2, 2
config['conditions'] = {}
config['conditions'][1] = {
    'trial_type': 'rect',
    'position': CENTER,
    'size': (W, H),
    'colour': (255,0,0)
}

PAD = .5
LEFT = CENTER[0] - PAD, CENTER[1]
RIGHT = CENTER[0] + PAD, CENTER[1]
positions = LEFT, RIGHT
for i, position, in enumerate(positions, start=2):
    config['conditions'][i] = {
        'trial_type': 'rect', 
        'position': position, 
        'colour': (255,0,0)
    }
for i, position, in enumerate(positions, start=4):
    config['conditions'][i] = {
        'trial_type': 'image', 
        'position': position, 
        'image_path': 'stimuli/aadac.png'
    }

config['blocks'] = {}
config['blocks'][1] = {
    'conditions': [1],
    'length': 5,
    'method': 'random',
    'transition': [
        {'condition': {'outcome': 'correct', 'min': 4}, 'next': 2},
        {'next': 1}
    ]
}
config['blocks'][2] = {
    'conditions': [2, 3],
    'length': 15,
    'method': 'random',
    'transition': [
        {'condition': {'outcome': 'correct', 'min': 12}, 'next': 3},
        {'condition': {'outcome': 'correct', 'min': 9}, 'next': 2},
        {'next': 1}
    ]
}
config['blocks'][3] = {
    'conditions': [2, 3, 4, 5],
    'length': 50,
    'method': 'random',
    'transition': [
        {'next': 2}
    ]
}

config['trial_types'] = {
    'rect': {'module': 'trials.py', 'class': 'RectTrial'},
    'image': {'module': 'trials.py', 'class': 'ImageTrial'},
}

def update_variables(scene: "Scene", event: "Event") -> None:
    for key, value in event['variables'].items():
        print(key, value, type(value))
        scene.manager.variables[key] = value

config['actions'] = {
    'update_variables': update_variables
}

config['hotkeys'] = {
    '4': {'do': 'pump_on'},
    '8': {'do': 'pump_off'},
    '3': {'do': 'pause'},
    '7': {'do': 'unpause'},
    '5': {'do': 'quit'},
}
config['valid_times'] = [
    {'start': '08:00', 'end': '18:00'}
]
