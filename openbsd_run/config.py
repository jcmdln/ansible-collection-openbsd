from configparser import ConfigParser, ParsingError
from typing import Any, Dict
from yaml import safe_load as yaml_load, YAMLError


def Read(filename: str) -> Dict[Any, Any]:
    """
    Read an ini or yaml configuration file as a dict, returning an empty dict
    if the file could not be parsed as either format.
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
