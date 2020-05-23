# Created by Zahorack
# 1.5.2020

import mysql.connector
from private import access

database= mysql.connector.connect(
    host = access.database_host,
    user = access.database_user,
    passwd = access.database_password,
    database = access.database_name
)


class Database(object):
    def __init__(self):
        self.cursor = database.cursor()

        print("SHOW TABLES")
        self.cursor.execute("SHOW TABLES")
        for x in self.cursor:
            print(x)

    def createClientTable(self, name):
        self.cursor.execute("CREATE TABLE %s (id INT AUTO_INCREMENT PRIMARY KEY, date DATE, time TIME, people_counter_data VARCHAR(255))")


    def insetInto(self, table, column, data):
        self.cursor = database.cursor()

        self.cursor.execute("INSERT INTO {table_name} ({column_name}) VALUES (%s);".format(table_name=table, column_name=column), (data.encode("utf-8"),))
        database.commit()


    def tables(self):
        self.cursor.execute("SHOW TABLES")

        tables = []
        for x in self.cursor:
            tables.append(str(x[0]))

        return tables

    def createTable(self, table):

        if table in self.tables():
            print("Table "+table+" already exist")
        else :
            self.cursor.execute("CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY)".format(table_name=table))


    def columns(self, table):

        self.cursor.execute("SHOW COLUMNS FROM {table_name};".format(table_name =table))

        columns = []
        for x in  self.cursor:
            columns.append(str(x[0]))

        return  columns


    def addColumn(self, table, name, type):
        print(self.columns(table))

        if name in self.columns(table):
            print("Column "+name+" already in table")
        else:
            print("Add column "+name+" to table "+table)
            self.cursor.execute("ALTER TABLE {table_name} ADD COLUMN {column_name} {datatype};".format(table_name=table, column_name=name, datatype=type))