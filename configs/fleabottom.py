import numpy as np
from typing import Dict, Any
from itertools import product

config: Dict[str, Any] = dict(
    name='fleabottom',
    duration=60,
    size=(200,200),
    bbox=dict(width=300, height=300),
)

W, H = 1080, 1920

config['conditions'] = {}
config['conditions'][1] = {
    'trial_type': 'rect',
    'position': (W/2, H/2),
    'size': (W, H),
    'colour': (255,0,0)
}

CENTER = (W/2, H/2)
PAD = 300
LEFT = CENTER[0] - PAD, CENTER[1]
RIGHT = CENTER[0] + PAD, CENTER[1]
positions = LEFT, RIGHT
for i, position, in enumerate(positions, start=2):
    config['conditions'][i] = {
        'trial_type': 'rect', 
        'position': position, 
        'size': (200,200), 
        'colour': (255,0,0)
    }
for i, position, in enumerate(positions, start=4):
    config['conditions'][i] = {
        'trial_type': 'image', 
        'position': position, 
        'size': (200,200), 
        'image_path': 'stimuli/aadac.png'
    }

config['blocks'] = {}
config['blocks'][1] = {
    'conditions': [1],
    'length': 5,
    'method': 'random',
    # not implemented yet but should allow for conditional transitions
    'transition': [
        {'condition': 'accuracy>.8', 'next': 2},
        {'next': 1}
    ]
}
config['blocks'][2] = {
    'conditions': [2, 3],
    'length': 15,
    'method': 'random',
    'transition': [
        {'condition': 'accuracy>.8', 'next': 3},
        {'next': 1}
    ]
}
config['blocks'][3] = {
    'conditions': [2, 3, 4, 5],
    'length': 50,
    'method': 'random',
    'transition': [
        {'next': 1}
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