import json
from .location import Country, State, City


def start():
    Country.run()
    State.run()
    City.run()

    # Tests
    x = ["static/data/bake/countries.json", "static/data/bake/cities.json", "static/data/bake/states.json"]
    for i in x:
        with open(i, 'r') as inf:
            data = json.load(inf)
            print("# of elements in '{}': {}".format(i, len(data)))
