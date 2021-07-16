# SPDX-License-Identifier: ISC

from __future__ import annotations

import os

path: str = os.path.dirname(os.path.abspath(__file__))

__all__: list[str] = ["path"]
