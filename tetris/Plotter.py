import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Plotter:

    @staticmethod
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