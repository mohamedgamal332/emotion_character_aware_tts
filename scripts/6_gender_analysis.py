import json
import re

char_dict = json.load(open("../temp/char_dict.json", "r"))
out_text = json.load(open("../temp/character-attribution.json", "r"))

characters_unique = list(set(char_dict.values()))
character_instances = {i : [] for i in characters_unique}

for i in range(len(out_text)):
    character_instances[out_text[i][1]].append(i)
    
character_context = {i : [] for i in characters_unique}

post = 2; pre = 0

for i in characters_unique:
    instances = character_instances[i]
    context = []
    for j in range(-pre, post +1):
        context.extend([j + k for k in instances if ((j + k) not in instances) or i == "Narrator"])
        
    context = [out_text[i][0] for i in context if i >= 0 and i < len(out_text)]
    character_context[i] = re.findall(r'\b\w+\b', (" ".join(context)).lower())
    
character_context

masculine_words = ["he", "his", "him", "himself", "mr", "sir", "lord", "king", "prince", "duke", "father", "brother", "uncle", "son", "boy", "man", "male", "gentleman", "lad", "guy", "dude", "husband", "boyfriend", "groom", "nephew", "grandson", "actor", "waiter", "god"]

feminine_words = ["she", "her", "hers", "herself", "mrs", "miss", "ms", "lady", "queen", "princess", "duchess", "mother", "sister", "aunt", "daughter", "girl", "woman", "female", "lady", "lass", "gal", "wife", "girlfriend", "bride", "niece", "granddaughter", "actress", "waitress", "goddess"]

male_probability = {i : 0 for i in characters_unique}

for i in characters_unique:
    context = character_context[i]
    masculine_score = sum([context.count(i) for i in masculine_words])
    feminine_score = sum([context.count(i) for i in feminine_words])
    male_probability[i] = (masculine_score + 1) / (masculine_score + feminine_score + 2)
    
genders = [(i, "M" if male_probability[i] >= 0.5 else "F") for i in characters_unique]

json.dump(genders, open("../temp/gender.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)