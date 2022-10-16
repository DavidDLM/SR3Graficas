from gl import Renderer, _color_, V3, V2

width = 1024
height = 512  # 512

rend = Renderer(width, height)

rend.glLoadModel("Dumbbell.obj",
                 translate=V3(width/2, -height, 0),
                 scale=V3(5, 5, 5))

rend.write("SR3.bmp")
