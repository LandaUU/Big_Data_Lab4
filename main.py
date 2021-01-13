import pandas
import re
from datetime import datetime

df = pandas.read_csv('Moscow.csv')

df["name"] = df["name"].str.lower()

# Группировка вакансий по названиям
vacancy_list = ['разработчик|developer|программист', 'инженер|engineer', 'архитектор|architect', 'аналитик|analyst',
                'data scientist', 'c++', 'c#', 'python', 'js|javascript', '1c', 'goland', 'frontend',
                'backend', 'full-stack|fullstack', 'security|безопасность']

print(df.columns)

for column_name in df.columns:
    print(df[column_name].value_counts())
    print(df[column_name].isnull())

df_group = pandas.DataFrame()
for vacancy in vacancy_list:
    for v in vacancy.split('|'):
        dfV = df[df["name"].replace('/', '').str.contains(re.escape(v))]
    if len(df_group.columns) == 0:
        df_group = dfV.copy()
    else:
        df_group.append(dfV)
    group_name = vacancy
    print('======================' + str(group_name) + '======================')
    # Заполнить пропуски в вакансии средним значением
    df_group["min_salary"] = df_group["min_salary"].fillna(df_group["min_salary"].mean())
    print(df_group["min_salary"])

    df_date = pandas.to_datetime(df_group['published_date']).dt.tz_localize(None)
    df_date_now = pandas.to_datetime(datetime.now())
    df_days = df_date_now - df_date
    # Добавить новый признак в датасет на основе признака “дата размещения вакансии” - количество дней с момента
    # размещения;
    df_group["publish_date"] = df_days
    print(df_group["publish_date"])
    # Заполнить пропуски в признаке “требуемый опыт работы” по принципу: если не указан, то опыт не требуется;
    df_group["experience"] = df_group["experience"].fillna("Нет опыта")
    # Заполнить пропуски в признаке “тип занятости” по принципу: если не указан, то любой тип;
    df_group["employment"] = df_group["employment"].fillna("Любой тип")

    df_group["city"] = df_group["city"].dropna()
    df_group["description"] = df_group["description"].fillna("Нет описания")
    df_group["duty"] = df_group["duty"].fillna("Нет описания обязанностей")
    df_group["requirements"] = df_group["requirements"].fillna("Нет описания требований")
    df_group["terms"] = df_group["terms"].fillna("Нет описания условий")
    # Надо подумать, чем заполнять умения если компания их не заполнила. Я бы так и оставил пустым, хотя можно просто
    # значение задать "неопределено"
    #df_group["skills"] = df_group["skills"].fillna("[{'name': 'Неопределено'}]")
    df_group["skills"] = df_group["skills"].fillna("Не указано")
    df_group = pandas.DataFrame()
