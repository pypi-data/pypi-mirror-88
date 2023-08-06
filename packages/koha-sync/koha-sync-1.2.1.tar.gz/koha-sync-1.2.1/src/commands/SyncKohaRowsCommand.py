from diskcache import Cache
from loguru import logger
from tqdm import tqdm

import pprint
import time
import requests
import sys

from src.commands.BaseCommand import BaseCommand
from src.commands.LoadConfigFileCommand import LoadConfigFileCommand
from src.core import SqlSentences
from src.core.DBPool import DBPool
from src.core.Config import Config
from src.utils.FakeHeaders import FakeHeaders
from src.utils.CacheManager import CacheManager


class SyncKohaRowsCommand(BaseCommand):

    def __init__(self):
        self.add = 'api/koha'
        self.cacheManager = CacheManager()

    def execute(self):
        logger.info("STARTING SYNCHRONIZATION LOOP")
        last_record = LoadConfigFileCommand.get_last_record()

        if Config.source == 'db':
            logger.success("Synchronizing from DB")
            updated_last_record = self.sync_from_db(last_record)

        if Config.source == 'koha_api':
            logger.success("Synchronizing from KOHA_API")
            updated_last_record = self.sync_from_api(last_record)

        # write last synchronized record
        LoadConfigFileCommand.set_last_record(updated_last_record)
        logger.success(f"Koha records synchronized")

    """ lower case and remove noise characters """
    @staticmethod
    def sanitize(value):
        chars_to_remove = [';', ':', '/', '.', ',', '(', ')', '-', '_']
        if isinstance(value, str):
            value = value.lower()
            value = value.translate({ord(char): '' for char in chars_to_remove})
            value = ' '.join(value.split())
        return value

    def sync_from_db(self, last_record):
        try:
            with DBPool.get_connection(True).cursor() as cursor:

                cursor.execute(SqlSentences.get_sql_sentence(Config.config["target"]["account_id"], last_record,
                                                             Config.config["target"]["block"]))
                records = cursor.fetchall()

                if not records:
                    SyncKohaRowsCommand.bypass()
                    return

                self.persist(records)

                # last synchronized record date without timezone
                return records[-1]['tr_datetime'].split("+")[0]

        except Exception as e:
            logger.exception(e)
            sys.exit(logger.error(f"There was an error while synchronizing records : {e.args}"))

    def sync_from_api(self, last_record):
        headers = {
            'User-Agent': FakeHeaders.user_agent_list[0]
        }

        try:
            response = requests.get(Config.config[Config.source]['url'], headers=headers)
        except Exception as e:
            sys.exit(logger.error(f"There was an error for {Config.source} sync request  : {e.args}"))

        if response.status_code is not 200:
            sys.exit(logger.error(f"API {Config.config[Config.source]['url']} status code {response.status_code}"))

        else:
            logger.success(f"{Config.source} request successfully")
            records = response.json()

        if not records:
            SyncKohaRowsCommand.bypass()
            return

        self.persist(records, use_cache=True)

        # last synchronized record date without timezone
        return records[-1]['tr_datetime'].split("+")[0]

    def persist(self, records, use_cache=False):
        # use cache when the request's results are overlapped
        if use_cache:

            # perform a difference
            new_records = [api for api in records if api not in self.cacheManager.records]
            logger.info(f"{len(new_records)} new transactions found")

            # save last synchronized records and set what we are going to persist
            self.cacheManager.set_cache(records)
            records = new_records

        if not records:
            SyncKohaRowsCommand.bypass()
            return

        with tqdm(total=len(records), desc="SYNCHRONIZING ROWS") as progress_bar:
            for record in records:
                progress_bar.update(1)
                for key in record:
                    if key != "tr_datetime":
                        record[key] = SyncKohaRowsCommand.sanitize(record[key])
                    if key == "tr_value":
                        record[key] = int(record[key])

        post_rows_req = requests.post(f"{Config.config['target']['url_add']}/{self.add}",
                                      json={
                                          "llave": Config.config['target']['key'],
                                          "secreto": Config.config['target']['secret'],
                                          "docs": records
                                      })

        if post_rows_req.status_code is not 200:
            logger.warning(f"Request status was not 200 : {post_rows_req}")

    @staticmethod
    def bypass():
        logger.info("There aren't new records to synchronize. Bypassing excecution")
        time.sleep(5)
