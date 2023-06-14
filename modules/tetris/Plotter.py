import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

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
    
    @staticmethod
    def plot_model_rectangles(model, x_range, rects):
        # Generate x-values to plot the regression line
        x_values = np.linspace(x_range[0], x_range[1], 100)
        x = np.arange(x_range[0],x_range[1])
        y = model.predict(x)

        fig, ax = plt.subplots()
        ax.plot(x, y, label='Función Polinómica')

        for rectangle in rects:
            # Draw the rotated rectangle
            ax.add_patch(patches.Polygon(list(zip(rectangle.x_rotated, rectangle.y_rotated)), closed=True, facecolor='blue'))

        ax.set_xlim(left=min(x_values))
        ax.set_ylim(bottom=0)
        ax.set_aspect('equal')
        #ax.set_ylim([min(y) - max([rect.alto for rect in rectangulos]), max(y)])
        ax.legend()

        plt.show()

    @staticmethod
    def save_model_rectangles(model, x_range, rects, title, filename, grid=True):
        # Generate x-values to plot the regression line
        x_values = np.linspace(x_range[0], x_range[1], 100)
        x = np.arange(x_range[0],x_range[1])
        y = model.predict(x)

        fig, ax = plt.subplots()
        ax.plot(x, y, label='Función Polinómica')

        if(grid):
            # Ángulo en grados
            angulo = 60

            # Convertir el ángulo a radianes
            angulo_rad = np.deg2rad(angulo)

            # Calcular la pendiente a partir del ángulo
            pendiente = np.tan(angulo_rad)

            for pos in np.arange(-88, x_range[1]+20, 4.4):
                ax.axline((pos, 0), slope=pendiente, color='gray', linestyle='-')

        for rectangle in rects:
            # Draw the rotated rectangle
            ax.add_patch(patches.Polygon(list(zip(rectangle.x_rotated, rectangle.y_rotated)), closed=True, facecolor='orange'))

        ax.set_xlim(left=min(x_values))
        ax.set_ylim(bottom=0)
        ax.set_aspect('equal')
        #ax.set_ylim([min(y) - max([rect.alto for rect in rectangulos]), max(y)])
        ax.legend()
        ax.set_title(title + ': ' + str(len(rects)) + ' equipos ubicados')
        plt.savefig(filename)