from typing import Any, Dict, List, Union
from pathlib import Path
from os.path import relpath
import re
import yaml
import json


class Includer:

    def __init__(self, include_regex: str, docs_folder: str, relative_path: bool):
        self.include_regex = include_regex
        self.docs_folder = docs_folder
        self.relative_path = relative_path

    def replace(self, data: Any):
        copied_data = data.copy()
        return self._recursive_replace(copied_data)

    def _recursive_replace(self, data: Any) -> Any:
        if isinstance(data, list):
            return [
                self._recursive_replace(item) for item in data
            ]
        elif isinstance(data, dict):
            return {
                key: self._recursive_replace(value)
                for key, value in data.items()
            }
        elif isinstance(data, str):
            regex = re.compile(self.include_regex)
            match = regex.match(data)
            if match:
                return self._include_from_str(match.group("path"))
            return data
        else:
            return data

    def _include_from_str(self, data: str) -> Any:
        path = Path(self.docs_folder, data)
        content = None
        file = open(path, "r")
        if path.suffix.lower() in [".yml", ".yaml"]:
            content = yaml.load(file, Loader=yaml.FullLoader)
        elif path.suffix.lower() in [".json"]:
            content = json.load(file)
        else:
            content = file.read()
        if self.relative_path:
            content = self._recursive_relative_path(content, path.parent)
        return content

    def _recursive_relative_path(self, data: Any, config_file_path: str):
        if isinstance(data, list):
            return [
                self._recursive_relative_path(item, config_file_path) for item in data
            ]
        elif isinstance(data, dict):
            return {
                key: self._recursive_relative_path(value, config_file_path)
                for key, value in data.items()
            }
        elif isinstance(data, str):
            path = relpath(Path(config_file_path, data), self.docs_folder)
            return str(path)
        else:
            return data
