from Polynomial import Polynomial, PolyRegressor
from Rectangle import Rectangle
from Plotter import Plotter
from Sorter import Sorter

place = Polynomial((0, 250),'math_models/Pulmon1A.joblib')

rec1 = Rectangle(4, 25, -30)
rec2 = Rectangle(5, 13, -30)
rec3 = Rectangle(8, 20, -30)

unlocated_rects = [rec1, rec2, rec3]

sorter = Sorter(unlocated_rects, place)
located_rects = sorter.locate_rects()

Plotter.plot_rectangles(located_rects)


