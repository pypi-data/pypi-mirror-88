import logging
from datetime import datetime, timedelta

import requests

DEMO_TOKEN = ''
DEFAULT_TIMEOUT = 15

_LOGGER = logging.getLogger(__name__)


class Barry:

    def __init__(
            self,
            access_token=DEMO_TOKEN,
            timeout=DEFAULT_TIMEOUT,
    ):
        self.access_token = access_token
        self.timeout = timeout

    def update_price_data(self):
        current_time = datetime.now().replace(microsecond=0).isoformat() + 'Z'
        last_hour_date_time = (datetime.now() - timedelta(hours=1)).replace(microsecond=0).isoformat() + 'Z'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json',
        }

        data = '{ "jsonrpc": "2.0", "id": 0, "method": "co.getbarry.api.v1.OpenApiController.getPrice", "params": [ "DK_NORDPOOL_SPOT_DK1", "%s", "%s" ] }' % (
            last_hour_date_time, current_time)

        response = requests.post('https://jsonrpc.barry.energy/json-rpc', headers=headers, data=data)
        json_res = response.json()
        if json_res.get('result'):
            return json_res['result'][0]['value']
