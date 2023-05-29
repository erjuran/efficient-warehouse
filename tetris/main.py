from Polynomial import Polynomial, PolyRegressor
from Rectangle import Rectangle
from Plotter import Plotter
from Sorter import Sorter

place = Polynomial((0, 250),'math_models/Pulmon1A.joblib')

unlocated_rects = []
for i in range(6):

    rec1 = Rectangle(13, 18, -30)
    rec2 = Rectangle(9, 13, -30)
    rec3 = Rectangle(5, 20, -30)
    rec4 = Rectangle(12, 15, -30)

    unlocated_rects += [rec1, rec2, rec3, rec4]

unlocated_rects.append(Rectangle(2, 8, -30))

sorter = Sorter(unlocated_rects, place)
located_rects = sorter.locate_rects()

""" index = 0
for rect in located_rects:
    xs = max(rect.x_rotated)
    if(xs > 500):
        print(xs)
        print(f'Index:{index+1}')
        print(rect.rotated_corners)
    index+=1 """

Plotter.plot_rectangles(located_rects)
#Plotter.plot_rectangles(unlocated_rects)


