from argparse import ArgumentParser
from datetime import date, timedelta, datetime
import requests
from matpot import plot_data
from btc_api import BtcApi
from data_storage import DataStorage
import maya


class Connection:
    def load_min_api_data(self, start: date, end: date):
        end_min_1_day = str((maya.parse(end).datetime().date() - timedelta(days=1)))
        btc = BtcApi(n)
        table = DataStorage()
        table_load = table.loading_from_a_table(start, end)
        if table_load == {}:
            print('Недостаточно данных. Выполняю запрос к API')
            table.save_in_table(btc.get_by_time_interval(start, end))
        else:
            if start not in table_load:
                table.save_in_table(btc.get_by_time_interval(start, min(table_load)))
                table_load = table.loading_from_a_table(start, end)
            if end_min_1_day not in table_load:
                table.save_in_table(btc.get_by_time_interval(max(table_load), end))
                table_load = table.loading_from_a_table(start, end)
            if len(table_load) < end_min_1_day:
                def minimazer():
                    st = start
                    tmp_start = []
                    tmp_end = []
                    while maya.parse(st).datetime() + timedelta(days=1) < maya.parse(end).datetime():
                        if st in list(table_load) and str(maya.parse(st).datetime().date() + timedelta(days=1)) not in list(
                                        table_load):
                            tmp_start.append(str(maya.parse(st).datetime().date() + timedelta(days=1)))
                        if st not in list(table_load) and str(maya.parse(st).datetime().date() + timedelta(days=1)) in list(
                                        table_load):
                            tmp_end.append(str(maya.parse(st).datetime().date() + timedelta(days=1)))
                        st = str(maya.parse(st).datetime().date() + timedelta(days=1))
                    print(tmp_start)
                    print(tmp_end)
                    if len(tmp_start) == len(tmp_end):
                        for i in range(len(tmp_start)):
                            table.save_in_table(btc.get_by_time_interval(tmp_start[i], tmp_end[i]))
                minimazer()
        plot_data(table.loading_from_a_table(start, end))
        
    def load_min_requests(self, start: date, end: date):
        btc = BtcApi(n)
        table = DataStorage()
        table_load = table.loading_from_a_table(start, end)
        if table_load == {} or len(table_load) < (maya.parse(end).datetime().date()-maya.parse(start).datetime().date()).days:
            print('Недостаточно данных. Выполняю запрос к API')
            table.save_in_table(btc.get_by_time_interval(start, end))
        plot_data(table.loading_from_a_table(start, end))

    def load(self, start: date, end: date):
        if maya.parse(start).datetime().date() < maya.parse(find_first_valid_day()).datetime().date():
            print('Невозможно получить данные. Дата должна быть больше', find_first_valid_day())
            return
        if maya.parse(start).datetime().date() > maya.parse(end).datetime().date():
            start, end = end, start
        if maya.parse(end).datetime().date() > datetime.now().date():
            print('Невозможно получить данные. Дата должна быть меньше', str(datetime.now().date()))
            return
        if mr and not mapi:
            return self.load_min_requests(start, end)
        elif mapi and not mr:
            return self.load_min_api_data(start, end)
        else:
            return self.load_min_api_data(start, end)


def find_first_valid_day():
    #ToDo
    responce = requests.get(
        'https://api.coindesk.com/v1/bpi/historical/close.json',
        params={'start': "2000-09-11", 'end': "2000-09-11"}
    )
    resp = responce.content
    resp = str(resp).split()
    for elem in resp:
        if elem.startswith('2'):
            return elem


def parser_args():
    parser = ArgumentParser()
    parser.add_argument("--start", help="start date yyyy-mm-dd")
    parser.add_argument("--end", help="end date yyyy-mm-dd")
    parser.add_argument("--n", default=30, help="number of days, n<=100")
    parser.add_argument("--mr", default=False, help="min requests")
    parser.add_argument("--mapi", default=False, help="min api data")
    args = parser.parse_args()
    start, end, n, mr, mapi = args.start, args.end, args.n, args.mr, args.mapi
    return str(start), str(end), int(n), mr, mapi


start, end, n, mr, mapi = parser_args()
con = Connection()
con.load(start, end)
