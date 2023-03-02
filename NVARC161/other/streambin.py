from flask import Flask

NAME = "new.bin"
HOST = "localhost"
PORT = 8080

app = Flask(__name__)

@app.route("/")
def index():
    with open(NAME, "r") as f:
        return f.read()

app.run(host=HOST, port=PORT)