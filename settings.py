import os
import pathlib

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Data directory contains all input and output data of parser
BASE_DATA_DIR = pathlib.Path(ROOT_DIR + "/static/data")
# Match directory contains all fixture data source.
MATCHES_DIR = BASE_DATA_DIR / "matches"
MATCHES_BUILD = BASE_DATA_DIR / "matches/build"

# Bake directory will have all output files from parser.
BAKE_DIR = BASE_DATA_DIR / "bake"
# Locations directory contains all country, city, division data source.
LOCATION_DIR = BASE_DATA_DIR / "locations"
# Locations directory contains all country, city, division data source.
PERSON_DIR = BASE_DATA_DIR / "person"
