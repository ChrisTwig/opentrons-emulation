import argparse
from emulation_system.settings_models import ConfigurationSettings
from emulation_system.parsers.abstract_parser import AbstractParser


class RepoParser(AbstractParser):
    """Parser for aws-ecr sub-command"""

    @classmethod
    def get_parser(
        cls, parser: argparse.ArgumentParser, settings: ConfigurationSettings
    ) -> None:
        """Build parser for aws-ecr command"""
        pass