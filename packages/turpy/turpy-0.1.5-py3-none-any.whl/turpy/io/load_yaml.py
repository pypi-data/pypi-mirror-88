import os
import yaml
from io import BytesIO, StringIO, IOBase
from typing import Union


def load_yaml(file: Union[str, BytesIO, StringIO]) -> dict:
    """Loads a yaml file.

    Can be used as stand alone script by

    :params filepath: file path to the yaml file to be loaded.

    :usage:

       `load_yaml.py --filepath /file/path/to/filename.yaml`

    :return: a dictionary object
    """

    assert file is not None

    if isinstance(file, IOBase):        
        assert os.path.isfile(os.path.abspath(file.name))
    elif isinstance(file, str):
        assert os.path.isfile(os.path.abspath(file))
    else:
        assert 2==1  # False        
        return None
    
    with open(file, 'r') as file_descriptor:
        try:
            yaml_data = yaml.safe_load(file_descriptor)
        except Exception as msg:
            print(f'File loading error. \n {msg}')
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
