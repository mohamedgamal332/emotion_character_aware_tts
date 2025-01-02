from transformers import pipeline
from ipywidgets.widgets import IntProgress
from IPython.display import display
from utilities import find_name

import json
import re

flat = json.load(open("../temp/flat-text.json", "r", encoding="utf-8"))
words = json.load(open("../temp/vocab.json", "r", encoding="utf-8"))

ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

def extract_names(text):
    # Perform Named Entity Recognition (NER)
    entities = ner_pipeline(text)
    
    # Extract entities labeled as "PER" (Person)
    names = {entity['word'] for entity in entities if entity['entity_group'] == "PER"}
    
    return names

max_progress= len(flat)

f = IntProgress(min=0, max=max_progress, bar_style='info', style = {'description_width': 'initial'}) # instantiate the bar
display(f) # display the bar
prev = set()
characters = set()
discarded = set()

for i in flat:
    new = extract_names(i)
    for name in new:
        if find_name(name, i):
            characters.add(name.split(" ")[-1])
        elif name not in discarded:
            discarded.add(name)
            
    if diff := characters.difference(prev):
        prev = set(characters)
            
    f.value += 1
    f.description = f"Progress: {f.value*100/max_progress:0.2f}% "
    
characters = list(characters)

exclamation_patterns = [r'^u*h*m*$']

excluded = set()

for character in characters:
    for pattern in exclamation_patterns:
        if re.match(pattern, character):
            excluded.add(character)
            break
        
characters = [character for character in characters if character not in excluded]

words.sort(key=lambda i: not(i in characters))

json.dump(characters, open("../temp/characters.json", "w", encoding="utf-8"))
json.dump(words, open("../temp/vocab.json", "w", encoding="utf-8"))