import os
# Lister les dossiers
def files_rec(chemin, r):
    t1 = [x[0].replace(r, "") for x in os.walk(chemin)]
    t2 = [os.path.join(x[0], y).replace(r, "") for x in os.walk(chemin) for y in x[2]]
    return [t1, t2]

