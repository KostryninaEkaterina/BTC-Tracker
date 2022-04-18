import json
import requests
from datetime import timedelta, date
import maya


class BtcApi:
    _base_url = 'https://api.coindesk.com/v1/bpi/historical/close.json'
    _days_step = 30

    def __init__(self, days_step: int = 100):
        self._days_step = days_step if days_step <= 100 else BtcApi._days_step

    def get_by_time_interval(self, start: date, end: date):
        data = dict()
        for k, v in self._generate_time_part(start, end).items():
            print(f'Make api request [{k}, {v}]')
            data.update(self._request(k, v))

        return data

    def _generate_time_part(self, start: date, end: date) -> dict:
        #Последняя дата не включается
        data_dict = {start: end}
        start = maya.parse(start).datetime().date()
        end = maya.parse(end).datetime().date()
        if start + timedelta(days=self._days_step) >= end:
            end -= timedelta(days=1)
            start, end = str(start), str(end)
            data_dict[start] = end
        else:
            while start < end:
                tmp_end = start + timedelta(days=self._days_step)
                start, tmp_end = str(start), str(tmp_end)
                data_dict[start] = tmp_end
                start = maya.parse(start).datetime().date()
                start += timedelta(days=self._days_step)
            if start >= end:
                start -= timedelta(days=self._days_step)
                end -= timedelta(days=1)
                start, end = str(start), str(end)
                data_dict[start] = end

        return data_dict

    def _make_request(self, start: date, end: date):
        responce = requests.get(
            BtcApi._base_url,
            params={'start': start, 'end': end}
        )
        return responce.content

    def _request(self, start: date, end: date):
        resp = json.loads(self._make_request(start, end))
        return resp['bpi']