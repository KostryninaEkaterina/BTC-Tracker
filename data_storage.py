import sqlite3
from datetime import date


class DataStorage:
    _db_name: str = str()

    def __init__(self, db_name: str = 'btc_historical'):
        self._db_name = db_name
        self.connection = sqlite3.connect('btc')
        self.cursor = self.connection.cursor()

    def save_in_table(self, data: dict) -> None:
        self._make_table()
        insert = 'INSERT OR IGNORE INTO ' + self._db_name + '(date, price) VALUES(?,?)'
        for k, v in data.items():
            self.cursor.execute(
                insert,
                (k, v)
            )
        self.connection.commit()

    def loading_from_a_table(self, start: date, end: date):
        self._make_table()
        request = 'SELECT * FROM ' + self._db_name + ' WHERE date >= \"' + start + '\" AND date <= \"' + end + '\" ORDER BY date'
        print(request)
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        print(result)
        table_dict = {}
        for elem in result:
            k, v = elem[0], elem[1]
            table_dict[k] = v
        return table_dict

    def _make_table(self):
        cr_table = 'CREATE TABLE IF NOT EXISTS ' + self._db_name + '(date TEXT, price REAl, UNIQUE(date))'
        self.cursor.execute(cr_table)
        self.connection.commit()