import json

switches = {'v-t2-leaf-2': '2:52184604307358850', 'v-t2-leaf-4': '2:52184604308964620',
            'v-t2-leaf-3': '2:52184604308210887', 'v-t2-leaf-1': '2:52184604306015293'}

with open('apod.json', 'r') as f:
    json_text = f.read()

new_dict = json.loads(json_text)
test = new_dict["data"]
dict1 = {}
for i in test:
    for key, value in i.items():
        if key == 'data':
            dict1.update({i["vlan_id"]: value})
print(sorted(dict1.items()))
dict2 = {}
for key, value in sorted(dict1.items()):
    for i in value:
        for key1 in list(i.keys()):
            if ('switch_id_1' in key1):
                dict2.update({key: [i['switch_id_1'], i['switch_id_2']]})
print(dict2)

"""
# Decode the JSON string into a Python dictionary.
apod_dict = json.loads(json_text)
for key in apod_dict:
    print(key + "{} {}".format(':', apod_dict[key]))

# Encode the Python dictionary into a JSON string.
'''
Without the indent the Json is not printing in legitimate manner
'''
new_json_string = json.dumps(apod_dict, indent=4)
print(new_json_string)
"""