import matplotlib
matplotlib.use('TkAgg')

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# Определяем класс Employee 
class Employee:
    def __init__(self, fio, position, hire_date, salary):
        self.__fio = fio
        self.__position = position
        self.__hire_date = self.__parse_hire_date(hire_date) # Дата найма, преобразованная в формат datetime
        self.__salary = self.__validate_salary(salary) # Проверка и установка зарплаты

    def __parse_hire_date(self, hire_date):
        # Различные форматы для даты найма
        date_formats = ["%d.%m.%Y", "%m/%d/%Y"]
        for fmt in date_formats:
            try:
                return datetime.strptime(hire_date, fmt) # Преобразуем строку в дату
            except ValueError:
                continue # Попробуем следующий формат
        raise ValueError(f"Неверный формат даты: {hire_date}")

    def get_fio(self):
        return self.__fio

    def get_position(self):
        return self.__position

    def get_hire_date(self):
        return self.__hire_date

    def get_salary(self):
        return self.__salary 

    def set_salary(self, new_salary): # Установка новой зарплаты с проверкой
        self.__salary = self.__validate_salary(new_salary) 

    @staticmethod
    def __validate_salary(salary): # Проверка, что зарплата является числом (int или float)
        if isinstance(salary, (int, float)):
            return salary
        raise ValueError("Зарплата должна быть числом")

    def calculate_programmer_bonus(self, bonus_percent=0.03): # Расчет бонуса для программистов, если они попадают под условие
        if "программист" in self.__position.lower():
            return self.__salary * bonus_percent
        return 0

    def calculate_holiday_bonus(self, women_bonus=2000, men_bonus=2000): # Расчет праздничного бонуса в зависимости от пола сотрудника
        if self.__fio.split()[-1].endswith('а'):
            return women_bonus
        else:
            return men_bonus 

    def calculate_salary_indexation(self, over_10_years_index=0.07, under_10_years_index=0.05): # Индексация зарплаты в зависимости от стажа
        years_worked = (datetime.now() - self.__hire_date).days // 365
        if years_worked > 10:
            self.__salary += self.__salary * over_10_years_index
        else:
            self.__salary += self.__salary * under_10_years_index
        return self.__salary

    def is_eligible_for_vacation(self): # Проверка на право на отпуск по стажу
        months_worked = (datetime.now() - self.__hire_date).days // 30
        return months_worked > 6

# Функция для загрузки данных сотрудников из CSV и создания объектов Employee
def load_employees_from_csv(file_path):
    df = pd.read_csv(file_path)
    employees = []
    for _, row in df.iterrows():
        fio = row['ФИО']
        position = row['Должность']
        hire_date = row['Дата найма']
        salary = row['Оклад']

        try:
            salary = float(salary.replace(',', ''))
        except ValueError:
            raise ValueError(f"Неверное значение зарплаты для {fio}: {salary}")

        employees.append(Employee(fio, position, hire_date, salary))
    return employees

# Функция для расчета фонда оплаты труда
def calculate_total_payroll(employees):
    total_payroll = sum([emp.get_salary() for emp in employees])
    print(f"Фонд оплаты труда: {total_payroll} руб.")
    return total_payroll

# Функция для визуализации окладов по должностям
def plot_salaries_by_position(employees):
    positions = [emp.get_position() for emp in employees]
    salaries = [emp.get_salary() for emp in employees]

    df = pd.DataFrame({'Должность': positions, 'Оклад': salaries})
    df.groupby('Должность').mean()['Оклад'].plot(kind='bar', color='skyblue')

    plt.title('Оклад по должностям')
    plt.ylabel('Оклад (руб.)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.close()  # Закрыть графическое окно, чтобы избежать блокировок

# Функция для расчета налогов (подоходный налог 13%, соц. страхование 30%)
def calculate_taxes(employees, income_tax_rate=0.13, social_security_rate=0.30):
    tax_results = []
    for emp in employees:
        income_tax = emp.get_salary() * income_tax_rate  # Подоходный налог
        social_security_tax = emp.get_salary() * social_security_rate  # Социальное страхование
        tax_results.append({
            'ФИО': emp.get_fio(),
            'Оклад': emp.get_salary(),
            'Налог': income_tax,
            'Соц. страхование': social_security_tax,
            'Итого налогов': income_tax + social_security_tax
        })
        print(f"Налоги для {emp.get_fio()}: {income_tax:.2f} руб. (подоходный), {social_security_tax:.2f} руб. (соц. страх.)")
    return tax_results

# Основной код
if __name__ == "__main__":
    # Загрузите путь к файлу mashinka_manerova.csv
    file_path = '/Users/shneiderman02/Documents/PythonProject/mashinka_manerova.csv'  # Укажите путь к CSV файлу

    # Загружаем сотрудников из CSV
    employees = load_employees_from_csv(file_path)

    # Пример использования методов

    # 1. Расчет премий ко Дню программиста
    for emp in employees:
        bonus = emp.calculate_programmer_bonus()
        if bonus > 0:
            print(f"Премия ко Дню программиста для {emp.get_fio()}: {bonus:.2f} руб.")

    # 2. Расчет премий к 8 марта и 23 февраля
    for emp in employees:
        holiday_bonus = emp.calculate_holiday_bonus()
        print(f"Премия к празднику для {emp.get_fio()}: {holiday_bonus} руб.")

    # 3. Индексация зарплаты
    for emp in employees:
        emp.set_salary(emp.calculate_salary_indexation())
        print(f"Индексация зарплаты для {emp.get_fio()}: {emp.get_salary():.2f} руб.")

    # 4. Список сотрудников для отпуска
    vacation_list = [emp.get_fio() for emp in employees if emp.is_eligible_for_vacation()]
    print("Сотрудники, имеющие право на отпуск:", vacation_list)

    # 5. Расчет фонда оплаты труда
    calculate_total_payroll(employees)

    # 6. Построение столбчатой диаграммы окладов по должностям
    plot_salaries_by_position(employees)

    # 7. Расчет налоговых отчислений
    calculate_taxes(employees)
