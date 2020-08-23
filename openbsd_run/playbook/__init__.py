import os as os
from typing import List


path: str = os.path.dirname(os.path.abspath(__file__))


__all__: List[str] = ["path"]
