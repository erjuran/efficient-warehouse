from Polynomial import Polynomial, PolyRegressor
from Rectangle import Rectangle
import matplotlib.pyplot as plt
import matplotlib.patches as patches

patio1a = Polynomial((0, 250),'math_models/Pulmon1A.joblib')
model = patio1a.model


def rect_fits_poly(corners, patio):
    for corner in corners:
        x_corner = corner[0]
        y_corner = corner[1]
        #print(corner)

        if(x_corner < 0 or y_corner < 0):
            return False
        
        if(x_corner > patio.x_range[1]):
            return False
        
        y_model = patio.model.predict(x_corner)
        if(y_model < y_corner):
            return False
        
    return True

x_values = patio1a.x_values
y_values = patio1a.y_values

rec1 = Rectangle(4, 25, -30)
rec2 = Rectangle(5, 13, -30)
rec3 = Rectangle(8, 20, -30)

unlocated_recs = [rec1,rec2,rec3]
located_recs = []

#for rec in unlocated_recs:
#    print(rec.rotated_corners)
index = 0

for rect in unlocated_recs:
    #for y_patio in y_values:


    index += 1
    #print(f'\n\nRECT {index}\n')

    for x_patio in x_values:

        fits = False
        overlap = False

        corners = rect.rotated_corners
        left_corner = corners[0]

        # Check if rectangle fits inside the plane
        fits = rect_fits_poly(corners, patio1a)
        #if(fits): print(f'Rect {index}: Fit!')

        if(len(located_recs)>0):
            # Compare the rectangles
            for other in located_recs:
                if(rect.overlap(other)):
                    #print(f'Rect {index}: Overlap!')
                    overlap = True
                    break
        else:
            overlap = False
        
        if(fits and not overlap):
            # Rectangle located
            #print(f'Rect {index}: Located!')
            located_recs.append(rect)
            #unlocated_recs.remove(rect)
            break
        else:
            x_diff = abs(x_patio - left_corner[0])
            # Move the X coordinates a bit a try again
            
            rect.update_coords(x_diff,0)
            #print(f'Rect {index}: Updating coords')


def plot_rectangles(rectangles):
    figure = plt.figure()
    ax = figure.add_subplot(111)

    for rectangle in rectangles:
        # Draw the rotated rectangle
        ax.add_patch(patches.Polygon(list(zip(rectangle.x_rotated, rectangle.y_rotated)), closed=True, facecolor='blue'))

    # Configure the plot limits
    max_dimension = max(max(rectangle.width, rectangle.height) for rectangle in rectangles)
    ax.set_xlim(-max_dimension, max_dimension)
    ax.set_ylim(-max_dimension, max_dimension)

    # Show the plot
    plt.axis('equal')
    plt.show()

'''
index = 0
for rec in unlocated_recs:
    index += 1
    print(f'RECT {index}')
    #print(rec.rotated_corners)
    print(rec.x_rotated)
    print(rec.y_rotated)
'''


#print(located_recs)
plot_rectangles(located_recs)