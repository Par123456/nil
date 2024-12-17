import requests
from uuid import uuid4
from typing import Dict, Optional
import random
from config import Config
from utils import encode_data

class ApiClient:
    def __init__(self, restore_key: str):
        self.restore_key = restore_key
        self.base_url = Config.API_ENDPOINTS['base']
        self.session = requests.Session()
        self._update_headers()

    def _update_headers(self):
        self.session.headers.update({
            'User-Agent': random.choice(Config.USER_AGENTS),
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

    def initialize(self) -> Dict:
        data = {
            'game_version': '1.7.10655',
            'device_name': 'unknown',
            'os_version': '10',
            'model': 'SM-A750F',
            'udid': str(uuid4()),
            'store_type': 'iraqapps',
            'restore_key': self.restore_key,
            'os_type': 2
        }

        return self.post('player/load', data)

    def post(self, endpoint: str, data: Dict) -> Dict:
        try:
            response = self.session.post(
                f'{self.base_url}{endpoint}',
                data=encode_data(data),
                timeout=5
            )
            return response.json()
        except requests.exceptions.RequestException:
            self._toggle_base_url()
            return self.post(endpoint, data)

    def _toggle_base_url(self):
        self.base_url = (
            Config.API_ENDPOINTS['secure_base']
            if self.base_url == Config.API_ENDPOINTS['base']
            else Config.API_ENDPOINTS['base']
        )

    def get_opponents(self) -> List[Dict]:
        try:
            response = self.session.get(
                f'{self.base_url}battle/getopponents',
                timeout=5
            )
            return response.json()['data']['players']
        except Exception as e:
            print(f"Failed to get opponents: {e}")
            return []