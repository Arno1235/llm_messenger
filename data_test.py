import json

with open("./data/formatted_messages.json") as f:
    data = json.load(f)

print(len(data))