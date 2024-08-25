import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = {}
for i in range(1,5):
    data[i] = pd.read_csv(f"/diem_thi_202{i}.csv")

data[1].drop(columns = ["Unnamed: 0", "Cum_thi"], inplace = True)
data[1].rename(columns = {'SBD':"id", 'Toan' :"Toán", 'Ngu_van': "Văn", 'Ngoai_ngu':"Ngoại ngữ", 'Vat_ly':"Lí", 'Hoa_hoc': "Hóa", 'Sinh_hoc': "Sinh",'Lich_su':"Sử", 'Dia_ly':"Địa"},inplace=True)
data[2].rename(columns = {'sbd': "id", 'toan':"Toán", 'ngu_van':"Văn", 'ngoai_ngu': "Ngoại ngữ", 'vat_li':"Lí", 'hoa_hoc':"Hóa", 'sinh_hoc':"Sinh",'lich_su':"Sử", 'dia_li':"Địa", 'gdcd':"GDCD"}, inplace = True)

for i in range(1,5):
    data[i] = data[i][['id', 'Toán', 'Văn', 'Ngoại ngữ', 'Lí', 'Hóa', 'Sinh', 'Sử', 'Địa','GDCD']]

plt.style.use("seaborn-v0_8-whitegrid")

### Phân tích dữ liệu năm 2024

# Biểu đồ số lượng bài thi mỗi môn năm 2024
data_chart = data[4][['Toán', 'Văn', 'Ngoại ngữ', 'Sử', 'Địa', 'GDCD', 'Lí', 'Hóa','Sinh']]

fig, ax = plt.subplots()
bars = ax.bar(data_chart.columns, data_chart.count()/1000)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')
    
ax1 = ax.twinx()
ax1.plot(data_chart.columns, data_chart.mean(), color = "red", marker='o', label='Điểm trung bình')
ax1.set_ylim(0, 10)

ax.set(title ="Biểu đồ số lượng bài thi và điểm trung bình mỗi môn năm 2024", ylabel= "Số lượng bài thi (x1000)")
ax.legend(loc='upper left')
ax1.legend(loc='upper right')


### So sánh dữ liệu năm 2024 với các năm trước

# Biển đồ Density Toán văn anh    
fig, ax = plt.subplots(figsize=(10, 6))
for i in range(1,5):
    ax = sns.kdeplot(data = data[i], x = "Toán", label = f"202{i}")
ax.set(title = "Biểu đồ tỷ trọng phân bổ điểm toán", xlabel= "Điểm")
ax.legend();

fig, ax = plt.subplots(figsize=(10, 6))
for i in range(1,5):
    ax = sns.kdeplot(data = data[i], x = "Văn", label = f"202{i}")
ax.set(title = "Biểu đồ tỷ trọng phân bổ điểm văn", xlabel= "Điểm")
ax.legend();

fig, ax = plt.subplots(figsize=(10, 6))
for i in range(1,5):
    ax = sns.kdeplot(data = data[i], x = "Anh", label = f"202{i}")
ax.set(title = "Biểu đồ tỷ trọng phân bổ điểm anh", xlabel= "Điểm")
ax.legend();



