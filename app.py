from flask import Flask, render_template, request, redirect, url_for
from assets.functions import get_data, insert_data

app = Flask(__name__)

@app.route('/')
def main_page():
    columns, dataset = get_data()
    return render_template("index.html", title="Hello", dataset=dataset, columns=columns)

@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        text = request.form.get('text')
        deadline = request.form.get('deadline')
        insert_data(text, deadline)
        return redirect(url_for('main_page'))
    return render_template("add.html", title="Add Data")

if __name__ == '__main__':
    app.run(debug=True)