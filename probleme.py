from fltk import *
import shapefile
import math



largeur = 800
hauteur = 720
taille = 1600
sf = shapefile.Reader("departement/departements-20180101")
shape = sf.shape()


def read_data(filepath):
    #fonction qui renvoie un dictionnaire avec comme cle le num du departement
    #et en item une liste des 3 couleurs [color_moy,color_min,color_max]
    data = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 8:
                code_dept = parts[0]
                color_moyenne = parts[3]
                color_min = parts[5]
                color_max = parts[7]
                if color_moyenne and color_moyenne[0] == '#':
                    if color_min and color_min[0] == '#':
                        if color_max and color_max[0] == '#':
                            data[code_dept] = [color_moyenne, color_min, color_max]                
    return data

def get_dept_code(record):
    try:
        code = str(record[3]).zfill(2)
        if code == '20':
            return code
        elif code in ['2A', '2B']:
             return code
        else:
             return code.zfill(2) 
    except IndexError:
        try:
             code = str(record[1]).zfill(2)
             if code == '20':
                 return code
             elif code in ['2A', '2B']:
                 return code
             return code.zfill(2)
        except IndexError:
            return None


def mercator(lat_degre,lon_degre):
    """
    fonction qui permet de faire la formule du projetcion de mercator
    """
    latitude = math.radians(lat_degre)
    lontitude = math.radians(lon_degre)
    X = lontitude
    Y = math.log(math.tan(latitude/2 + math.pi/4))
    return X, Y

def draw_terrain(scale=5):
    """
    affichage des départements
    """
    filepath="data annuelles/2020-temperature-data.txt"
    choix=input("A->Afficher les temperatures moyennes\nB->Afficher les temperatures minimales\nC->Afficher les temperatures maximales\n\n")
    cree_fenetre(largeur, hauteur)
    LISTE = [0,5,10,15,20,25,30,35,40,45]
    compteur = 0
    coeff = 20
    i = 20

    if choix=='A':
        index=0
    elif choix=='B':
        index=1
    elif choix=='C':
        index=2

    while i<= 800:
        if compteur in LISTE:
            texte(757,i -14, str(compteur)+"°C", couleur="red", taille=7)
            rectangle(780,i-coeff,800,i*2,remplissage = "blue")
        else:
            rectangle(780,i-coeff,800,i*2,remplissage = "blue")
        compteur +=1
        i += coeff
    data_temp=read_data(filepath)
    """
    lst_coords = []
    for shape in sf.shapes():
        pts = [mercator(latitude, lontitude) for (lontitude,latitude) in shape.points]
        parts = shape.parts[:]
        parts.append(len(pts))
        lst_coords.append((pts,parts))
    """
    lst_coords=[]
    for shape,record in zip(sf.shapes(), sf.records()):
            pts = [mercator(latitude, lontitude) for (lontitude,latitude) in shape.points]
            parts = shape.parts[:]
            parts.append(len(pts))
            lst_coords.append((pts,parts,record))


    # recupération des coordonnées maxmum et minmum
    xs = []
    ys = []

    for pts, _,_ in lst_coords:
        for x, y in pts:
            xs.append(x)
            ys.append(y)
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    for pts,parts,record in lst_coords:
        code_departement=record[0]#recuperation du code du departement
        colors=data_temp.get(code_departement)
        if colors:
            fill_color=colors[index]
        else:
            fill_color='white'#pas de données

    #for pts, parts in lst_coords:
        for i in range(len(parts) - 1):
                deb = parts[i]
                fin = parts[i + 1]
                poly = []
                for X,Y in pts[deb:fin]:
                    Xp = (X - minx) * taille -1400
                    Yp = (maxy - Y) * taille + 100
                    poly.append((Xp, Yp))
                polygone(poly, couleur='black', remplissage =fill_color)
    attend_ev()
    ferme_fenetre()
draw_terrain()

