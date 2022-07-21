import json
import base64
import pandas as pd
from settings import MATCHES_DIR, BAKE_DIR

WRITING_MODE = "w"


def write_to_file(data, f_name, mode=WRITING_MODE):
    if f_name == "" or f_name is None:
        raise ValueError("f_name argument cannot be None or empty string.")
    if f_name.suffix == '.json':
        with open(f_name, mode) as fs:
            fs.write(json.dumps(data))


def get_x_dataframe_from_csv(f_name, data_type=None):
    df = pd.read_csv(f_name, dtype=data_type)
    return df


def snake_case_to_camel_case(data: str):
    if data:
        temp = data.split('_')
        return temp[0] + ''.join(ele.title() for ele in temp[1:])


def remove_suffix_id(key):
    return key[0:-2]


def convert_id_suffix_key_to_base64(data, suffix_id_keys):
    temp = list()
    for item in data:
        x = dict({})
        for key, val in item.items():
            if key in suffix_id_keys:
                key = remove_suffix_id(key)
                encoded = (str(key).capitalize() + ":" + str(val)).encode('ascii')
                x[key] = base64.b64encode(encoded).decode('ascii')
            else:
                x[key] = val
        temp.append(x)
    return temp


def build_short_name(data):
    if isinstance(data, str):
        split_data = str(data).split(' ')
        if len(split_data) > 1:
            short_name = "".join((str(i[0]) for i in split_data)).upper()
        else:
            short_name = data[0:3].upper()
        return short_name
    else:
        raise TypeError("Expected of type 'str' but received of type '{0}'", str(type(data)))


def build_overview_csv_file(path=MATCHES_DIR / 'README.txt'):
    """
    Build overview.csv file from Readme.txt in cricsheet folder.
    :param path: cricsheet folder path
    :return: None
    """

    with open(path, 'r') as inf, open(BAKE_DIR / 'overview.csv', 'w') as outf:
        outf.write(str('date,pool,format,gender,fixtureId,teamA,teamB\n'))
        for i, line in enumerate(inf):
            split = str(line).split(' - ')
            if len(split) == 6:
                outf.write(str(line).replace(' - ', ',').replace(' vs ', ','))
