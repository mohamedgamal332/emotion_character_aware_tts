file_name = "Moby Dick.txt"

input_directory = "../temp/"
output_directory = "../temp/"

import re
import os
import json

# read text
file_path = os.path.join(input_directory, file_name) # Replace with your text file's path
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

def extract_sentences(text):
    quote_sentences = [i for i in text.split("“") if re.match(r'.*[A-Za-z0-9].*', i)]
    tokens = []
    for i in [j for j in quote_sentences[0].split(".") if re.match(r'.*[A-Za-z0-9].*', j)]:
        tokens.append(("Sentence", i.strip().lower()))
        
    for i in quote_sentences[1:]:
        if re.match(r'[A-Za-z0-9]|:', i.strip()[-1]): tokens.append(tuple(["Link"]))
        parts = [i for i in i.split("”") if i]
        tokens.append(("Quote", parts[0].strip().lower()))
        flag = re.match(r'^[A-Za-z0-9]', parts[1].strip()) if len(parts) > 1 else False
        for j in parts[1:]:
            for k in [l for l in j.split(".") if re.match(r'.*[A-Za-z0-9].*', l)]:
                if flag: tokens.append(tuple(["Link"])); flag = False
                tokens.append(("Sentence", k.strip().lower()))
                
    return tokens

# Example usage
tokens = extract_sentences(text)
flat = [i[1] for i in tokens if len(i) > 1]
full_words = re.findall(r'\b\w+\b', text.lower())
words = sorted(list(set(i.lower() for i in re.findall(r'\b\w+\b', text))))

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# write tokens
with open(os.path.join(output_directory, "sentences-tokenized.json"), 'w', encoding='utf-8') as file:
    json.dump(tokens, file, ensure_ascii=False, indent=4)

with open(os.path.join(output_directory, "vocab.json"), 'w', encoding='utf-8') as file:
    json.dump(words, file, ensure_ascii=False, indent=4)
    
with open(os.path.join(output_directory, "full-vocab.json"), 'w', encoding='utf-8') as file:
    json.dump(full_words, file, ensure_ascii=False, indent=4)
    
with open(os.path.join(output_directory, "flat-text.json"), 'w', encoding='utf-8') as file:
    json.dump(flat, file, ensure_ascii=False, indent=4)