import numpy as np
import pandas as pd

cant_ordenes=len(ots['Pedido'].unique())
pasillos=layout['pasillo'].unique() 

for x in range(cant_ordenes): 
  obj=list(ots.loc[ots["Pedido"]==x+1]["Cod.Prod"])
  lista.append(obj)
ordenes=np.array(lista)

l=[]
for pasillo in pasillos:
  l.append([pasillo,False, 0])
pasillo_bool=pd.DataFrame(l,columns=["pasillo","ocupado","pickeador"])

pasillo_act=[]
for x in range(cant_pickeadores): 
  pasillo_act.append(0)
 
pickeadores=[]
for x in range(cant_pickeadores):
  pickeadores.append(0)

