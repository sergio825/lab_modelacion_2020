#Algunas Consideraciones:
tiempo_pickeo=20#[s]
velocidad=20# [m/s]

lista=[]
for x in range(cant_ordenes): 
  obj=list(ots.loc[ots["Pedido"]==x+1]["Cod.Prod"])
  lista.append(obj)
ordenes=np.array(lista)

for x in range(len(ordenes)):
  ordenes[x]=ordenar(ordenes[x],pasillos)


l=[]
for pasillo in pasillos:
  l.append([pasillo,False, 0])
pasillo_bool=pd.DataFrame(l,columns=["pasillo","ocupado","pickeador"])
