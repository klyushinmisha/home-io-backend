# this is example flask proj for team
# TODO: delete this

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

if __name__ == '__main__':
    app.debug = True
    app.run()
