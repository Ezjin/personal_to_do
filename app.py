from flask import Flask, render_template
from assets.functions import get_data

app = Flask(__name__)

@app.route('/')
def hello_world():
    columns, dataset = get_data()
    return render_template("index.html", title="Hello", dataset=dataset, columns=columns)

if __name__ == '__main__':
    app.run(debug=True)