import pprint

import pymysql
from loguru import logger

from src.core.Config import Config

import time


class DBPool:

    @staticmethod
    def get_connection(insist=False):

        while True:
            try:
                db = pymysql.connect(db=Config.config['db']['schema'], user=Config.config['db']['user'],
                                     password=Config.config['db']['password'], host=Config.config['db']['host'],
                                     port=Config.config['db']['port'], cursorclass=pymysql.cursors.DictCursor)

                logger.success(f"Getting new connection from pool : insist -> {insist}")
                return db
            except Exception as e:
                fail = True
                logger.error(f"Koha Database connection failed : {e.args}")
                time.sleep(5)

            if not insist:
                if fail:
                    return None
                break
