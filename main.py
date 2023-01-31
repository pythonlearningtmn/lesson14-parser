import os.path
import json
from func_flask1 import new_parser1

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/contacts/')
def contacts():
    developer_name = 'Leo'
    # Контекст name=developer_name - те данные, которые мы передаем из view в шаблон
    # context = {'name': developer_name}
    # Словарь контекста context
    # return render_template('contacts.html', context=context)
    contxt = {'name': 'Сергей Шишов',
              'creation_date': '30-01-2023',
              'phone': '+7 (912) 391-44-23'
              }
    return render_template('contacts.html', **contxt)


@app.route('/results/')
def results():
    if os.path.exists('results.json'):
        with open('results.json', 'r') as f:
            text = json.load(f)
    else:
        text = ''
    return render_template('results.html', text=text)


@app.route('/run/', methods=['GET'])
def run_get():
    if os.path.exists('results.json'):
        with open('results.json', 'r') as f:
            text = json.load(f)
    else:
        text = ''
    return render_template('form.html', text=text)


@app.route('/run/', methods=['POST'])
def run_post():
    q = request.form['input_text']
    result = new_parser1(q)
    return render_template('results.html', text=result)


if __name__ == "__main__":
    app.run(debug=True)
