from __future__ import annotations

from configparser import ConfigParser, ParsingError
from typing import Any

from yaml import YAMLError
from yaml import safe_load as yaml_load


def Read(filename: str) -> dict[Any, Any]:
    """
    Read an ini or yaml configuration file as a dictionary.
    """

    try:
        with open(filename, "r") as f:
            contents: str = f.read()
    except FileNotFoundError as e:
        raise e

    try:
        cfg: ConfigParser = ConfigParser(allow_no_value=True)
        cfg.read_string(contents)
        return {s: dict(cfg.items(s)) for s in cfg.sections()}
    except ParsingError:
        pass

    try:
        return yaml_load(contents)  # type: ignore
    except YAMLError:
        pass

    return {}
