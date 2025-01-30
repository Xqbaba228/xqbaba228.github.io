from random import randint, shuffle
from flask import Flask, session, request, redirect, url_for, render_template
import os
from dwarf_unit_roster import get_data

# Функція отримує список рядків з таблиці бази даних і формує форму з таблицею
def data_form(sort_column=None, sort_order='asc'):
  data_list = get_data(sort_column, sort_order)
  return render_template('dawi_unit_roster.html', data_list=data_list)


# Функція view для стартової сторінки
def index():
    if request.method == 'GET':
      return data_form()
    else:
      # отримує значення стовпця, за яким потрібно сортувати. Це значення передається як приховане поле 
      # форми (<input type="hidden" name="column" value="{{ i }}">), де i є індексом стовпця
      column = request.form.get('column')
      # перевіряє, яка кнопка була натиснута: для сортування за зростанням чи за спаданням. 
      # Якщо натиснуто кнопку для зростання (sort_asc), значення буде 'asc', інакше — 'desc'.
      order = 'asc' if 'sort_asc' in request.form else 'desc'

      # Якщо стовпець для сортування вказаний, функція передає його значення та порядок сортування (asc або desc) у функцію data_form. 
      # Там уже можна обробляти ці параметри для виконання сортування
      if column is not None:
          return data_form(sort_column=int(column), sort_order=order)
      # Якщо стовпець не вказаний (наприклад, помилка або непередбачувана дія), просто показується таблиця без сортування
      else:
          return data_form()
        


folder = os.getcwd()  # Запам'ятали поточну робочу папку
# Створюємо об'єкт веб-програми:
app = Flask(__name__, template_folder=folder, static_folder=folder)
app.add_url_rule('/', 'index', index, methods=['post', 'get'])  # Створює правило для URL '/'

# Встановлюємо ключ шифрування:
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

if __name__ == '__main__':
    # Запускаємо веб-сервер:
    app.run()