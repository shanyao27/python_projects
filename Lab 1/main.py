import json
import pandas as pd
import matplotlib.pyplot as plt
from graph_1 import draw_chart_bar
from graph_2 import create_pie_chart


with open('ВыгрузкаКонтрольПоручений.txt', 'r', encoding='utf-8') as file:
    data = json.load(file)
    
df = pd.DataFrame(data)
    
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
draw_chart_bar(df)
plt.subplot(1, 2, 2)
create_pie_chart(df)
    
plt.show()

