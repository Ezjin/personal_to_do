from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from assets.functions import get_data, insert_data, delete_data
from datetime import datetime

app = Flask(__name__)

dataframe = None
data_file = "data-demo/data_template.csv"  # Path to your CSV file


def load_data():
    """Load the CSV file into the global DataFrame."""
    global dataframe
    dataframe = pd.read_csv(data_file, sep=";")


def save_data():
    """Save the global DataFrame back to the CSV file."""
    global dataframe
    dataframe.to_csv(data_file, index=False, sep=";")

with app.app_context():
    """Load the data when the app starts."""
    load_data()

@app.route('/')
def main_page():
    global dataframe
    columns = list(dataframe.columns)
    dataset = dataframe.to_dict(orient="records")
    return render_template("index.html", title="To-Do Pessoal", dataset=dataset, columns=columns)

@app.route('/add', methods=['GET', 'POST'])
def add_data():
    global dataframe
    if request.method == 'POST':
        texto = request.form.get('text')
        deadline = request.form.get('deadline')
        
        # Add a new row to the DataFrame
        date_now = datetime.today().strftime('%Y-%m-%d')
        new_id = dataframe['id'].max() + 1 if not dataframe.empty else 1
        new_row = {'id': new_id, 'status': 0, 'text': texto, 'date_created': date_now, 'deadline': deadline}
        dataframe = pd.concat([dataframe, pd.DataFrame([new_row])], ignore_index=True)

        # Save changes to the file
        save_data()
        return redirect(url_for('main_page'))
    return render_template("add.html", title="Add Data")

@app.route('/delete/<int:row_id>', methods=['POST'])
def delete_row(row_id):
    global dataframe

    dataframe = dataframe[dataframe['id'] != row_id]

    # Save changes to the file
    save_data()
    
    return redirect(url_for('main_page'))

if __name__ == '__main__':
    app.run(debug=True)