import os
import yaml
from io import BytesIO, StringIO
from typing import Union


def load_yaml(file: Union[BytesIO, StringIO] = None, filepath:str = None) -> dict:
    """Loads a yaml file.

    :params file: file BytesIO or StringIO type, defaults to None
    :params filepath: file path to the yaml file to be loaded.

    :usage:

        Please provide a `file` or a `filepath`. If `file` is None,
        then use a `filepath` as string. if `file` object is provided,
        the parameter `filepath` will be ignored.


       DEPRECIATED: `load_yaml.py --filepath /file/path/to/filename.yaml`

    :return: a dictionary object
    """

    assert file is not None or filepath is not None

    if file is not None:
        assert isinstance(file, BytesIO) or isinstance(file, StringIO) 

        try:
            yaml_data = yaml.safe_load(file.read())
        except Exception as msg:
            print(f'File loading error. \n {msg}')
            return None
        else:
            return yaml_data

    else:
        assert filepath is not None
        assert os.path.isfile(os.path.abspath(filepath))
        
        with open(filepath, 'r') as file_descriptor:
            try:
                yaml_data = yaml.safe_load(file_descriptor)
            except Exception as msg:
                print(f'File loading error. \n {msg}')
                return None
            else:
                return yaml_data

"""
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--file', action="store",
                        dest="file", type=Union[str, BytesIO, StringIO], default=True)
    args = parser.parse_args()
    load_yaml(args.file)
"""
