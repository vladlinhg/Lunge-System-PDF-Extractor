import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("I have a black cat that likes to eat fish")

distances = {token.i: None for token in doc}

root_token = next(token for token in doc if token.dep_ == "ROOT")
distances[root_token.i] = 0

queue = [root_token]

while queue:
    current_token = queue.pop(0)
    current_distance = distances[current_token.i]

    for child in current_token.children:
        if distances[child.i] is None:
            distances[child.i] = current_distance + 1
            queue.append(child)

for token in distances:
    print (f"{doc[token]} - distance: {distances[token]}")
print(distances)