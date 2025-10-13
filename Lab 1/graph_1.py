import pandas as pd
import matplotlib.pyplot as plt

def draw_chart_bar(df):
    warehouse_counts = df['Фирма'].value_counts()  
    warehouses = ['Владивосток Склад', 'Иркутск Склад']
    warehouse_data = []
    for warehouse in warehouses:
        count = warehouse_counts.get(warehouse, 0)  
        warehouse_data.append(count)

    plt.bar(warehouses, warehouse_data, color=['pink', 'orange'])
    plt.title('Количество операций по складам')
    plt.xlabel('Склады')
    plt.ylabel('Количество операций')
