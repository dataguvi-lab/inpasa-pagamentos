import os
import appconfig as cfg
import pandas as pd
import logging
import json
from dotenv import load_dotenv
from conn_pstg import start_connection_datalake, start_connection_datatalk
import pytz
from datetime import datetime


load_dotenv()
logger = logging.getLogger(cfg.APP_NAME)

class DataWrapper:

    @staticmethod
    def get_reports_pagamentos():
        conn = start_connection_datalake()           
        df = pd.read_sql_query(cfg.QUERY_PAGAMENTO, conn)
        df = pd.DataFrame(df)
        return df
