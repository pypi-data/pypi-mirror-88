from loguru import logger

from src.commands.BaseCommand import BaseCommand
from src.core.Config import Config
from src.utils.FakeHeaders import FakeHeaders

import pprint
import requests
import sys


class ValidateApiCommand(BaseCommand):

    def __init__(self):
        self.add_koha = 'api/koha'
        self.headers = {
            "Accept": "application/json"
        }

    def execute(self):
        logger.info("VALIDATING API AVAILABILITY")

        # Lookproxy koha ingest api
        self.validate_api_call(f"{Config.config['target']['url_add']}/{self.add_koha}", "post", headers=self.headers)

        # Lookproxy koha data source api
        if Config.source == 'koha_api':
            self.headers['User-Agent'] = FakeHeaders.user_agent_list[0]
            self.validate_api_call(Config.config[Config.source]['url'], "get", headers=self.headers)

    def validate_api_call(self, uri, method, headers=None):
        method = getattr(requests, method)

        try:
            response = method(uri, headers=headers)
        except Exception as e:
            sys.exit(logger.error(f"There was an error for request  : {e.args}"))

        if response.status_code not in [401, 200]:
            sys.exit(logger.error(f"API {uri} status code {response.status_code}"))

        else:
            logger.success(f"API available")

