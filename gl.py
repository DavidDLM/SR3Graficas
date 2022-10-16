# SR3
# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Carlos Alonso / Ing. Dennis Aldana
import conversions as conv
import random
import struct
from collections import namedtuple
import matMath as mt
from obj import Obj
from math import cos, sin

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])


def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    # 2 bytes
    return struct.pack('=h', w)


def dword(d):
    # 4 bytes
    return struct.pack('=l', d)


def _color_(r, g, b):
    return bytes([int(b*255),
                  int(g*255),
                  int(r*255)])


# Colores default
white = _color_(1, 1, 1)
black = _color_(0, 0, 0)


class Renderer(object):
    def __init__(init, width, height):
        init.width = width
        init.height = height
        init.clearColor = black
        init.currColor = white
        init.glViewPort(0, 0, init.width, init.height)
        init.glClear()

    # El area donde se v1 a dibujar
    def glCreateWindow(init, width, height):
        init.width = width
        init.height = height
        init.glClear()

    # Utiliza las coordenadas
    def glViewPort(init, x, y, width, height):
        init.viewportX = x
        init.viewportY = y
        init.viewportWidth = width
        init.viewportHeight = height

    # Limpia los pixeles de la pantalla poniendolos en blanco o negro
    def glClear(init):
        init.framebuffer = [[init.clearColor for y in range(
            init.height)]for x in range(init.width)]

    # Coloca color de fondo
    def glClearColor(init, r, g, b):
        init.clearColor = _color_(r, g, b)

    # Dibuja un punto
    def glVertex(init, vertexX, vertexY, color=None):
        x = int((vertexX+1)*(init.viewportWidth/2)+init.viewportX)
        y = int((vertexY+1)*(init.viewportHeight/2)+init.viewportY)
        init.glPoint(x, y, color)

    def glPoint(init, x, y, color=None):
        # Coordenadas de la ventana
        if (0 <= x < init.width) and (0 <= y < init.height):
            init.framebuffer[x][y] = color or init.currColor

    # Se establece el color de dibujo, si no tiene nada se dibuja blanco
    def glColor(init, r, g, b):
        init.currColor = _color_(r, g, b)

    def glClearViewPort(init, color=None):
        for x in range(init.viewportX, init.viewportX + init.viewportWidth):
            for y in range(init.viewportY, init.viewportY + init.viewportHeight):
                init.glVertex(x, y, color)

    # Algoritmo de Bresenham para creación de lineas
    def glLine(init, v1, v2, color=None):
        # Bresenham line algorithm
        # y = m * x + b
        x1 = int(v1.x)
        x2 = int(v2.x)
        y1 = int(v1.y)
        y2 = int(v2.y)

        # Si el punto0 es igual al punto 1, dibujar solamente un punto
        if x1 == x2 and y1 == y2:
            init.glPoint(x1, y1, color)
            return

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        steep = dy > dx

        # Si la linea tiene pendiente mayor a 1 o menor a -1
        # intercambio las x por las y, y se dibuja la linea
        # de manera vertical
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Si el punto inicial X es mayor que el punto final X,
        # intercambio los puntos para siempre dibujar de
        # izquierda a derecha
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)

        offset = 0
        limit = 0.5
        m = dy / dx
        y = y1

        for x in range(x1, x2 + 1):
            if steep:
                # Dibujar de manera vertical
                init.glPoint(y, x, color)
            else:
                # Dibujar de manera horizontal
                init.glPoint(x, y, color)

            offset += m

            if offset >= limit:
                if y1 < y2:
                    y += 1
                else:
                    y -= 1

                limit += 1

    def glCreateRotationMatrix(init, rotate=V3(0, 0, 0)):

        # https://howthingsfly.si.edu/flight-dynamics/roll-pitch-and-yaw
        # Rotation around the front-to-back axis is called roll.
        # Rotation around the side-to-side axis is called pitch.
        # Rotation around the vertical axis is called yaw.
        pitch = conv.degrees_to_radians(rotate.x)
        yaw = conv.degrees_to_radians(rotate.y)
        roll = conv.degrees_to_radians(rotate.z)

        # Matrices de rotacion proporcionadas por Ing. Dennis Aldana
        rotationX = [[1, 0, 0, 0],
                     [0, cos(pitch), -sin(pitch), 0],
                     [0, sin(pitch), cos(pitch), 0],
                     [0, 0, 0, 1]]

        rotationY = [[cos(yaw), 0, sin(yaw), 0],
                     [0, 1, 0, 0],
                     [-sin(yaw), 0, cos(yaw), 0],
                     [0, 0, 0, 1]]

        rotationZ = [[cos(roll), -sin(roll), 0, 0],
                     [sin(roll), cos(roll), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]]

        return mt.multMatrix(mt.multMatrix(rotationX, rotationY), rotationZ)

    def glCreateObjectMatrix(init, translate=V3(0, 0, 0), rotate=V3(0, 0, 0), scale=V3(1, 1, 1)):

        translateMatrix = [[1, 0, 0, translate.x],
                           [0, 1, 0, translate.y],
                           [0, 0, 1, translate.z],
                           [0, 0, 0, 1]]

        rotationMatrix = init.glCreateRotationMatrix(rotate)

        scaleMatrix = [[scale.x, 0, 0, 0],
                       [0, scale.y, 0, 0],
                       [0, 0, scale.z, 0],
                       [0, 0, 0, 1]]

        return mt.multMatrix(mt.multMatrix(translateMatrix, rotationMatrix), scaleMatrix)

    def glTransform(init, vertex, matrix):

        aV = V4(vertex[0], vertex[1], vertex[2], 1)
        transV = mt.vectMultMatrix(matrix, aV)

        transV = V3(transV[0] / transV[3],
                    transV[1] / transV[3],
                    transV[2] / transV[3])

        return transV

    def glLoadModel(init, filename, translate=V3(0, 0, 0), rotate=V3(0, 0, 0), scale=V3(1, 1, 1)):
        model = Obj(filename)
        modelMatrix = init.glCreateObjectMatrix(translate, rotate, scale)

        for face in model.faces:
            vertCount = len(face)
            # Relleno con triangulos de colores
            v0 = model.vertices[face[0][0] - 1]
            v1 = model.vertices[face[1][0] - 1]
            v2 = model.vertices[face[2][0] - 1]

            v0 = init.glTransform(v0, modelMatrix)
            v1 = init.glTransform(v1, modelMatrix)
            v2 = init.glTransform(v2, modelMatrix)

            init.glTriangle_standard(v0, v1, v2, _color_(random.random(),
                                                         random.random(),
                                                         random.random()))

    def glTriangle_standard(init, A, B, C, color=None):
        # Para asegurarnos que estamos trabajando con el orden correcto de los vertices
        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        def flatBottomTriangle(v1, v2, v3):
            try:
                m21 = (v2.x - v1.x) / (v2.y - v1.y)
                m31 = (v3.x - v1.x) / (v3.y - v1.y)
            except:
                pass
            else:
                x1 = v2.x
                x2 = v3.x
                for y in range(int(v2.y), int(v1.y)):
                    init.glLine(V2(int(x1), y), V2(int(x2), y), color)
                    x1 += m21
                    x2 += m31

        def flatTopTriangle(v1, v2, v3):
            try:
                m31 = (v3.x - v1.x) / (v3.y - v1.y)
                m32 = (v3.x - v2.x) / (v3.y - v2.y)
            except:
                pass
            else:
                x1 = v1.x
                x2 = v2.x

                for y in range(int(v1.y), int(v3.y), -1):
                    init.glLine(V2(int(x1), y), V2(int(x2), y), color)
                    x1 -= m31
                    x2 -= m32

        if B.y == C.y:
            # Parte plana abajo
            flatBottomTriangle(A, B, C)
        elif A.y == B.y:
            # Parte plana arriba
            flatTopTriangle(A, B, C)
        else:
            # Dibujo ambos tipos de triangulos
            # Teorema de intercepto
            D = V2(A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x), B.y)
            flatBottomTriangle(A, B, D)
            flatTopTriangle(B, D, C)

    # Crea un archivo BMP

    def write(init, filename):
        with open(filename, "bw") as file:
            # pixel header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + init.width * init.height * 3))
            file.write(word(0))
            file.write(word(0))
            file.write(dword(14 + 40))

            # informacion del header
            file.write(dword(40))
            file.write(dword(init.width))
            file.write(dword(init.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(init.width * init.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # pixel data
            for y in range(init.height):
                for x in range(init.width):
                    file.write(init.framebuffer[x][y])
