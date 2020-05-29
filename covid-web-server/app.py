# Created by Zahorack
# 1.5.2020

from threading import Thread
from flask import Flask, render_template,session, request
from interfaces import SocketCommunication, Database
from flask_socketio import SocketIO, emit, disconnect
import time, datetime
import json
import os
import socket



from OpenSSL import SSL
# context = SSL.Context(SSL.TLSv1_2_METHOD)
# context.use_privatekey_file('example.key')
# context.use_certificate_file('example.crt')

app = Flask(__name__)

socketio = SocketIO(app, async_mode=None)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/covid')
def covid():
    return render_template('covid.html')

@app.route('/covid-graph')
def covid_graph():
    return render_template('covid-graph.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/design1')
def design1():
    return render_template('design1.html')

@app.route('/design2')
def design2():
    return render_template('design2.html')


@app.route('/design3')
def design3():
    return render_template('design3.html')


@app.route('/database/<table>', methods=['GET', 'POST'])
def database(table):
    tb = Database.Table()
    print(str(table))
    if tb.initialise(str(table)):
        # data = tb.selectWhere("datum", datetime.datetime.today().utcnow().date())
        data = tb.selectColumn("data")
        my_string = ','.join(map(str, data))

        return str("["+my_string+"]")

    return  "Database does not exist"


@app.route('/database/<table>/<date>', methods=['GET', 'POST'])
def database_by_date(table, date):
    tb = Database.Table()
    print(str(table))
    if tb.initialise(str(table)):
        print(date)
        # data = tb.selectWhere("datum", datetime.datetime.today().utcnow().date())
        if date == 'today':
            date = datetime.datetime.today().utcnow().date()
        data = tb.selectColumnWhere("data", "datum", date)
        print(data)
        my_string = ','.join(map(str, data))

        return str("["+my_string+"]")

    return  "Database does not exist"

@app.route('/tables', methods=['GET', 'POST'])
def select_tables():
    db = Database.Database()
    print("web request for tables")
    tables = db.tables()
    print(tables)
    #
    return json.dumps(tables)

@app.route('/dates/<table>', methods=['GET', 'POST'])
def select_dates(table):
    tb = Database.Table()
    print(str(table))
    if tb.initialise(str(table)):
        # data = tb.selectWhere("datum", datetime.datetime.today().utcnow().date())
        dates = tb.selectColumn("datum")
        dates = list(dict.fromkeys(dates))

        result = []
        for date in dates:
            result.append(str(date))

        print(dates)
        # my_string = ','.join(map(str, data))

        return json.dumps(result)

    return  "Database does not exist"


if __name__ == '__main__':

    com = SocketCommunication.SocketCommunication()
    com_thread = Thread(target=com.update, args=())
    com_thread.start()


    # socketio.run(app, host="0.0.0.0", port=80, debug=True)
    app.run(host="0.0.0.0", port=80, debug=True, ssl_context=("example.crt", "example.key"))
    # thread.start_new_thread(app.run, ("0.0.0.0", 80))

    # com_thread.join()




