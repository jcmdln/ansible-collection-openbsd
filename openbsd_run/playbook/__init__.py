import os as os
from typing import List


def Path() -> str:
    """
    Return the path of the playbook folder for easier access to files
    within it.
    """
    return os.path.dirname(os.path.abspath(__file__))


__all__: List[str] = ["Path"]
