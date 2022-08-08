import json

json_string = '{ "1":"Red", "2":"Blue", "3":"Green"}'

parsed_json = json.loads(json_string)

print(parsed_json)


# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y)