import os
from pathlib import Path

import pkg_resources
from pkg_resources import DistInfoDistribution, VersionConflict
from loguru import logger
from .BaseCommand import BaseCommand


class ValidateRequirementsCommand(BaseCommand):

    _REQUIREMENTS_PATH = os.getcwd().join('../requirements.txt')

    def execute(self):
        logger.info("VERIFYING REQUIREMENTS")

        requirements = pkg_resources.parse_requirements(ValidateRequirementsCommand._REQUIREMENTS_PATH.open())
        for requirement in requirements:
            requirement = str(requirement)
            with self.subTest(requirement=requirement):
                pkg_resources.require(requirement)
