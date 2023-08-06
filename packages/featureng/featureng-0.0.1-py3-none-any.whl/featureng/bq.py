
import pandas as pd
from google.cloud import bigquery

from . import exceptions

from typing import Union, List, Dict, Sequence

def get_client(client: Union[str, bigquery.client.Client] = None):
    if isinstance(client,bigquery.client.Client):
        return client
    elif isinstance(client,str):
        return bigquery.Client.from_service_account_json(client)
    else:
        return bigquery.Client()

def get_zip_population(zipcode: Union[str,Sequence[str]], client: Union[str, bigquery.client.Client] = None):
    client = get_client(client)
    client.query("""
        SELECT *
        FROM (
          SELECT 2018 year, total_pop
          FROM `bigquery-public-data`.census_bureau_acs.zip_codes_2018_5yr
          WHERE geo_id = "11377"
          UNION ALL
          SELECT 2017 year, total_pop
          FROM `bigquery-public-data`.census_bureau_acs.zip_codes_2017_5yr
          WHERE geo_id = "11377"
          UNION ALL
          SELECT 2016 year, total_pop
          FROM `bigquery-public-data`.census_bureau_acs.zip_codes_2016_5yr
          WHERE geo_id = "11377"
          UNION ALL
          SELECT 2015 year, total_pop
          FROM `bigquery-public-data`.census_bureau_acs.zip_codes_2015_5yr
          WHERE geo_id = "11377"
          UNION ALL
          SELECT 2014 year, total_pop
          FROM `bigquery-public-data`.census_bureau_acs.zip_codes_2014_5yr
          WHERE geo_id = "11377"
          UNION ALL
          SELECT 2013 year, total_pop
          FROM `bigquery-public-data`.census_bureau_acs.zip_codes_2013_5yr
          WHERE geo_id = "11377"
          UNION ALL
          SELECT 2012 year, total_pop
          FROM `bigquery-public-data`.census_bureau_acs.zip_codes_2012_5yr
          WHERE geo_id = "11377"
          UNION ALL
          SELECT 2011 year, total_pop
          FROM `bigquery-public-data`.census_bureau_acs.zip_codes_2011_5yr
          WHERE geo_id = "11377"
        ) multi_year
        ORDER BY year;
    """)
