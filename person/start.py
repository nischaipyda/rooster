import json
from .person import Person


def start():
    Person.run()

    x = ["static/data/bake/person.json"]
    for i in x:
        with open(i, 'r') as inf:
            data = json.load(inf)
            print(len(data))
