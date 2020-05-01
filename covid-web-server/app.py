from xdrlib import Packer
from flask import Flask, render_template, session, request, jsonify, url_for
import SocketCommunication
import thread


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/design1')
def design1():
    return render_template('design1.html')

@app.route('/design2')
def design2():
    return render_template('design2.html')


@app.route('/design3')
def design3():
    return render_template('design3.html')


if __name__ == '__main__':
    com = SocketCommunication.SocketCommunication()
    # thread.start_new_thread(com.update, ())
    com.update()

    # app.run(host="0.0.0.0", port=80, debug=True)
    # thread.start_new_thread(app.run, ("0.0.0.0", 80, True))




