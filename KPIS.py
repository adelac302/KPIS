#!/usr/bin/env python
# coding: utf-8

# In[4]:


get_ipython().system('pip install plotly')
get_ipython().system('pip install tabulate')


# In[5]:


import numpy as np 
import pandas as pd 
import plotly.express as px
import warnings  
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.style as style
import seaborn as sns
import seaborn as sns
from tabulate import tabulate

warnings.filterwarnings("ignore")
YEAR = 2023
MES = 11
fecha_inicio='2023-11-20'
fecha_fin='2023-11-26'


# In[6]:



df=pd.read_excel(r'C:\Users\sistemas\Desktop\KPIS_ELN2.xlsx')
df


# In[7]:


df.info()


# In[8]:


df["eqmtid"]=[s.strip() for s in df["eqmtid"]]
df['YEAR'] = df['shiftdate'].dt.strftime('%Y')
df['MONTH'] = df['shiftdate'].dt.strftime('%m')
df


# In[9]:


df['MONTH'].unique()


# In[10]:


df['YEAR'].unique()


# In[11]:


df1 = df[(df['YEAR'] == '2023') & (df['MONTH'] == '11')]
df1


# In[12]:



df1['unit'].unique()
df1['unit']=[s.strip() for s in df1['unit']]
df1= df1[(df1['unit'] == 'Camion')]
df1


# In[13]:


df1['shiftdate']=pd.to_datetime(df1['shiftdate'])
df1=df1[(df1['shiftdate']>=fecha_inicio)&(df1['shiftdate']<=fecha_fin)]
df1


# In[52]:


df1['nueva_columna'] = ((df1['hrope'] + df1['hruti']) * 100) / df1['hrdsp']

# Utiliza pivot_table para organizar los resultados
dfu1 = df1.pivot_table(index="eqmtid", columns="shiftdate", values=("hrope",'hruti',), aggfunc='sum')
dfu1['nueva_columna'] = dfu1[('hrope', 'sum')] + dfu1[('hruti', 'sum')]
dfu1['nueva_columna']


# In[15]:


get_ipython().system('pip install cufflinks')
import pandas as pd
import cufflinks as cf
from IPython.display import display,HTML
cf.set_config_file(sharing='public',theme='white',offline=True)


# In[16]:


dfdisp=df1.pivot_table(index="eqmtid",columns="shiftdate",values="disp",aggfunc="mean")
dfdisp


# In[17]:


dfu=df1.pivot_table(index="eqmtid",columns="shiftdate",values="util",aggfunc="mean")
dfu


# In[18]:


eqmtids = dfdisp.index
num_eqmtids = len(eqmtids)

colors = plt.cm.get_cmap('tab10', num_eqmtids)

num_cols = 3
num_rows = -(-num_eqmtids // num_cols)

fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

for i, eqmtid in enumerate(eqmtids):
    row = i // num_cols
    col = i % num_cols
    ax = axs[row, col] if num_rows > 1 else axs[col]
    
    color = colors(i)

    ax.bar(dfdisp.columns, dfdisp.loc[eqmtid], color=color, alpha=0.7)
    ax.set_title(f'Disponibilidad por día para eqmtid {eqmtid}')
    ax.set_xlabel('Día')
    ax.set_ylabel('Disponibilidad')
    ax.set_xticklabels(dfdisp.columns, rotation=45)
    ax.grid(axis='y')

    for bar, value in zip(ax.patches, dfdisp.loc[eqmtid]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), round(value, 2),
                ha='center', va='bottom', fontsize=8)
    
    # Agregar línea constante en y=85
    ax.axhline(y=85, color='red', linestyle='--', linewidth=1)

for i in range(num_eqmtids, num_rows * num_cols):
    row = i // num_cols
    col = i % num_cols
    ax = axs[row, col] if num_rows > 1 else axs[col]
    ax.axis('off')

plt.tight_layout()

# Guardar la figura como un archivo PDF
plt.savefig('grafico_DISPONIBILIDAD_por_dia.pdf', format='pdf')

plt.show()


# In[19]:


eqmtids = dfu.index
num_eqmtids = len(eqmtids)

colors = plt.cm.get_cmap('tab10', num_eqmtids)

num_cols = 3
num_rows = -(-num_eqmtids // num_cols)

fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

for i, eqmtid in enumerate(eqmtids):
    row = i // num_cols
    col = i % num_cols
    ax = axs[row, col] if num_rows > 1 else axs[col]
    
    color = colors(i)

    ax.bar(dfu.columns, dfu.loc[eqmtid], color=color, alpha=0.7)
    ax.set_title(f'Utilidad por día para eqmtid {eqmtid}')
    ax.set_xlabel('Día')
    ax.set_ylabel('Utilidad')
    ax.set_xticklabels(dfu.columns, rotation=45)
    ax.grid(axis='y')

    for bar, value in zip(ax.patches, dfu.loc[eqmtid]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), round(value, 2),
                ha='center', va='bottom', fontsize=8)
    
    # Agregar línea constante en y=85 (por ejemplo)
    ax.axhline(y=85, color='red', linestyle='--', linewidth=1)

for i in range(num_eqmtids, num_rows * num_cols):
    row = i // num_cols
    col = i % num_cols
    ax = axs[row, col] if num_rows > 1 else axs[col]
    ax.axis('off')

plt.tight_layout()

# Guardar la figura como un archivo PDF
plt.savefig('grafico_utilidad_por_dia.pdf', format='pdf')

plt.show()


# In[20]:


dfres=df1.groupby(['eqmtid'])[['hrope','hruti','hrdem','hrsby','hrmnt','hrdsp','htot']].sum()
utilizacion=((dfres['hrope']+dfres['hruti'])/dfres['hrdsp'])*100
disponibilidad=(dfres['hrdsp']/dfres['htot'])*100
dfres=dfres.assign(disponibilidad=disponibilidad.values)
dfres=dfres.assign(utilizacion=utilizacion.values)
dfres


# In[21]:


# Supongamos que tienes un DataFrame dfres con columnas 'disponibilidad' y 'utilizacion'

plt.figure(figsize=(12, 8))

# Graficar la disponibilidad
plt.subplot(2, 1, 1)
dfres['disponibilidad'].plot(kind='bar', width=0.4, color='skyblue')
plt.axhline(y=85, color='red', linestyle='--', label='Disponibilidad Aprobada')
plt.title('Disponibilidad')
plt.xlabel('Índice')
plt.ylabel('Disponibilidad')
plt.xticks(rotation=45)
plt.legend()
plt.grid(axis='y')

# Agregar etiquetas de datos a cada barra de disponibilidad
for i, value in enumerate(dfres['disponibilidad']):
    plt.text(i, value + 0.2, f'{value:.2f}', ha='center', va='bottom')

# Graficar la utilización
plt.subplot(2, 1, 2)
dfres['utilizacion'].plot(kind='bar', width=0.4, color='orange')
plt.axhline(y=85, color='red', linestyle='--', label='Utilización Aprobada')
plt.title('Utilización')
plt.xlabel('Índice')
plt.ylabel('Utilización')
plt.xticks(rotation=45)
plt.legend()
plt.grid(axis='y')

# Agregar etiquetas de datos a cada barra de utilización
for i, value in enumerate(dfres['utilizacion']):
    plt.text(i, value + 0.2, f'{value:.2f}', ha='center', va='bottom')

plt.tight_layout()

# Guardar los gráficos como un archivo PDF
plt.savefig('disponibilidad_y_utilizacion_linea_y85.pdf', format='pdf')

plt.show()

