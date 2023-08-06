from dataclasses import dataclass


@dataclass(init=True, repr=True)
class DataLineage():
    """Class for keeping track of secrets
    """
    metadata: dict()
    


