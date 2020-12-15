import pandas as pd
import numpy as np

ots = pd.read_csv("data/ot.csv",sep=',')
ots=ots.sort_values('Pedido')
xlsx_file = "data/layout.xlsx"
layout = pd.read_excel(xlsx_file, sheet_name="layout")
adyacencia=pd.read_excel(xlsx_file, sheet_name="adyacencia")
cant_ordenes=len(ots['Pedido'].unique())
pasillos=layout['pasillo'].unique()
