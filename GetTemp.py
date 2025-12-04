import pandas as pd
#partie temperature
import fltk as fl
import matplotlib.cm as cm 
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


df=pd.read_parquet('temperatures-traitées.parquet')

dico_mois={'01':31,'02':28,'03':31,'04':30,'05':31,'06':30,'07':31,'08':31,'09':30,'10':31,'11':30,'12':31}
list_annee=['2018','2019','2020','2021','2022','2023','2024','2025']
bissextile=['2020','2024']

def set_date_mois(annee,mois):
    str_date=[]
    for jour in range(1,dico_mois[mois]+1):
        if jour<=9:
            str_jour='0'+str(jour)
        else:
            str_jour=str(jour)
        dt=annee+'-'+mois+'-'+str_jour
        str_date.append(dt)
    return str_date

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

#print(temp_moy_annee_dep('2025','Rhône'))

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

#print(temp_max_annee_dep('2025','Rhône'))

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

#print(temp_min_annee_dep('2024','Rhône'))


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


def test_cercle(color):
    fl.cree_fenetre(800,800)
    fl.cercle(200, 200, 75, remplissage=str(color))

    fl.attend_ev()
    fl.ferme_fenetre()

    
###TEST###
temp_trouve=temp_moy_annee_dep('2024','Rhône')
print(temp_trouve)
t_ex=temp_to_color(temp_trouve)
print(t_ex)
a=rgba_float_to_int(cmap(int(t_ex)))#ATTENTION , sans le int un probleme de valeur apparait exemple: cmap(78.97 donne du jaune comme si c'etait la valeur maximale)
print(a)
test_cercle(rgb_to_hex(a))

#stockage (dans un fichier txt) desdonnées annuelle par departement

