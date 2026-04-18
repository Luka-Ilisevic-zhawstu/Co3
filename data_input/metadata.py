"""
Elements that always stay the same:
-> Printer Dimensions
-> Objects type, dimensions and number

"""


from model.shapes import Cube, Pyramid, Sphere

W, D, H = 38.0, 28.4, 38.0

objects = [

    Cube(a = 5.0),

    Cube(a = 5.0),

    Cube(a = 5.0),

    Cube(a = 5.0),

    Cube(a = 15.0),

    Sphere(r = 3.0),

    Sphere(r = 3.0),

    Sphere(r = 8.0),

    Pyramid(b = 4.0, h = 10.0),

    Pyramid(b = 5.0, h = 10.0),

    Pyramid(b = 5.0, h = 10.0)
    
    ]