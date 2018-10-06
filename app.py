import os
from flask import Flask

app = Flask(__app__)

@app.route('/')
def hello():
    return 'Hello World! This is my Milestone 4 Project Kick-Start'

if __name__ == '__main__':
    app.run(host.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debig=True)