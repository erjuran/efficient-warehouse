from Polynomial import Polynomial, PolyRegressor
from Rectangle import Rectangle
from Plotter import Plotter
from Sorter import Sorter
from DualSorter import DualSorter

placeA = Polynomial((0, 250),'math_models/Pulmon1A.joblib')
placeB = Polynomial((0, 250),'math_models/Pulmon1B.joblib')


unlocated_rects = []
for i in range(10):

    rec1 = Rectangle(13, 18, -30)
    rec2 = Rectangle(9, 13, -30)
    rec3 = Rectangle(5, 20, -30)
    rec4 = Rectangle(12, 15, -30)

    unlocated_rects += [rec1, rec2, rec3, rec4]

unlocated_rects.append(Rectangle(2, 8, -30))

''' One place test
sorter = Sorter(unlocated_rects, placeA)
located_rects = sorter.locate_rects()

#Plotter.plot_rectangles(located_rects)
Plotter.plot_model_rectangles(place.model, (0,250), located_rects)
'''

# Dual place test
sorter = DualSorter(unlocated_rects,placeA,placeB)
placeA_recs, placeB_recs = sorter.locate_rects()

#Plotter.plot_model_rectangles(placeA.model, (0,250), placeA_recs)
#Plotter.plot_model_rectangles(placeB.model, (0,250), placeB_recs)

Plotter.save_model_rectangles(placeA.model, (0,250), placeA_recs, "Pulmon 1A Test", "tetrisPulmon1A.png")
Plotter.save_model_rectangles(placeB.model, (0,250), placeB_recs, "Pulmon 1B Test", "tetrisPulmon1B.png")


