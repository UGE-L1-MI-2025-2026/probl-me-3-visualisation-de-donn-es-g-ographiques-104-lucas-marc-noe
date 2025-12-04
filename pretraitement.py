import json
import pandas as pd
import os
import time
"""
with open('temperature-quotidienne-departementale.json')as file:
    data=json.load(file)
print(data)
"""

default_file='temperature-quotidienne-departementale.json'
clear_file='temperatures-traitées.parquet'
colonne_date='date_obs'

def pretraitement():
    if not os.path.exists(default_file):
        print("Fichier introuvable.")
        return
    
    temps_deb=time.time()
    
    try:
        with open('temperature-quotidienne-departementale.json')as file:
            data=json.load(file)
        df=pd.DataFrame(data)
    except Exception as e:
        print(e)
        return 
    
    if colonne_date in df.columns:
        df['Date']=pd.to_datetime(df[colonne_date])
        df=df.drop(columns=[colonne_date])
    
    if 'Date' in df.columns:
        df=df.sort_values(by=['Date','departement'], ascending=[True, True])
    
    try:
        df.to_parquet(clear_file,index=False)
    except exception as e:
        print("Erreur lors de la sauvegarde du fichier parquet "+e)

    temps_fin=time.time()
    print("Preptratiement terminé en "+str(temps_fin - temps_deb)+" secondes. Fichier crée : "+ str(clear_file))
    

pretraitement()
