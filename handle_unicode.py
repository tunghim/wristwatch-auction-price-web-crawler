import re
import json

with open('raw_geneva-2011-03-27.json') as f:
    data = json.load(f)

for i in data:
    for k, v in i.items():
        i[k] = re.sub('(\\r|\\n|\\r\\n)', '', v)

with open('result_geneva-2011-03-27.json', 'w+') as f:
    json.dump(data, f, ensure_ascii=False)
