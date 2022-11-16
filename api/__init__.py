from flask import Flask

from FashionCampus.common import hello

app = Flask(__name__)

@app.route('/')
def main():
    return {'message': hello()}, 200
