import numpy as np
from typing import Dict, Any
from itertools import product

config: Dict[str, Any] = dict(
    name='fleabottom',
    duration=100,
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
positions = list(product([W/4, 3*W/4], [H/4, 3*H/4])) + [(W/2, H/2)]
for i, position, in enumerate(positions, start=2):
    config['conditions'][i] = {'trial_type': 'rect', 'position': position, 'size': (W/3, H/3), 'colour': (255,0,0)}

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
    'conditions': [2, 3, 4, 5, 6],
    'length': 100,
    'method': 'random',
    # not implemented yet but should allow for conditional transitions
    'transition': [
        {'next': 1}
    ]
}

config['trial_types'] = {'rect': {
    'module': 'trials.py',
    'class': 'RectTrial'
}}

def update_variables(scene: "Scene", event: "Event") -> None:
    for key, value in event['variables'].items():
        print(key, value, type(value))
        scene.manager.variables[key] = value

config['actions'] = {
    'update_variables': update_variables
}