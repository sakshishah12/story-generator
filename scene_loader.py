import json
import random
from collections import defaultdict

with open("final.json") as f:
    scenes = json.load(f)

themes = defaultdict(list)

for s in scenes:
    themes[s["theme"]].append(s)

def get_themes():
    return sorted(themes.keys())

def get_random_query(theme):
    return random.choice(themes[theme])["query"]