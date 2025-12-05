from fltk import *
import shapefile
import math



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
    while i<= 800:
        if compteur in LISTE:
            texte(757,i -14, str(compteur)+"°C", couleur="red", taille=7)
            rectangle(780,i-coeff,800,i*2,remplissage = "blue")
        else:
            rectangle(780,i-coeff,800,i*2,remplissage = "blue")
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
    attend_ev()
    ferme_fenetre()
draw_terrain()