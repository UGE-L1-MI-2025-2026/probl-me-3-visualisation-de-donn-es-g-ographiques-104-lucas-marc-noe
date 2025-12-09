import pandas as pd
from dico_departement import *
import fltk as fl
import matplotlib.cm as cm 
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


df=pd.read_parquet('temperatures-traitées.parquet')

liste_departement=df['departement'].unique().tolist()
liste_num_nom_departement=[]
for nom_departement in liste_departement:
    for num_departement in DEPARTMENTS.keys():
        if nom_departement==DEPARTMENTS[num_departement]:
            liste_num_nom_departement.append((num_departement,DEPARTMENTS[num_departement]))



#################################
###Partie temperatures moyenne###
#################################

def temp_moy_annee_dep(annee,departement):
    annee_int=int(annee)
    condition=((df['Date'].dt.year==annee_int)&(df['departement']==departement))
    df_filtre=df[condition]
    if not df_filtre.empty:
        return df_filtre['tmoy'].mean()
    return 0

###################################
###Partie temperatures maximales###
###################################

def temp_max_annee_dep(annee,departement):
    annee_int=int(annee)
    condition=((df['Date'].dt.year==annee_int)&(df['departement']==departement))
    df_filtre=df[condition]
    if not df_filtre.empty:
        return df_filtre['tmax'].max()
    return 0


###################################
###Partie temperatures minimales###
###################################

def temp_min_annee_dep(annee,departement):
    annee_int=int(annee)
    condition=((df['Date'].dt.year==annee_int)&(df['departement']==departement))
    df_filtre=df[condition]
    if not df_filtre.empty:
        return df_filtre['tmin'].min()
    return 0

#Association des temperatures

cmap = plt.colormaps['plasma']

def rgba_float_to_int(rgba_float_tuple):
    rgba_255_raw = np.array(rgba_float_tuple) * 255#convertition pour fromat rgb(255,255,255)
    rgb_int_array = np.rint(rgba_255_raw).astype(int)[:3]
    return tuple(int(val) for val in rgb_int_array)  

def rgb_to_hex(tuple_rgb):#convertit en hexadecimal pour fltk
    r,g,b=[int(val) for val in tuple_rgb]
    hexa=f'#{r:02x}{g:02x}{b:02x}'
    return hexa

def temp_to_color(temp):
    #pour le meme indicateur de temperature, -10 est la valeur la plus basse de l'indicateur
    #et 45 la valeur maximale, 0 se situe a environ 1/5 de l'indicateur
    temp_min,color_min=(-10,0)
    temp_max,color_max=(40,255)
    if temp>=0:
        temp_color= (temp*color_max)/temp_max
    else:
        temp_color=-(temp*color_max)/temp_max
    return temp_color


def conv_finale(temp):
    return rgb_to_hex(rgba_float_to_int(cmap(int(temp_to_color(temp)))))

a=3
print(temp_to_color(a))
print(cmap(int(temp_to_color(a))))
print(rgba_float_to_int(cmap(int(temp_to_color(a)))))


"""
#stockage (dans un fichier txt) desdonnées annuelle par departement
def data_file(annee):
    try:
        with open(annee+"-temperature-data.txt","w",encoding="utf-8") as f:
            for infos in liste_num_nom_departement:
                num_departement,departement=infos
                tmoy=temp_moy_annee_dep(annee,departement)
                tmoy_color=conv_finale(tmoy)
                tmin=temp_min_annee_dep(annee,departement)
                tmin_color=conv_finale(tmin)
                tmax=temp_max_annee_dep(annee,departement)
                tmax_color=conv_finale(tmax)
                f.write(f"{num_departement} {departement} {tmoy} {tmoy_color} {tmin} {tmin_color} {tmax} {tmax_color}\n")
    except IOError as e:
        print(f"ERREUR FATALE D'ÉCRITURE : {e}")


data_file("2025")
data_file("2024")
data_file("2023")
data_file("2022")
data_file("2021")
data_file("2020")
data_file("2019")
data_file("2018")
"""