import os
import math
from collections import defaultdict, Counter

import pandas as pd
import numpy as np
import yaml
from yaml import safe_load

from internal.keyboard import Keyboard
from internal.corpus import Corpus
from internal.hands import Hands
from internal.setup import *

import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import matplotlib.patheffects as pe
from matplotlib import colormaps

from internal.keyboard import Keyboard
from internal.setup import setup

ARGS = setup("display")
# keyboard = Keyboard.load(ARGS["keyboard"], ARGS["layout"], ARGS["frequency"])


def calculate_metrics(keyboard, bigram_file_path):
    with open(bigram_file_path, 'r', encoding='utf-8') as f:
        bigrams_data = safe_load(f)
    
    total_bigrams = sum(bigrams_data.values())
    
    metrics = {
        'Travel distance': {
            'Total': 0,
            'Finger 1': 0, 'Finger 2': 0, 'Finger 3': 0, 'Finger 4': 0, 'Finger 5': 0,
            'Finger 6': 0, 'Finger 7': 0, 'Finger 8': 0, 'Finger 9': 0, 'Finger 10': 0
        },
        'Hand usage': {
            'Left hand': 0, 'Right hand': 0
        },
        'Finger usage': {
            'Finger 1': 0, 'Finger 2': 0, 'Finger 3': 0, 'Finger 4': 0, 'Finger 5': 0,
            'Finger 6': 0, 'Finger 7': 0, 'Finger 8': 0, 'Finger 9': 0, 'Finger 10': 0
        },
        'Row usage': defaultdict(float),
        'Same finger bigrams': {
            'Left hand': 0, 'Right hand': 0
        },
        'Alternating finger bigrams': {
            'Left hand': 0, 'Right hand': 0
        },
        'Rolling': {
            'Inrolls': 0, 'Outrolls': 0
        }
    }
    
    finger_usage_single = defaultdict(float)
    hand_usage_single = defaultdict(float)
    row_usage_single = defaultdict(float)
    
    for bigram, count in bigrams_data.items():
        if len(bigram) != 2:
            continue
            
        first_char, second_char = bigram
        first_key = keyboard.key_for(first_char)
        second_key = keyboard.key_for(second_char)
        
        if not first_key or not second_key:
            continue
            
        weight = count / total_bigrams
        
        finger_usage_single[first_key.finger] += weight
        hand_usage_single['left' if first_key.finger <= 5 else 'right'] += weight
        
        row_name = f"Row {first_key.row}"
        if first_key.row == 1: row_name = "Row 1"
        elif first_key.row == 2: row_name = "Row 2 top" 
        elif first_key.row == 3: row_name = "Row 3 home"
        elif first_key.row == 4: row_name = "Row 4 bottom"
        else: row_name = f"Row {first_key.row}"
        row_usage_single[row_name] += weight
        
        distance = math.sqrt((second_key.x - first_key.x)**2 + (second_key.y - first_key.y)**2)
        metrics['Travel distance']['Total'] += distance * weight
        metrics['Travel distance'][f'Finger {first_key.finger}'] += distance * weight
        
        first_hand = 'left' if first_key.finger <= 5 else 'right'
        second_hand = 'left' if second_key.finger <= 5 else 'right'
        
        if first_key.finger == second_key.finger:
            metrics['Same finger bigrams'][f'{first_hand.capitalize()} hand'] += weight
        elif first_hand != second_hand:
            metrics['Alternating finger bigrams'][f'{first_hand.capitalize()} hand'] += weight
            
        if first_hand == 'left' and second_hand == 'right':
            metrics['Rolling']['Outrolls'] += weight
        elif first_hand == 'right' and second_hand == 'left':
            metrics['Rolling']['Inrolls'] += weight
    
    for finger in range(1, 11):
        metrics['Finger usage'][f'Finger {finger}'] = finger_usage_single.get(finger, 0)
    
    metrics['Hand usage']['Left hand'] = hand_usage_single.get('left', 0)
    metrics['Hand usage']['Right hand'] = hand_usage_single.get('right', 0)
    
    for row_name, usage in row_usage_single.items():
        metrics['Row usage'][row_name] = usage
    
    metrics['Row usage'] = dict(metrics['Row usage'])
    
    return metrics

corpus_name = os.path.basename(ARGS["corpus"]).replace('.', '_')
bigram_file_path = f'./data/bigramms/{corpus_name}.yaml'

keyboard = Keyboard.load(
    ARGS["keyboard"],
    ARGS["layout"], 
    ARGS["frequency"]
)

metrics = calculate_metrics(keyboard, bigram_file_path)
print(yaml.dump(metrics, allow_unicode=True, default_flow_style=False))
