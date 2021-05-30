from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/add_nums/<int:a_number>-<int:b_number>')
def addThem(a_number,b_number):
    return f'{a_number+b_number}'

if __name__ == '__main__':
    app.run()