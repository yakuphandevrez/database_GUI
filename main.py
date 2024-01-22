import tkinter as tk
from tkinter import ttk
from colorama import init, Fore, Style
import mysql.connector

init(autoreset=True)

connection_info = {
    "host": "localhost",
    "user": "root",
    "password": "root1234",
    "database": "lovoo"
}

def get_connection():
    try:
        connection = mysql.connector.connect(**connection_info)
        return connection
    except Exception as e:
        print(f"Hata: {e}")
        return None

def select_from_table(table_name):
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        else:
            print("MySQL bağlantısı başarısız.")
            return None
    except Exception as e:
        print(f"Hata: {e}")
        return None

def insert_into_table(table_name, columns, values):
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            print(f"{table_name} tablosuna veri eklendi.")
        else:
            print("MySQL bağlantısı başarısız.")
    except Exception as e:
        print(f"Hata: {e}")

def delete_from_table(table_name, condition_column, condition_value):
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            query = f"DELETE FROM {table_name} WHERE {condition_column} = %s"
            values = (condition_value,)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            print(f"{table_name} tablosundan veri silindi.")
        else:
            print("MySQL bağlantısı başarısız.")
    except Exception as e:
        print(f"Hata: {e}")

def update_table(table_name, column_name, new_value, condition_column, condition_value):
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            query = f"UPDATE {table_name} SET {column_name} = %s WHERE {condition_column} = %s"
            values = (new_value, condition_value)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            print(f"{table_name} tablosu güncellendi.")
        else:
            print("MySQL bağlantısı başarısız.")
    except Exception as e:
        print(f"Hata: {e}")

def on_select():
    selected_table = combo_table.get()
    result = select_from_table(selected_table)
    if result is not None:
        text_result.config(state=tk.NORMAL)
        text_result.delete(1.0, tk.END)
        for row in result:
            text_result.insert(tk.END, f"{row}\n")
        text_result.config(state=tk.DISABLED)

def on_insert():
    table_name = combo_table.get()
    columns = entry_insert_columns.get()
    values = entry_insert_values.get()
    insert_into_table(table_name, columns, values)

def on_delete():
    table_name = combo_table.get()
    condition_column = entry_delete_column.get()
    condition_value = entry_delete_value.get()
    delete_from_table(table_name, condition_column, condition_value)

def on_update():
    table_name = combo_table.get()
    column_name = entry_update_column.get()
    new_value = entry_update_new_value.get()
    condition_column = entry_update_condition_column.get()
    condition_value = entry_update_condition_value.get()
    update_table(table_name, column_name, new_value, condition_column, condition_value)

root = tk.Tk()
root.title("Veritabanı Uygulaması")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_table = ttk.Label(frame, text="Tablo:")
label_table.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)

tables = ["tablo1", "tablo2", "tablo3"]
combo_table = ttk.Combobox(frame, values=tables)
combo_table.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)

button_select = ttk.Button(frame, text="SEÇ", command=on_select)
button_select.grid(row=0, column=2, pady=5, padx=5, sticky=tk.W)

text_result = tk.Text(frame, height=10, width=40, state=tk.DISABLED)
text_result.grid(row=1, column=0, columnspan=3, pady=5, padx=5, sticky=tk.W)

# INSERT
label_insert = ttk.Label(frame, text="Insert:")
label_insert.grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)

entry_insert_columns = ttk.Entry(frame)
entry_insert_columns.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
entry_insert_columns.insert(0, "sütun1, sütun2")

entry_insert_values = ttk.Entry(frame)
entry_insert_values.grid(row=2, column=2, pady=5, padx=5, sticky=tk.W)
entry_insert_values.insert(0, "değer1, değer2")

button_insert = ttk.Button(frame, text="EKLE", command=on_insert)
button_insert.grid(row=2, column=3, pady=5, padx=5, sticky=tk.W)

# DELETE
label_delete = ttk.Label(frame, text="Delete:")
label_delete.grid(row=3, column=0, pady=5, padx=5, sticky=tk.W)

entry_delete_column = ttk.Entry(frame)
entry_delete_column.grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)
entry_delete_column.insert(0, "sütun_adı")

entry_delete_value = ttk.Entry(frame)
entry_delete_value.grid(row=3, column=2, pady=5, padx=5, sticky=tk.W)
entry_delete_value.insert(0, "değer")

button_delete = ttk.Button(frame, text="SİL", command=on_delete)
button_delete.grid(row=3, column=3, pady=5, padx=5, sticky=tk.W)

# UPDATE
label_update = ttk.Label(frame, text="Update:")
label_update.grid(row=4, column=0, pady=5, padx=5, sticky=tk.W)

entry_update_column = ttk.Entry(frame)
entry_update_column.grid(row=4, column=1, pady=5, padx=5, sticky=tk.W)
entry_update_column.insert(0, "güncellenecek_sütun")

entry_update_new_value = ttk.Entry(frame)
entry_update_new_value.grid(row=4, column=2, pady=5, padx=5, sticky=tk.W)
entry_update_new_value.insert(0, "yeni_değer")

entry_update_condition_column = ttk.Entry(frame)
entry_update_condition_column.grid(row=4, column=3, pady=5, padx=5, sticky=tk.W)
entry_update_condition_column.insert(0, "koşul_sütun")

entry_update_condition_value = ttk.Entry(frame)
entry_update_condition_value.grid(row=4, column=4, pady=5, padx=5, sticky=tk.W)
entry_update_condition_value.insert(0, "koşul_değer")

button_update = ttk.Button(frame, text="GÜNCELLE", command=on_update)
button_update.grid(row=4, column=5, pady=5, padx=5, sticky=tk.W)

root.mainloop()