# Created by Zahorack
# 1.5.2020

from datetime import datetime
from interfaces import Database
import json
import time, os
from private import clients

os.environ['TZ'] = 'Europe/Bratislava'
time.tzset()

class PeopleCounter(object):
    def __init__(self):
        self.id = 0
        self.datetime = ''

        self.counter = 0
        self.name = None

        self.table = Database.Table()


    def initializeDatabase(self):
        self.table.create(self.name)

        if self.table.exist():
            self.table.addColumn("datum", "DATE")
            self.table.addColumn("cas", "TIME")
            self.table.addColumn("data", "VARCHAR(255)")


    def update(self, data):
        jsonData = json.loads(data)
        print(jsonData["name"])

        if clients.hasValidKey(jsonData["name"], jsonData["key"]):

            if not self.name:
                self.name = str(jsonData["name"])
                self.initializeDatabase()
            else:
                # self.table.insetInto("data", str(jsonData["counter"]))
                # self.table.insetInto("datum", str(time.strftime('%Y-%m-%d')))
                # self.table.insetInto("cas", str(time.strftime('%H:%M:%S')))

                columns = str("datum, cas, data")
                data = json.dumps({"date": str(time.strftime('%Y-%m-%d')), "time":str(time.strftime('%H:%M:%S')), "counter": str(jsonData["counter"])})

                self.table.cursor.execute("INSERT INTO {table_name} ({column_name}) VALUES (%s,%s,%s);".format \
                                        (table_name=str(self.name), column_name=str(columns)), (time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S'), data))
                self.table.db.commit()











