# OBJ.py
# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Carlos Alonso

class Obj(object):
    def __init__(init, filename):
        with open(filename, "r") as file:
            init.lines = file.read().splitlines()

        init.vertices = []
        init.texcoords = []
        init.normals = []
        init.faces = []

        for line in init.lines:
            try:
                prefix, value = line.split(' ', 1)
            except:
                continue

            if prefix == 'v':  # Vertices
                init.vertices.append(list(map(float, value.split(' '))))
            elif prefix == 'vt':
                init.texcoords.append(list(map(float, value.split(' '))))
            elif prefix == 'vn':
                init.normals.append(list(map(float, value.split(' '))))
            elif prefix == 'f':
                init.faces.append([list(map(int, vert.split('/')))
                                  for vert in value.split(' ')])
