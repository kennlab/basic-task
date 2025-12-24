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

config['blocks'] = {}
config['blocks'][1] = {
    'conditions': [1],
    'length': 100
}

config['trial_types'] = {'rect': {
    'module': 'trials.py',
    'class': 'RectTrial'
}}