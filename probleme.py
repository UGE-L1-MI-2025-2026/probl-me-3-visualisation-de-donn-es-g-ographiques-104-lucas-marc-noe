from fltk import *
import shapefile

largeur = 800
hauteur = 600
taille = 10
sf = shapefile.Reader("departement/departements-20180101")
shape = sf.shape(9)
print(shape.parts)
def draw_terrain(scale=5):
    cree_fenetre(largeur, hauteur)

    pts = shape.points
    minx, miny, maxx, maxy = shape.bbox

    for part in shape.parts:
        polygone_pts = []

        for x, y in pts[part:]:
            X = (x - minx) * taille * scale
            Y = (maxy - y) * taille * scale
            polygone_pts.append((X, Y))
            if (part != shape.parts[-1]) and (len(polygone_pts) > 1) and (pts.index((x, y)) == shape.parts[shape.parts.index(part)+1]-1):
                break
        polygone(polygone_pts, couleur='black', remplissage = 'blue')

    attend_ev()
    ferme_fenetre()

draw_terrain()
