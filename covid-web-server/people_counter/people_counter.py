# Created by Zahorack
# 1.5.2020

from datetime import datetime
from interfaces import Database


class PeopleCounter(object):
    def __init__(self):
        self.id = 0
        self.datetime = ''
        self.counter = 0

        self.database = Database.Database()








