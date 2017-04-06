import argparse
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Load the arguments of the program
    # Host and port where the service will be running
    parser = argparse.ArgumentParser(description='Text summarizer server')
    parser.add_argument('-ip', '--ip', help='Host where the service will be running', required=False, default='0.0.0.0')
    parser.add_argument('-p', '--port', help='Port where the service will be running', required=False, default=8080)
    args = vars(parser.parse_args())

    app.debug = True
    app.run(host=args['ip'], port=int(args['port']))
