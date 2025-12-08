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
sf = shapefile.Reader("departements-20180101")
shape = sf.shape()

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
    cree_fenetre(largeur, hauteur)


    LISTE = [0,5,10,15,20,25,30,35,40,45]
    compteur = 0
    coeff = 20
    i = 20
    while compteur != 36:
        if compteur in LISTE:
            texte(757,i -14, str(compteur)+"°C", couleur="red", taille=7)
            rectangle(780,i-coeff,800,i*2,remplissage = colors[compteur])
        else:
            rectangle(780,i-coeff,800,i*2,remplissage = colors[compteur])
        compteur +=1
        i += coeff
    lst_coords = []
    for shape in sf.shapes():
        pts = [mercator(latitude, lontitude) for (lontitude,latitude) in shape.points]
        parts = shape.parts[:]
        parts.append(len(pts))
        lst_coords.append((pts,parts))
    

    # recupération des coordonnées maxmum et minmum
    xs = []
    ys = []
    for pts, _ in lst_coords:
        for x, y in pts:
            xs.append(x)
            ys.append(y)
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    for pts, parts in lst_coords:
        for i in range(len(parts) - 1):
                deb = parts[i]
                fin = parts[i + 1]
                poly = []
                for X,Y in pts[deb:fin]:
                    Xp = (X - minx) * taille -1400
                    Yp = (maxy - Y) * taille + 100
                    poly.append((Xp, Yp))
                polygone(poly, couleur='black', remplissage = 'blue')

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
        elif type_ev(ev) == 'Right':
            x2+= 5
            deplace("zone",x2,692)


            

        mise_a_jour()
    attend_ev()
    ferme_fenetre()
draw_terrain()


