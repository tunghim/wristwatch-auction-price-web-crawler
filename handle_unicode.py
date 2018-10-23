import re
import json

with open('raw.json') as f:
    data = json.load(f)

for i in data:
    for k, v in i.items():
        i[k] = re.sub('(\\r|\\n|\\r\\n)', '', v)

with open('result.json', 'w+') as f:
    json.dump(data, f, ensure_ascii=False)
