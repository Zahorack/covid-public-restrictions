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

    def commit(self):
        database.commit()

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


    def selectTable(self, table):
        print("Select from " + table)
        sql = "SELECT * FROM {table_name}".format(table_name=table)

        self.cursor.execute(sql)
        myresult = self.cursor.fetchall()

        # for x in myresult:
        #     print(x)

        return myresult


class Table(object):
    def __init__(self):
        self.db = Database()
        self.cursor = self.db.cursor
        self.name = str()
        self.id = 0


    def getId(self):
        self.cursor.execute("SELECT MAX(id) FROM {table_name}".format(table_name=self.name))

        self.id = self.cursor.fetchall()[0]

        return self.id


    def exist(self):
        if self.name in self.db.tables():
            return True
        return False

    def create(self, name):
        self.name = str(name)

        if self.name in self.db.tables():
            print("Table " + self.name + " already exist")
        else:
            self.cursor.execute(
                "CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY)".format(table_name=self.name))

        self.columns = self.db.columns(self.name)


    def initialise(self, name):
        self.name = str(name)

        if self.exist():
            self.columns = self.db.columns(self.name)
            return True

        return False


    def insetInto(self, column, data):
        self.cursor.execute(
            "INSERT INTO {table_name} ({column_name}) VALUES (%s);".format(table_name=self.name, column_name=column),
            (data.encode("utf-8"),))

        self.db.commit()

    def inset(self, columns, data):

        self.cursor.execute("INSERT INTO {table_name} ({column_name}) VALUES (%s,%s,%s);".format\
                                (table_name=str(self.name), column_name=str(columns)), (data[0], data[1], data[2]))
        self.db.commit()


    def addColumn(self, name, type):
        print(self.db.columns(self.name))

        if name in self.db.columns(self.name):
            print("Column "+name+" already in table")
        else:
            print("Add column "+name+" to table "+self.name)
            self.cursor.execute("ALTER TABLE {table_name} ADD COLUMN {column_name} {datatype};".format(table_name=self.name, column_name=name, datatype=type))

        self.columns = self.db.columns(self.name)


    def select(self):
        sql = "SELECT * FROM {table_name}".format(table_name=self.name)
        print(sql)
        self.cursor.execute(sql)
        myresult = self.cursor.fetchall()
        # for x in myresult:
        #     print(x)
        return myresult


    def selectColumn(self, column):
        sql = "SELECT {column_name} FROM {table_name}".format(table_name=self.name, column_name=column)
        print(sql)
        self.cursor.execute(sql)

        myresult = self.cursor.fetchall()
        # for x in myresult:
        #     print(x)
        return  myresult

    def selectWhere(self, column, item):
        sql = "SELECT * FROM {table_name} WHERE {column_name} = '{item_name}'".format(table_name=self.name, column_name=column, item_name=item)
        print(sql)
        self.cursor.execute(sql)

        myresult = self.cursor.fetchall()
        # for x in myresult:
        #     print(x)
        return  myresult