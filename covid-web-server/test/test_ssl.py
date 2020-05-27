from flask import Flask

app = Flask(__name__)
import ssl

@app.route('/')
def ping():
    return 'pong'


if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('ca-crt.pem')
    context.load_cert_chain('server.crt', 'server.key')
    app.run('0.0.0.0', 80, ssl_context='adhoc')