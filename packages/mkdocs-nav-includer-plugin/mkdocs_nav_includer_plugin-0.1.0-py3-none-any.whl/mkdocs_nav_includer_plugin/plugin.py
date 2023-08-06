from mkdocs_nav_includer_plugin.includer import Includer
from mkdocs.plugins import BasePlugin
from pathlib import Path
from mkdocs.structure.nav import Navigation
import logging
import mkdocs


logger = logging.getLogger("mkdocs")

class NavIncluderPlugin(BasePlugin):
    config_scheme = (
        ('include_regex', mkdocs.config.config_options.Type(str, default='@include (?P<path>.*)')),
        ('relative_path',  mkdocs.config.config_options.Type(bool, default=True))
    )
    def on_config(self, config, **kwargs):
        nav = config.get("nav", {})
        includer = Includer(
            include_regex=self.config["include_regex"],
            docs_folder=config["docs_dir"],
            relative_path=self.config["relative_path"],
        )
        config["nav"] = includer.replace(config.get("nav", {}))
        return config