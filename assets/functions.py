import pandas as pd
import os
from datetime import datetime


def get_data():
    table = pd.read_csv('data-demo/data_template.csv', sep=';')
    table_filtered = table[table['status'] == 0]
    dataset = table_filtered.to_dict(orient="records")
    columns = table_filtered.columns.tolist()  # List of column names
    return columns, dataset

def insert_data(texto, deadline):
    """
    Adiciona uma nova linha com o texto e a data de entrega no arquivo CSV

    Args:
        texto (str): O texto a ser inserido.
        deadline (str): A data limite, se espera no formado DD/MM/YYYY.
    """
    file_path = 'data-demo/data_template.csv'

    if os.path.exists(file_path):
        # Load the existing file into a DataFrame
        df = pd.read_csv(file_path, sep=';')
        # Get the next ID
        new_id = df['id'].max() + 1
    else:
        # Create a new DataFrame if the file doesn't exist
        df = pd.DataFrame(columns=['id', 'status', 'text', 'date_created', 'deadline'])
        new_id = 0

    # Append the new row
    date_now = datetime.today().strftime('%Y-%m-%d')
    new_row = {'id': new_id, 'status': 0, 'text': texto, 'date_created': date_now, 'deadline': deadline}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    df.to_csv(file_path, sep=';', index=False)


def delete_data(row_id):
    """
    Remove uma linha no arquivo CSV

    Args:
        row_id (str): O id da linha a ser deletada.
    """
    file_path = 'data-demo/data_template.csv'
    
    # Lê o DataFrame e remove uma linha da planilha
    df = pd.read_csv(file_path, sep=';')
    df = df[df["id"] != row_id]
    df.to_csv(file_path, sep=';', index=False)

def change_status(row_id):
    file_path = 'data-demo/data_template.csv'