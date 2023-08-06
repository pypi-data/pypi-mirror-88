import sys
from loguru import logger

from src.core.DBPool import DBPool
from src.commands.BaseCommand import BaseCommand


class ValidateKohaDBCommand(BaseCommand):

    def __init__(self):
        pass

    def execute(self):
        logger.info("VALIDATING KOHA DB CONNECTION")

        if not DBPool.get_connection(insist=False):
            sys.exit(0)

        logger.success("Connection established successfully")
