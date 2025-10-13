import pandas as pd
import matplotlib.pyplot as plt

def create_pie_chart(df):
    operation_counts = df['Операция'].value_counts()
    
    plt.pie(operation_counts.values,  labels=operation_counts.index, autopct='%1.1f%%', textprops={'fontsize': 6})
    plt.title('Распределение типов операций')