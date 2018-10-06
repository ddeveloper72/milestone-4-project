import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World! This is my Milestone 4 Project Kick-Start'


if __name__ == '__main__':
    
    # assign a port ID works with Vscode
   
    app.run(host=os.getenv('IP'),
        port=os.getenv('PORT'),
        # debug set to true to help during development
        debug=True)

""" if __name__ == '__main__':

    # Cloud 9 Environmental variables

    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    # debug set to true to help during development
    debug=True) """