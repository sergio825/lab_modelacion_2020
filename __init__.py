import numpy as np
import pandas as pd

cant_ordenes=len(ots['Pedido'].unique())
for x in range(cant_ordenes): 
  obj=list(ots.loc[ots["Pedido"]==x+1]["Cod.Prod"])
  lista.append(obj)
ordenes=np.array(lista)
