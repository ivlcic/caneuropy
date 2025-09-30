import logging
import os
from datetime import timedelta, datetime
from typing import TypeVar, Any, List, Dict, Tuple

import requests
from requests.auth import HTTPBasicAuth

TElasticQuery = TypeVar("TElasticQuery", bound="ElasticQuery")

logger = logging.getLogger('es-query')

class ElasticQuery:

    def __init__(self, url: str = None, user: str = None, passwd: str = None):
        self._user: str = user if user else os.environ.get('CPTM_SUSER', '')
        self._passwd: str = passwd if passwd else os.environ.get('CPTM_SPASS', '')
        self._url: str = url if url else os.environ.get('CPTM_SURL', 'http://localhost:9200')

        self.full_url = f"{self._url}?track_total_hits=true"
        self._limit = 10000
        self._offset = 0

    def limit(self, limit: int) -> TElasticQuery:
        self._limit = limit
        return self

    def offset(self, offset: int) -> TElasticQuery:
        self._offset = offset
        return self

    def query(self, query: str, start: datetime, end: datetime = None) -> Tuple[List[Dict[str, Any]], int]:
        if not end:
            end = start + timedelta(hours=24)
        query = query.replace('<from>', str(self._offset))
        query = query.replace('<size>', str(self._limit))
        query = query.replace('<date_start>', start.astimezone().isoformat())
        query = query.replace('<date_end>', end.astimezone().isoformat())

        # logger.debug("Executing raw query: [%s]", query)

        result = []
        resp = requests.post(
            self.full_url,
            headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth(self._user, self._passwd),
            data=query
        )

        if resp.status_code != 200:
            logger.error('Elasticsearch request failed with status [%s]: [%s]', resp.status_code, resp.text)
            return result, 0

        resp_data = resp.json()
        hits = resp_data.get('hits', {})
        for hit in hits.get('hits', []):
            result.append(hit['_source'])

        # logger.info("Raw query returned [%s] articles from [%s]", len(result), self.full_url)

        return result, hits.get('total', {}).get('value', 0)
