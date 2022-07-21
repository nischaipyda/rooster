import os
import pathlib

from inspect import isclass

from .exceptions import ImproperlyConfigured
from .utils import snake_case_to_camel_case, write_to_file
from settings import BAKE_DIR, LOCATION_DIR
from core.logger import Logger

logger = Logger.get_logger(__name__)


def props(x):
    return {
        key: vars(x).get(key, getattr(x, key)) for key in dir(x)
    }


def get_unbound_function(func):
    if not getattr(func, "__self__", True):
        return func.__func__
    return func


class SubclassWithMeta_Meta(type):
    _meta = None

    def __str__(cls):
        if cls._meta:
            return cls._meta.name
        return cls.__name__

    def __repr__(cls):
        return "<{} meta={}>".format(cls.__name__, repr(cls._meta))


class SubclassWithMeta(metaclass=SubclassWithMeta_Meta):
    """This class improves __init_subclass__ to receive automatically the options from meta"""

    def __init_subclass__(cls, **meta_options):
        """This method just terminates the super() chain"""

        _Meta = getattr(cls, "Meta", None)
        _meta_props = {}
        if _Meta:
            if isinstance(_Meta, dict):
                _meta_props = _Meta
            elif isclass(_Meta):
                _meta_props = props(_Meta)
            else:
                raise Exception(
                    f"Meta have to be either a class or a dict. Received {_Meta}"
                )
            delattr(cls, "Meta")
        options = dict(meta_options, **_meta_props)

        abstract = options.pop("abstract", False)
        if abstract:
            assert not options, (
                "Abstract types can only contain the abstract attribute. "
                f"Received: abstract, {', '.join(options)}"
            )
        else:
            super_class = super(cls, cls)
            if hasattr(super_class, "__init_subclass_with_meta__"):
                super_class.__init_subclass_with_meta__(**options)

    @classmethod
    def __init_subclass_with_meta__(cls, **meta_options):
        """This method just terminates the super() chain"""


class BaseOption(object):
    input_file_path = None
    output_file_name = None
    bake_path = None
    delete_fields = None

    def __init__(self, class_type):
        self.class_type = class_type


class BaseParser(SubclassWithMeta):

    @classmethod
    def __init_subclass_with_meta__(
            cls,
            input_file_path=None,
            output_file_name=None,
            delete_fields=None,
            bake_path=BAKE_DIR,
            _meta=None,
            **options
    ):
        if not _meta:
            _meta = BaseOption(cls)

        if not input_file_path:
            raise ImproperlyConfigured("No input_file_path provided in Meta")

        if not output_file_name:
            raise ImproperlyConfigured("No output_file_name provided in Meta")

        if not os.path.isfile(input_file_path):
            raise ImproperlyConfigured("{0} file does not exists.".format(input_file_path))

        _meta.input_file_path = input_file_path
        _meta.output_file_name = output_file_name
        _meta.delete_fields = delete_fields
        _meta.bake_path = bake_path

        cls._meta = _meta
        super(BaseParser, cls).__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    def _get_bake_file_path(cls):
        return BAKE_DIR / cls._meta.output_file_name

    @classmethod
    def _get_temp_file_path(cls):
        """
        Creates /temp dir in the parent dir of the input_file_path value (if /temp does not exists).

        :return: string containing file path of the /temp dir.
        """
        parent = cls._meta.input_file_path.resolve().parent

        try:
            os.makedirs(pathlib.Path(parent / "temp"), exist_ok=True)
            temp_file_name = pathlib.Path(parent / "temp" / cls._meta.output_file_name)

        except OSError:
            raise
        else:
            return temp_file_name

    @classmethod
    def clean_input(cls, camel_case=False, **kwargs):
        """
        Clean the data from file path provided in input_file_path meta parameter. Output is saved in a /temp folder (
        /temp folder is created in same directory as the input file is in).

        :param camel_case: if true, keys in json files and header in csv will be camel cased.
        :param kwargs:
        :return: None
        """

        temp_file_name = cls._get_temp_file_path()
        if not camel_case:
            if cls._meta.input_file_path.suffix == '.csv':
                temp_file_name = cls._meta.input_file_path.resolve().parent / "temp" / "person.csv"
                import csv
                with open(cls._meta.input_file_path, 'r') as inf, open(temp_file_name, 'w') as outf:
                    for line in inf:
                        columns = ["".join(col) for col in line.strip().split(",")]
                        break
                    # TODO: handle delete_fields and remove all respective columns
                    reader = csv.DictReader(inf, fieldnames=columns)
                    writer = csv.DictWriter(outf, delimiter=',', fieldnames=columns)
                    writer.writeheader()
                    writer.writerows(reader)

            if cls._meta.input_file_path.suffix == '.json':
                import json
                with open(cls._meta.input_file_path, 'r') as inf:
                    data = json.load(inf)
                    temp = list()
                    for item in data:
                        # check for delete_fields and delete respective keys.
                        if cls._meta.delete_fields and len(cls._meta.delete_fields):
                            for key in list(item):
                                if key in cls._meta.delete_fields:
                                    del item[key]
                        temp.append(item)
                    write_to_file(temp, temp_file_name, mode='w')

    @classmethod
    def build_data(cls, **kwargs):
        """
        Buffer step before baking the data to the output file. Any data modifications can be performed in this step.
        :param kwargs:
        :return: data that will be baked to output file.
        """
        temp_file_name = cls._get_temp_file_path()

        if cls._meta.input_file_path.suffix == '.json' or temp_file_name.suffix == '.json':
            import json
            with open(temp_file_name, 'r') as inf:
                data = json.load(inf)
                return data
        print("heloo this is not possible")
        return None

    @classmethod
    def bake_data(cls, data):
        """
        save data to file provided in output_file_name meta parameter.
        :param data:
        :return: None
        """
        print(cls._get_bake_file_path())
        write_to_file(data, f_name=cls._get_bake_file_path())

    @classmethod
    def mutate(cls):
        pass

    @classmethod
    def run(cls, **kwargs):
        """
        Parser starts workflow from run function.
        :param kwargs:
        :return:
        """

        cls.clean_input(**kwargs)
        data = cls.build_data(**kwargs)
        if data:
            cls.bake_data(data)
            cls.mutate()
