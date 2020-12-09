import pandas as pd
import numpy as np




'''Extracción de datos:'''
ots = pd.read_csv("data/ot.csv",sep=',')
ots=ots.sort_values('Pedido')
xlsx_file = "data/layout.xlsx"
layout = pd.read_excel(xlsx_file, sheet_name="layout")
adyacencia=pd.read_excel(xlsx_file, sheet_name="adyacencia")
cant_ordenes=len(ots['Pedido'].unique())
pasillos=layout['pasillo'].unique()
ordenes_enum=ots["Pedido"].unique()
ordenes_enum=list(ordenes_enum)  

'''se crea array con cada orden y cada producto'''
lista=[]
for x in range(cant_ordenes):
    obj=list(ots.loc[ots["Pedido"]==x+1]["Cod.Prod"])
    lista.append(obj)
    ordenes=np.array(lista)


'''se crea lista con el pedido asignado a cada pickeador(inicialmente 0)'''
pickeadores=[]
for x in range(cant_pickeadores):
    pickeadores.append(0)
    

'''data frame con informacion sobre que pasillo esta ocupado'''
l=[]
for pasillo in pasillos:
    l.append([pasillo,False, 0])
pasillo_bool=pd.DataFrame(l,
                          columns=["pasillo","ocupado","pickeador"])

    


'''se inicializa una lista donde el elemento i es el pasillo actual del pickeador i+1'''
pasillo_act=[]
for x in range(cant_pickeadores):
    pasillo_act.append(0)
    
    
    
'''Funciones'''
def asignar_ordenes(pickeadores):
    for x in range(cant_pickeadores):
        if pickeadores[x]==0:
            if len(ordenes_enum)>0:
                pickeadores[x]=ordenes_enum[0]
                ordenes_enum.remove(ordenes_enum[0])
    return pickeadores

def next_move(pasillo_a_ir,pasillo_act):
    ady=adyacencia.loc[adyacencia["pasillo"]==pasillo_act]
    for x in range(ady.shape[0]):
        if existe_ruta(pasillo_a_ir,ady.iloc[x,1]):
            return ady.iloc[x,1]
            
            
            
def existe_ruta(p1,p2):
    ady=adyacencia.loc[adyacencia["pasillo"]==p2]
    
    if p1==p2:
        return True
    
    for x in range(ady.shape[0]):
        if ady.iloc[x,1]==p1:
            return True
        else:
            if ady.iloc[x,1]==-1:
                return False
            else:
                return existe_ruta(p1,ady.iloc[x,1])
            
def ruta(pasillo_a_ir,pasillo_act):
    x=pasillo_act
    l=[]
    while x!=pasillo_a_ir:
        x=next_move(pasillo_a_ir,x)
        l.append(x)
    return l

def objeto_en_pasillo(cod_prod):
    l=layout.loc[layout["Producto"]==cod_prod]
    pasillo=l.iloc[0,2]
    return pasillo

def ocupado(pasillo):
    p=pasillo_bool.loc[pasillo_bool["pasillo"]==pasillo]
    return p.iloc[0,1]

def tiempo(ordenes,pickeadores):
    print("cant pickeadores:", cant_pickeadores)
    for x in range(len(ordenes)):
        ordenes[x]=ordenar(ordenes[x])
    
    t_recorrido=0
    t_wait=0
    t_pick=0
    contador=[]
    for y in range(cant_pickeadores):
        contador.append(0)
        
    while len(ordenes_enum)>0:
        
        asignar_ordenes(pickeadores)
        for x in range(cant_pickeadores):
            if pickeadores[x]!=0: 
                if contador[x]==-1:
                    next_move=-1
                else:
                    next_move=objeto_en_pasillo(ordenes[pickeadores[x]-1][contador[x]])
                if len(ruta(next_move,pasillo_act[x]))==0:
                    if pasillo_act[x]==-1:
                        contador[x]=0
                        pickeadores[x]=0
                        pasillo_act[x]=0
                    
                    else:
                        t_pick+=tiempo_pickeo
                        if contador[x]+1<len(ordenes[pickeadores[x]-1]):
                            contador[x]+=1
                        else:
                            contador[x]=-1
                else:
                    route=ruta(next_move,pasillo_act[x])
                    if route[0]==-1:
                        pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==pasillo_act[x]].index,1]=False
                        pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==pasillo_act[x]].index,2]=0
                        t_recorrido+=1/velocidad
                        pasillo_act[x]=route[0]
                        pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==route[0]].index,1]=True
                        pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==route[0]].index,2]=x+1
                    
                    else:
                        if ocupado(route[0]):
                            t_wait+=tiempo_pickeo
                        else:
                            if pasillo_act[x]>0:
                                largo_pasillo=layout.loc[layout["pasillo"]==pasillo_act[x]].iloc[0,9]
                                t_recorrido+=largo_pasillo/velocidad
                            pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==pasillo_act[x]].index,1]=False
                            pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==pasillo_act[x]].index,2]=0
                            t_recorrido+=1/velocidad
                            pasillo_act[x]=route[0]
                            pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==route[0]].index,1]=True
                            pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==route[0]].index,2]=x+1
            
    print ("tiempo de espera:", t_wait)
    print("tiempo en hacer recorridos:", t_recorrido)
    print("tiempo de pickeo:", t_pick)
    
    return t_recorrido+t_wait+t_pick

def ordenar(orden):
    lista_ordenada=[]
    for pasillo in pasillos:
        for x in range(len(orden)):
        
            if pasillo==objeto_en_pasillo(orden[x]):
                lista_ordenada.append(orden[x])
    return lista_ordenada
        
'''Datos considerados para la implementacion (modificables):'''  
cant_pickeadores=18
tiempo_pickeo=20
velocidad= 20

   
    
        
    
    
    
    
    
    
    


            
            
        
   
        

        
        
        

                
                
        
        
        
    
            
    
       
            
                

        
        
    
        
        
        
    
    
    

 


