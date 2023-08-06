import requests
from typing import Dict

import logging

logger = logging.getLogger()


class XmrigClient:
    def __init__(self, base_url, token) -> None:
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {token}",
            }
        )
        self.base_url = base_url

    def get_config(self) -> Dict:
        response = self._session.get(f"{self.base_url}/2/config")
        logger.debug(response)
        return response.json()

    def set_config(self, config: Dict):
        response = self._session.put(f"{self.base_url}/2/config", json=config)
        logger.debug(response)
