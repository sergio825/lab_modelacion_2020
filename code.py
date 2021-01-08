import pandas as pd
import numpy as np

ots = pd.read_csv("data/ot.csv",sep=',')
ots=ots.sort_values('Order')
xlsx_file = "data/layout.xlsx"
layout = pd.read_excel(xlsx_file, sheet_name="layout")
adj=pd.read_excel(xlsx_file, sheet_name="adyacencia")
num_of_orders=len(ots['Order'].unique())
aisles=layout['aisle'].unique()
tiempo_pickeo=10
velocidad=4

list1=[]
for x in range(num_of_orders): 
  obj=list(ots.loc[ots["Order"]==x+1]["Cod.Prod"])
  list1.append(obj)
orders=np.array(list1)

l=[]
for aisle in aisles:
  l.append([aisle,False, 0])
aisle_bool=pd.DataFrame(l,columns=["aisle","ocuppied","picker"])


def assignment_of_orders(pickers:list, orders_enum:list, num_of_pickers:int )->list:
    '''This function assigns orders to the pickers that are not working'''
    for x in range(num_of_pickers):
        if pickers[x]==0:
            if len(orders_enum)>0:
                pickers[x]=orders_enum[0]
                orders_enum.remove(orders_enum[0])
    return pickers

def next_move(aisle_to_go:float,act_aisle:float, adj:pd.core.frame.DataFrame)->float:
    '''Returns the next aisle to visit in a route
    from a starting aisle to another aisle'''
    ady=adj.loc[adj["aisle"]==act_aisle]
    for x in range(ady.shape[0]):
        if route_exist(aisle_to_go,ady.iloc[x,1],adj):
            return ady.iloc[x,1]
            
def sort(order:list, aisles:np.ndarray):
    '''sort the orders according to the aisles'''
    lista_ordenada=[]
    for pasillo in aisles:
        for x in range(len(order)):
            if pasillo==product_in_aisle(order[x],layout):
                lista_ordenada.append(order[x])
    return lista_ordenada
                 
            
def route_exist(a1:float,a2:float, adj:pd.core.frame.DataFrame)->bool:
    '''returns true if exist any route from a starting aisle to another aisle, false in other case'''
    ady=adj.loc[adj["aisle"]==a2]
    
    if a1==a2:
        return True
    
    for x in range(ady.shape[0]):
        if ady.iloc[x,1]==a1:
            return True
        else:
            if ady.iloc[x,1]==-1:
                return False
            else:
                return route_exist(a1,ady.iloc[x,1],adj)
            
def routing(aisle_to_go:float,act_aisle:float)->list:
    '''returns the route from an initial aisle, to another aisle'''
    x=act_aisle
    l=[]
    while x!=aisle_to_go:
        x=next_move(aisle_to_go,x,adj)
        l.append(x)
    return l

def product_in_aisle(prod_code:float, layout:pd.core.frame.DataFrame):
    '''returns the aisle where you can find the product'''
    l=layout.loc[layout["Product"]==prod_code]
    pasillo=l.iloc[0,2]
    return pasillo

def ocuppied(aisle:float,aisle_bool:pd.core.frame.DataFrame)->bool:
    '''returns true if the aisle is ocuppied, false if not'''
    p=aisle_bool.loc[aisle_bool["aisle"]==aisle]
    return p.iloc[0,1]

def time(orders:np.ndarray,num_of_pickers:int, ots:pd.core.frame.DataFrame,
           layout:pd.core.frame.DataFrame, adj:pd.core.frame.DataFrame):
    '''
    
    Parameters
    ----------
    orders: array with the products to pick in the orders
    ots:Dataframe with orders
    layout: Dataframe with information about the layout of the warehouse
    adj: Dataframe with information about the adjacence of the aisles
    
    Returns
    -----------
    t:Float
    
        Final function, returns the total time in which the orders are completed
    '''
    
    pickeadores=[]
    t=0
    t_recorrido=0
    t_wait=0
    t_pick=0
    contador=[]
    to_end=[]
    ordenes_enum=ots["Order"].unique()
    ordenes_enum=list(ordenes_enum)
    pasillo_act=[]
    pasillos=layout['aisle'].unique() 
    for x in range(num_of_pickers): 
        pasillo_act.append(0)
 
    pickeadores=[]
    for x in range(num_of_pickers):
        pickeadores.append(0)
  
    
    for x in range(len(orders)):
        orders[x]=sort(orders[x],pasillos)
        
    for x in range(num_of_pickers):
        to_end.append(0)
        
    for y in range(num_of_pickers):
        contador.append(0)
        
    while len(ordenes_enum)>=0:
        
        if assignment_of_orders(pickeadores,ordenes_enum,num_of_pickers)==to_end:
            break
        assignment_of_orders(pickeadores,ordenes_enum,num_of_pickers)
        for x in range(num_of_pickers):
            if pickeadores[x]!=0: 
                print("----------------------------------------")
                print("picker:", x+1 , "in the order", pickeadores[x],"\n")
                print("actual aisle:", pasillo_act[x])
                if contador[x]==-1:
                    print("picker going to the depot")
                    next_move=-1
                else:
                    print("Next product to pick:", orders[pickeadores[x]-1][contador[x]])
                    next_move=product_in_aisle(orders[pickeadores[x]-1][contador[x]],layout)
                if len(routing(next_move,pasillo_act[x]))==0:#estoy en el pasillo a recoger producto
                    if pasillo_act[x]==-1:
                        print("picker", "finished order", pickeadores[x] ,"at the minute:", t/60 )
                        contador[x]=0
                        pickeadores[x]=0
                        pasillo_act[x]=0    
                    else:
                        t_pick+=tiempo_pickeo
                        t+=tiempo_pickeo
                        
                        if contador[x]+1<len(orders[pickeadores[x]-1]):
                            contador[x]+=1
                        else:
                            contador[x]=-1
                else:
                    route=routing(next_move,pasillo_act[x])
                    if route[0]==-1:
                        print("next location: Depot" )
                        distancia_df=adj.loc[(adj["aisle"]==pasillo_act[x]) & (adj["adjacent"]==route[0])]
                        distancia=distancia_df.iloc[0,2]
                        aisle_bool.iloc[aisle_bool.loc[aisle_bool["aisle"]==pasillo_act[x]].index,1]=False
                        aisle_bool.iloc[aisle_bool.loc[aisle_bool["aisle"]==pasillo_act[x]].index,2]=0
                        t_recorrido+=distancia/velocidad
                        t+=distancia/velocidad
                        pasillo_act[x]=route[0]
                        aisle_bool.iloc[aisle_bool.loc[aisle_bool["aisle"]==route[0]].index,1]=True
                        aisle_bool.iloc[aisle_bool.loc[aisle_bool["aisle"]==route[0]].index,2]=x+1
                    
                    else:
                        print("next aisle to visit:",route[0])
                        if ocuppied(route[0],aisle_bool):
                            print("aisle",route[0], " ocuppied at the minute:", t/60)
                            t_wait+=tiempo_pickeo
                            t+=tiempo_pickeo
                        else:
                            
                            if pasillo_act[x]>0:
                                largo_pasillo=layout.loc[layout["aisle"]==pasillo_act[x]].iloc[0,9]
                                t_recorrido+=(largo_pasillo/velocidad)
                                t+=(largo_pasillo/velocidad)
                            
                            distancia_df=adj.loc[(adj["aisle"]==pasillo_act[x]) & (adj["adjacent"]==route[0])]
                            distancia=distancia_df.iloc[0,2]
                            aisle_bool.iloc[aisle_bool.loc[aisle_bool["aisle"]==pasillo_act[x]].index,1]=False
                            aisle_bool.iloc[aisle_bool.loc[aisle_bool["aisle"]==pasillo_act[x]].index,2]=0
                            print("picker moves to the aisle", route[0],"\n")
                            print("aisle", pasillo_act[x]," free ", "at the minute:", t/60)
                            t_recorrido+=distancia/velocidad
                            t+=distancia/velocidad
                            pasillo_act[x]=route[0]
                            
                            aisle_bool.iloc[aisle_bool.loc[aisle_bool["aisle"]==route[0]].index,1]=True
                            aisle_bool.iloc[aisle_bool.loc[aisle_bool["aisle"]==route[0]].index,2]=x+1
    print("\n \n")     
    print ("Congestion time:", t_wait/60)
    print("Travel time:", t_recorrido/60)
    print("Picking time:", t_pick/60)
    
    return t/60
