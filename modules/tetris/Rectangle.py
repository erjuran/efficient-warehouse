import math
import numpy as np

class Rectangle:
    def __init__(self, width, height, angle, summary=None):
        self.summary = summary

        if(width > height):
            self.width = height
            self.height = width
        else:
            self.width = width
            self.height = height
            
        self.angle = angle
        self.x_rotated = None
        self.y_rotated = None
        self.rotated_corners = None
        self.initial_coords = None
        self.rotate()

    def rotate(self):
        # Calculate the coordinates of the unrotated rectangle vertices
        x = [0, self.width, self.width, 0]
        y = [0, 0, self.height, self.height]

        # Apply rotation to the rectangle
        angle_radians = math.radians(self.angle)
        cosine = math.cos(angle_radians)
        sine = math.sin(angle_radians)
        self.x_rotated = [xi * cosine - yi * sine for xi, yi in zip(x, y)]
        self.y_rotated = [xi * sine + yi * cosine for xi, yi in zip(x, y)]

        # Get the coordinates of the rotated corners
        self.rotated_corners = []
        for i in range(4):
            self.rotated_corners.append((self.x_rotated[i], self.y_rotated[i]))
        
        # Realizar la traslación
        x_min = min(self.x_rotated)
        y_min = min(self.y_rotated)
        self.x_rotated = [x - x_min for x in self.x_rotated]
        self.y_rotated = [y - y_min for y in self.y_rotated]
        self.rotated_corners = [(x - x_min, y - y_min) for x, y in self.rotated_corners]
        self.initial_coords = self.rotated_corners.copy()

        #print(self.rotated_corners)
        #print(self.x_rotated)
        #print(self.y_rotated)
    
    def update_coords(self, x_diff, y_diff):

        if(x_diff > 0):
            self.x_rotated = [x + x_diff for x in self.x_rotated]
        

        if(y_diff > 0):
            self.rotated_corners = self.initial_coords
            self.y_rotated = [coord[1] for coord in self.rotated_corners]
            self.x_rotated = [coord[0] for coord in self.rotated_corners]
            self.y_rotated = [y + y_diff for y in self.y_rotated]

        self.rotated_corners = [(x + x_diff, y + y_diff) for x, y in self.rotated_corners]


    def overlap(self, other):
        rect1 = self.rotated_corners
        rect2 = other.rotated_corners

        if self._check_projection(rect1, rect2) and self._check_projection(rect2, rect1):
            return True

        return False

    def _check_projection(self, rect1, rect2):
        for i in range(4):
            axis = self._get_axis(rect1, i)

            min_r1, max_r1 = self._project(rect1, axis)
            min_r2, max_r2 = self._project(rect2, axis)

            if not (max_r2 >= min_r1 and max_r1 >= min_r2):
                return False

        return True

    def _get_axis(self, rect, i):
        p1 = rect[i]
        p2 = rect[(i + 1) % 4]

        edge = np.array([p2[0] - p1[0], p2[1] - p1[1]])
        axis = np.array([-edge[1], edge[0]])
        axis /= np.linalg.norm(axis)

        return axis

    def _project(self, rect, axis):
        min_val = np.dot(rect[0], axis)
        max_val = min_val

        for i in range(1, 4):
            val = np.dot(rect[i], axis)
            min_val = min(min_val, val)
            max_val = max(max_val, val)

        return min_val, max_val




'''
    def overlap(self, other):

        rect1 = self.rotated_corners
        rect2 = other.rotated_corners

        return self._compare_corners(rect1, rect2) or self._compare_corners(rect2, rect1)

    def _compare_corners(self, rect1, rect2):
        x_other = [corner[0] for corner in rect2]
        y_other = [corner[1] for corner in rect2]

        for corner_self in rect1:
            x_self = corner_self[0]
            y_self = corner_self[1]
            # Check if one rectangle corner is inside the other on X coord
            if(min(x_other) < x_self < max(x_other) and min(y_other) < y_self < max(y_other)):
                return True
        
        return False
'''


                




