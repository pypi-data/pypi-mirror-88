import importlib
import os
import sys
from turpy.logger import log
from typing import List
import re


def string_search_in_list(input_string:str, searching_list:List[str]):
    """List of items where a particular string matches (case insensitive) items in a list of strings.
    
    :returns: items in list where there was a match

    """
    r = re.compile(input_string, re.IGNORECASE)
    return list(filter(r.search, searching_list))


def script_as_module(module_filepath: str, package_path: str = './project/services/'):
    """Loads a python script, register as module, and makes it available for the package path. Super geek powers!

    Usually used to populate services in a streamlit app.
   
    :return: True if success else False
    """

    assert isinstance(module_filepath, str)
    assert isinstance(package_path, str)
    assert os.path.isfile(os.path.abspath(module_filepath))
    assert os.path.isdir(os.path.abspath(package_path))

    # Loading by script module
    module_name = os.path.basename(
        os.path.abspath(module_filepath)).replace('.py', '')

    spec = importlib.util.spec_from_file_location(
        name=module_name,
        location=module_filepath,
        submodule_search_locations=[package_path]
    )

    try:
        module = importlib.util.module_from_spec(spec)
    except Exception as e:
        log.error(e)
        return False
    else:
        spec.loader.exec_module(module)
        # Optional; only necessary if you want to be able to import the module
        # by name later.
        sys.modules[module_name] = module
        return True

