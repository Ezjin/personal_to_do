from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from assets.functions import get_data, insert_data, delete_data
from datetime import datetime
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json
import bcrypt
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
from google_firestore import valida_login

#Importando variaveis de ambiente
load_dotenv()

file_path = os.getenv("file_path")

if not firebase_admin._apps:
    cred = credentials.Certificate(file_path)
    app_firebase = firebase_admin.initialize_app(cred)
    
store = firestore.client()

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

# Autenticacao de usuario --------------------------------------
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
  if valida_login(username, password):
    return username
  return None

with app.app_context():
    """Load the data when the app starts."""
    load_data()

@app.route('/')
@auth.login_required
def main_page():
    global dataframe
    if dataframe.empty:
        columns = ['id', 'status', 'text', 'date_created', 'deadline']  # Default column names
        data = [0, 0, "Adicione uma tarefa para começar", datetime.today().strftime('%Y-%m-%d'), datetime.today().strftime('%Y-%m-%d')]
        dataframe = pd.DataFrame([data], columns=columns)
        dataset = dataframe.to_dict(orient="records")
    else:
        dataframe = dataframe.sort_values(by=['status', 'date_created'], ascending=[True, False]).reset_index(drop=True)
        columns = list(dataframe.columns)
        dataset = dataframe.to_dict(orient="records")
    return render_template("index.html", title="To-Do Pessoal", dataset=dataset, columns=columns)

@app.route('/add', methods=['GET', 'POST'])
@auth.login_required
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
@auth.login_required
def delete_row(row_id):
    global dataframe

    dataframe = dataframe[dataframe['id'] != row_id]

    # Save changes to the file
    save_data()
    
    return redirect(url_for('main_page'))

@app.route('/toggle_status/<int:row_id>', methods=['POST'])
@auth.login_required
def toggle_status(row_id):
    global dataframe

    # Find the row and toggle the status
    dataframe.loc[dataframe['id'] == row_id, 'status'] = 1 - dataframe.loc[dataframe['id'] == row_id, 'status']

    # Save the changes to the file
    save_data()
    
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    app.run(debug=True)