from fltk import *
import shapefile
import math

colors = [
    "#0D0887", "#1B068E", "#290593", "#37049A", "#44039E", "#5102A3",
    "#5E01A6", "#6B01A6", "#7701A8", "#8402A8", "#900DA4", "#9C179E",
    "#A62098", "#B12A90", "#BB3488", "#C43E7F", "#CC4977", "#D3516C",
    "#DA5A60", "#DF6353", "#E46C46", "#E97538", "#ED7E2B", "#F0851D",
    "#F48C12", "#F7930A", "#F99A05", "#FBA305", "#FDAB0D", "#FBB41B",
    "#F9BD2A", "#F6C53A", "#F4CD4A", "#F1D45A", "#EEDD6B", "#EAE76F"
]
largeur = 800
hauteur = 720
taille = 1600
sf = shapefile.Reader("departement/departements-20180101")
shape = sf.shape()

def read_data(filepath):
    #fonction qui renvoie un dictionnaire avec comme cle le num du departement
    #et en item une liste [color_moy,color_min,color_max]
    data = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            
            if len(parts) >= 8:
                code_dept = parts[0]
                #assignation des couleurs selon la position de leur information 
                #dans le fichier(similaire a leur 'colonne')
                color_moyenne = parts[3]
                color_min = parts[5]
                color_max = parts[7]
                #vérifie que nos variables ne sont pas vides, et son bien des couleurs hexadecimales(commence par #)
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

def draw_dom():
    rect_x1, rect_y1 = 30, 300
    rect_x2, rect_y2 = 200, 550

    box_w = (rect_x2 - rect_x1) // 2
    box_h = (rect_y2 - rect_y1) // 3
    dom_list = ["971", "972", "973", "974", "975", "976"]
    offsets = [
        (0, 0),
        (1, 0), 
        (0, 1),  
        (1, 1),  
        (1, 2),
        (0, 2),  
    ]
    zoom_dom = 800

    records = sf.records()
    shapes = sf.shapes()

    for (shape, rec) in zip(shapes, records):
        dep_code = rec[0]

        if dep_code not in dom_list:
            continue

        i = dom_list.index(dep_code)
        ox, oy = offsets[i]
        offset_x = rect_x1 + ox * box_w + 10
        offset_y = rect_y1 + oy * box_h + 10

        pts = []
        for (lon, lat) in shape.points:
            X, Y = mercator(lat, lon)
            pts.append((X, Y))

        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)

        parts = shape.parts[:]
        parts.append(len(pts))

        for i in range(len(parts) - 1):
            deb = parts[i]
            fin = parts[i+1]

            poly = []
            for X, Y in pts[deb:fin]:
                Xp = (X - minx) * zoom_dom + offset_x
                Yp = (maxy - Y) * zoom_dom + offset_y
                poly.append((Xp, Yp))

            polygone(poly, couleur='black', remplissage='cyan')


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
    while compteur != 36:
        if compteur in LISTE:
            texte(757,i -14, str(compteur)+"°C", couleur="red", taille=7)
            rectangle(780,i-coeff,800,i*2,remplissage = colors[compteur])
        else:
            rectangle(780,i-coeff,800,i*2,remplissage = colors[compteur])
        compteur +=1
        i += coeff
    data_temp=read_data(filepath)
    lst_coords = []
    for shape,record in zip(sf.shapes(),sf.records()):
        pts = [mercator(latitude, lontitude) for (lontitude,latitude) in shape.points]
        parts = shape.parts[:]
        parts.append(len(pts))
        lst_coords.append((pts,parts,record))
    

    # recupération des coordonnées maxmum et minmum
    xs = []
    ys = []
    for pts, _, _ in lst_coords:
        for x, y in pts:
            xs.append(x)
            ys.append(y)
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    for pts,parts,record in lst_coords:
        code_departement=record[0]#recuperation du code du departement
        couleur_departement=data_temp.get(code_departement)
        if couleur_departement:
            fill_color=couleur_departement[index]
        else:
            fill_color='white'#pas de données
        for i in range(len(parts) - 1):
                deb = parts[i]
                fin = parts[i + 1]
                poly = []
                for X,Y in pts[deb:fin]:
                    Xp = (X - minx) * taille -1400
                    Yp = (maxy - Y) * taille + 100
                    poly.append((Xp, Yp))
                polygone(poly, couleur='black', remplissage =fill_color)
    rectangle(30, 300, 200, 550, remplissage = 'white', couleur = 'black')
    rectangle(50,700,750,685)
    x2 = 57
    cercle(x2, 692, 7.5,remplissage = "blue",tag="zone")
    while True:
        ev = donne_ev()
        if type_ev(ev) == 'ClicGauche':
            x,y = abscisse(ev), ordonnee(ev)
            if 50 <= x <= 750 and 685<= y <= 700:
                print(x)
            if 50 <= x <= 150 and 685<= y <= 700:
                print("année 1")
            if 150 <= x <= 250 and 685<= y <= 700:
                print("année 2")
            if 250 <= x <= 350 and 685<= y <= 700:
                print("année 3")
            if 350 <= x <= 450 and 685<= y <= 700:
                print("année 4")
            if 450 <= x <= 550 and 685<= y <= 700:
                print("année 5")
            if 550 <= x <= 650 and 685<= y <= 700:
                print("année 6")
            if 650 <= x <= 750 and 685<= y <= 700:
                print("année 7")
        elif type_ev(ev) == 'Touche':
            tch = touche(ev)
            if tch == 'Right':
                deplace("zone",5,0)
            if tch == 'Left':
                deplace('zone',-5,0)
        draw_dom()
        mise_a_jour()
    attend_ev()
    ferme_fenetre()
draw_terrain()