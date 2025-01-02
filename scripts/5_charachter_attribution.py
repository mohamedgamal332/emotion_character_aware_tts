import json
import numpy as np
import re

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import to_categorical

from utilities import find_name

tokens = json.load(open("../temp/sentences-tokenized.json", "r"))
characters = json.load(open("../temp/characters.json", "r"))

speech_verbs = [
    # neutral/multi-purpose words
    "said", "acknowledged", "added", "agreed", "announced", "articulated", "asserted", "backtracked", 
    "began", "blurted", "called", "commented", "communicated", "conferred", "considered", 
    "contended", "declared", "denoted", "drawled", "elaborated", "emitted", "ended", 
    "enunciated", "expounded", "expressed", "greeted", "interjected", "mentioned", 
    "noted", "observed", "orated", "persisted", "predicted", "pronounced", "quipped", 
    "recited", "reckoned", "related", "remarked", "repeated", "replied", "responded", 
    "shared", "slurred", "stated", "suggested", "told", "urged", "uttered", 
    "vocalized", "voiced",
    # happy/excited words
    "approved", "babbled", "beamed", "bubbled", "chattered", "cheered", "chimed in", 
    "chortled", "chuckled", "congratulated", "complimented", "crooned", "effused", 
    "exclaimed", "giggled", "grinned", "gushed", "jabbered", "joked", "laughed", 
    "praised", "rejoiced", "sang", "smiled", "thanked", "tittered", "trilled", "yammered",
    # sad/upset words
    "agonized", "apologized", "bawled", "blubbered", "cried", "fretted", "grieved", 
    "groaned", "lamented", "mewled", "moaned", "mumbled", "sobbed", "sighed", 
    "sniffled", "sniveled", "wailed", "wept",
    # angry words
    "accused", "choked", "badgered", "barked", "bellowed", "chastised", "cursed", 
    "demanded", "exploded", "fumed", "glowered", "growled", "hissed", "insulted", 
    "raged", "ranted", "reprimanded", "roared", "scolded", "screamed", "screeched", 
    "snarled", "spat", "shouted", "swore", "thundered", "vociferated", "yelled",
    # annoyed words
    "bleated", "complained", "condemned", "criticized", "exhaled", "groused", 
    "grumbled", "grunted", "heaved", "insisted", "mocked", "rasped", "rejoined", 
    "retorted", "scoffed", "smirked", "snapped", "whined",
    # frightened/pained words
    "coughed", "cautioned", "gulped", "howled", "keened", "panted", "prayed", 
    "quavered", "screamed", "shrieked", "shuddered", "squalled", "squealed", 
    "trembled", "wailed", "warbled", "whimpered", "yelped", "yowled", "warned",
    # prideful words
    "advertised", "bloviated", "boasted", "boomed", "bossed", "bragged", "broadcasted", 
    "crowed", "exhorted", "dictated", "gloated", "moralized", "ordered", "prattled", 
    "preached", "sermonized", "snorted", "swaggered", "trumpeted",
    # uncertainty words
    "breathed", "doubted", "faltered", "hesitated", "lilted", "mumbled", "murmured", 
    "muttered", "shrugged", "squeaked", "stammered", "stuttered", "swallowed", 
    "trailed off", "vacillated", "whispered",
    # words that make fun
    "derided", "jeered", "heckled", "lampooned", "mocked", "mimicked", "parodied", 
    "ridiculed", "satirized", "scorned", "spoofed", "sneered", "snickered", "taunted", "teased",
    # words that ask a question
    "asked", "begged", "challenged", "contemplated", "guessed", "hinted", "hypothesized", 
    "implied", "inquired", "interrogated", "invited", "mouthed", "mused", "pleaded", 
    "pondered", "probed", "proposed", "puzzled", "repeated", "requested", 
    "requisitioned", "queried", "questioned", "quizzed", "solicited", "speculated", "wondered",
    # words that give an answer
    "accepted", "advised", "affirmed", "alleged", "answered", "assured", "avowed", 
    "claimed", "conceded", "concluded", "confided", "confirmed", "explained", 
    "disclosed", "disseminated", "divulged", "imparted", "informed", "indicated", 
    "maintained", "notified", "offered", "passed on", "proffered", "promised", 
    "promulgated", "released", "reported", "revealed", "shared", "specified", 
    "speculated", "supposed", "testified", "transmitted", "verified"
]

# Definite pairs
pairs = []

for ndx in range(len(tokens)):
    if tokens[ndx][0] == "Link":
        if tokens[ndx-1][0] == "Quote":
            quote = tokens[ndx-1]
            sentence = tokens[ndx+1]
            q_ndx = ndx-1
        else:
            quote = tokens[ndx+1]
            sentence = tokens[ndx-1]
            q_ndx = ndx+1
        
        found = False
        
        for verb in speech_verbs:
            if verb in sentence[1]:
                for char in characters:
                    if f"{char} {verb}" in sentence[1]:
                        pairs.append((q_ndx, char, quote[1]))
                        found = True
                        break
                    elif f"{verb} {char}" in sentence[1]:
                        pairs.append((q_ndx, char, quote[1]))
                        found = True
                        break
            if found: break

print(f"Definite pairs count : {len(pairs)}")

words = json.load(open("../temp/vocab.json", "r"))
word_to_index = {word: i for i, word in enumerate(words)}

# Definite pairs embedding
def prepare_input_embedding(ndx, pre_count=2, post_count=2):
    diff = 0
    preceding = []
    end_flag = False

    for i in range(pre_count):
        while True:
            diff = (diff % ndx) + 1
            if (token := tokens[ndx-diff])[0] in ["Sentence"]:
                have_names = False
                for char in characters:
                    if find_name(char, token[1]):
                        have_names = True
                        break
                if have_names: 
                    preceding.append(token[1])
                    break

            if (diff == ndx) and (not preceding):
                preceding = [''] * pre_count
                end_flag = True
                break
        
        if end_flag: break
        
    diff = 0
    following = []
    end_flag = False

    for i in range(post_count):  # Looking for 4 following sentences
        while True:
            diff = ((diff + 1) % (len(tokens) - ndx))
            token = tokens[ndx + diff]
            if token[0] in ["Sentence"]:
                have_names = False
                for char in characters:
                    if find_name(char, token[1]):
                        have_names = True
                        break
                if have_names: 
                    following.append(token[1])
                    break
                
            if (diff == len(tokens) - ndx - 1) and (not following):
                following = ['']*post_count
                end_flag = True
                break
            
        if end_flag: break

    context = preceding + following #+ [tokens[i_ndx][1]]
    
    embedding = []
    for sentence in context:
        sentence_tokens = re.findall(r'\b\w+\b', sentence)
        sentence_embedding = []
        if len(sentence_tokens) == 0: sentence_embedding = [-1] * 32
        else:
            for i in range(32):
                sentence_embedding.append(word_to_index.get(sentence_tokens[i%len(sentence_tokens)], 0))
        embedding += sentence_embedding

    return np.array(embedding[:256])  # Ensure fixed size

def embed(pairs, pre_count=2, post_count=2):
    inputs = []; outputs = []
    for ndx, char, _ in pairs:
        outputs.append(word_to_index.get(char, 0))
        inputs.append(prepare_input_embedding(ndx, pre_count, post_count))

    inputs = np.array(inputs)
    outputs = np.array(outputs)
    
    return inputs, outputs

inputs, outputs = embed(pairs, 0, 2)

# Number of classes
n_classes = len(characters)

# One-hot encode the outputs
outputs_one_hot = to_categorical(outputs[:], num_classes=n_classes)

# Define the model
model = Sequential([
    Dense(128, activation='linear', input_shape=(2*32,)),  # Hidden layer 1
    Dropout(0.2),
    Dense(64, activation='linear'),  # Hidden layer 2
    Dropout(0.2),
    Dense(64, activation='linear'),  # Hidden layer 3
    Dropout(0.2),
    Dense(n_classes, activation='softmax')  # Output layer
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(inputs[:], outputs_one_hot, epochs=100, batch_size=16, validation_split=0.2)

# Evaluate the model
loss, accuracy = model.evaluate(inputs[:], outputs_one_hot)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Compute speaker [Neural]
def compute_speaker(ndx, pre_count=2, post_count=2):
    inpt = prepare_input_embedding(ndx, pre_count, post_count)
    prediction = model.predict(np.array([inpt]))
    predicted_class = np.argmax(prediction, axis=1)
    return words[predicted_class[0]]

char_dict = json.load(open("../temp/char_dict.json", "r"))

out_text = []
for i in range(len(tokens)):
    if tokens[i][0] == "Sentence":
        out_text.append((tokens[i][1], "Narrator"))
    elif tokens[i][0] == "Quote":
        out_text.append((tokens[i][1], char_dict[compute_speaker(i, 0, 2)]))
        
json.dump(out_text, open("../temp/character-attribution.json", "w"), ensure_ascii=False, indent=4)