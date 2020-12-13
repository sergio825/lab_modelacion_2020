

def asignar_ordenes(pickeadores:list, ordenes_enum:list, cant_pickeadores:int )->list:
    for x in range(cant_pickeadores):
        if pickeadores[x]==0:
            if len(ordenes_enum)>0:
                pickeadores[x]=ordenes_enum[0]
                ordenes_enum.remove(ordenes_enum[0])
    return pickeadores

def next_move(pasillo_a_ir:float,pasillo_act:float, adyacencia:pd.core.frame.DataFrame)->float:
    ady=adyacencia.loc[adyacencia["pasillo"]==pasillo_act]
    for x in range(ady.shape[0]):
        if existe_ruta(pasillo_a_ir,ady.iloc[x,1]):
            return ady.iloc[x,1]
            
def ordenar(orden:list, pasillos:np.ndarray):
    lista_ordenada=[]
    for pasillo in pasillos:
        for x in range(len(orden)):
            if pasillo==objeto_en_pasillo(orden[x]):
                lista_ordenada.append(orden[x])
    return lista_ordenada
                 
            
def existe_ruta(p1:float,p2:float, adyacencia:pd.core.frame.DataFrame)->bool:
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
            
def ruta(pasillo_a_ir:float,pasillo_act:float)->list:
    x=pasillo_act
    l=[]
    while x!=pasillo_a_ir:
        x=next_move(pasillo_a_ir,x)
        l.append(x)
    return l

def objeto_en_pasillo(cod_prod:float, layout:pd.core.frame.DataFrame):
    l=layout.loc[layout["Producto"]==cod_prod]
    pasillo=l.iloc[0,2]
    return pasillo

def ocupado(pasillo:float,pasillo_bool:pd.core.frame.DataFrame)->bool:
    p=pasillo_bool.loc[pasillo_bool["pasillo"]==pasillo]
    return p.iloc[0,1]

def tiempo(ordenes:np.ndarray,cant_pickeadores:int, ots:pd.core.frame.DataFrame,
           layout:pd.core.frame.DataFrame, adyacencia:pd.core.frame.DataFrame):
    
    pickeadores=[]
    t=0
    t_recorrido=0
    t_wait=0
    t_pick=0
    contador=[]
    to_end=[]
    ordenes_enum=ots["Pedido"].unique()
    ordenes_enum=list(ordenes_enum)
    pasillo_act=[]
    pasillos=layout['pasillo'].unique() 
    
    for x in range(len(ordenes)):
        ordenes[x]=ordenar(ordenes[x])
        
    for x in range(cant_pickeadores):
        to_end.append(0)
        
    for y in range(cant_pickeadores):
        contador.append(0)
        
    while len(ordenes_enum)>=0:
        
        if asignar_ordenes(pickeadores)==to_end:
            break
        asignar_ordenes(pickeadores)
        for x in range(cant_pickeadores):
            
            if pickeadores[x]!=0: 
                print("----------------------------------------")
                print("pickeador:", x+1 , "en orden", pickeadores[x],"\n")
                print("ubicacion actual:", pasillo_act[x])
                if contador[x]==-1:
                    print("pickeador camino al deposito")
                    next_move=-1
                else:
                    print("Siguiente producto a recoger:", ordenes[pickeadores[x]-1][contador[x]])
                    next_move=objeto_en_pasillo(ordenes[pickeadores[x]-1][contador[x]])
                if len(ruta(next_move,pasillo_act[x]))==0:#estoy en el pasillo a recoger producto
                    if pasillo_act[x]==-1:
                        print("pickeador", "termino orden ", pickeadores[x] ,"al minuto:", t/60 )
                        contador[x]=0
                        pickeadores[x]=0
                        pasillo_act[x]=0
                    
                    else:
                        t_pick+=tiempo_pickeo
                        t+=tiempo_pickeo
                        
                        if contador[x]+1<len(ordenes[pickeadores[x]-1]):
                            contador[x]+=1
                        else:
                            contador[x]=-1
                else:
                    route=ruta(next_move,pasillo_act[x])
                    if route[0]==-1:
                        print("siguiente parada: Deposito" )
                        distancia_df=adyacencia.loc[(adyacencia["pasillo"]==pasillo_act[x]) & (adyacencia["adyacente"]==route[0])]
                        distancia=distancia_df.iloc[0,2]
                        pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==pasillo_act[x]].index,1]=False
                        pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==pasillo_act[x]].index,2]=0
                        t_recorrido+=distancia/velocidad
                        t+=distancia/velocidad
                        pasillo_act[x]=route[0]
                        pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==route[0]].index,1]=True
                        pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==route[0]].index,2]=x+1
                    
                    else:
                        print("siguiente pasillo a visitar:",route[0])
                        if ocupado(route[0]):
                            print("pasillo",route[0], " ocupado al minuto:", t/60)
                            t_wait+=tiempo_pickeo
                            t+=tiempo_pickeo
                        else:
                            
                            if pasillo_act[x]>0:
                                largo_pasillo=layout.loc[layout["pasillo"]==pasillo_act[x]].iloc[0,9]
                                t_recorrido+=(largo_pasillo/velocidad)
                                t+=(largo_pasillo/velocidad)
                            
                            distancia_df=adyacencia.loc[(adyacencia["pasillo"]==pasillo_act[x]) & (adyacencia["adyacente"]==route[0])]
                            distancia=distancia_df.iloc[0,2]
                            pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==pasillo_act[x]].index,1]=False
                            pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==pasillo_act[x]].index,2]=0
                            print("pickeador se mueve al pasillo", route[0],"\n")
                            print("Se desocupa pasillo", pasillo_act[x], "al minuto:", t/60)
                            t_recorrido+=distancia/velocidad
                            t+=distancia/velocidad
                            pasillo_act[x]=route[0]
                            
                            pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==route[0]].index,1]=True
                            pasillo_bool.iloc[pasillo_bool.loc[pasillo_bool["pasillo"]==route[0]].index,2]=x+1
    print("\n \n")     
    print ("tiempo de espera:", t_wait/60)
    print("tiempo en hacer recorridos:", t_recorrido/60)
    print("tiempo de pickeo:", t_pick/60)
    
    return t/60
