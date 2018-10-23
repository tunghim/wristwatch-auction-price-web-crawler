import json

with open('raw.json') as f:
    data = json.load(f)

with open('result.json', 'w+') as f:
    json.dump(data, f, ensure_ascii=False)
