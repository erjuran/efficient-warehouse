import math
import numpy as np

class DualSorter:

    def __init__(self, unlocated_recs, placeA, placeB, slot_size=0):
        self.unlocated_recs = unlocated_recs
        self.placeA_recs = []
        self.placeB_recs = []
        #self.place = single_place
        #self.model = single_place.model

        self.slot_size = slot_size
        self.placeA = placeA
        self.placeB = placeB
        self.monitor = 119
        
    def _rect_fits_poly(self, corners, patio):
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
    
    def _assign_coords(self,index, place, x_values, y_values, rect, located_recs, located=False):
        
        #if(index == self.monitor): print(x_values)
        '''
        if(self.slot_size > 0):
            
            # Ángulo en grados
            angulo = 60

            # Convertir el ángulo a radianes
            angulo_rad = np.deg2rad(angulo)

            # Calcular la pendiente a partir del ángulo
            pendiente = np.tan(angulo_rad)

            corners = rect.rotated_corners
            left_corner = corners[0]
            
            #x_init = self._move_point_to_align(left_corner[0], self.slot_size)
            x_delta = left_corner[1]/pendiente

        else:
            x_delta = 0
        
        '''
        
        for y_patio in y_values:

            if(self.slot_size > 0):
            
                # Ángulo en grados
                angulo = 60

                # Convertir el ángulo a radianes
                angulo_rad = np.deg2rad(angulo)

                # Calcular la pendiente a partir del ángulo
                pendiente = np.tan(angulo_rad)

                corners = rect.rotated_corners
                left_corner = corners[0]
                
                #x_init = self._move_point_to_align(left_corner[0], self.slot_size)
                x_delta = left_corner[1]/pendiente

            else:
                x_delta = 0

            if(not located):

                added_delta=False

                for x_patio in x_values:

                    if(not added_delta and self.slot_size > 0):

                        # Ajustar coordenadas iniciales al primer carril más cercano
                        x_probable = left_corner[0] + x_delta
                        for x_resta in x_values:
                            if(x_probable - x_resta < 0):
                                break
                            else:
                                x_probable -= x_resta

                        #rect.update_coords(x_delta,0)
                        rect.update_coords(x_probable, 0)
                        added_delta = True
                    
                    fits = False
                    overlap = False

                    corners = rect.rotated_corners
                    left_corner = corners[0]

                    # Check if rectangle fits inside the plane
                    fits = self._rect_fits_poly(corners, place)
                    if(fits):
                        if(index == self.monitor): 
                            #print(f'Fit!')
                            #print(f'X:{x_patio}, Y:{y_patio}')
                            pass

                        if(len(located_recs)>0):
                            # Compare the rectangles
                            for other in located_recs:
                                if(rect.overlap(other)):
                                    if(index == self.monitor):  
                                        #print(f'Overlap!') 
                                        #print(rect.rotated_corners)
                                        pass
                                    overlap = True
                                    break
                        else:
                            overlap = False
                        
                        if(not overlap):
                            # Rectangle located
                            #print(f'Rect {index}: Located!')
                            located_recs.append(rect)
                            located = True
                            #unlocated_recs.remove(rect)
                            break
                        else:
                            
                            if(self.slot_size > 0):
                                x_diff = self.slot_size
                            else:
                                x_diff = abs(x_patio - left_corner[0])
                            # Move the X coordinates a bit a try again
                            rect.update_coords(x_diff,0)
                            #print(f'Rect {index}: Updating coords')

                    else:
                        if(self.slot_size > 0):
                            x_diff = self.slot_size
                        else:
                            x_diff = abs(x_patio - left_corner[0])
                        # Move the X coordinates a bit a try again
                        rect.update_coords(x_diff,0)
                        #print(f'Rect {index}: Updating coords')
                
            if(not located):
                y_diff = abs(y_patio - left_corner[1])
                # Move the Y coordinates a bit a try again
                
                #if(index == monitor):
                #    print(f'Rect {index}: Updating coords in Y')
                #    print(rect.rotated_corners)
                rect.update_coords(0, y_diff)
            else:
                break
    
        return located
    
    def locate_rects(self):
        index = 0

        placeA_x_values = self.placeA.x_values
        placeB_x_values = self.placeB.x_values
        placeA_y_values = self.placeA.y_values
        placeB_y_values = self.placeB.y_values

        for rect in self.unlocated_recs:
            index += 1
            
            if(index == self.monitor):
                print(f'\n\nRECT {index}\n')
                print(f'ORIGINAL:{rect.rotated_corners}')
                
            if((index-1) % 2 == 0):
                place = self.placeA
                x_values = placeA_x_values
                y_values = placeA_y_values
                located_recs = self.placeA_recs
            else:
                place = self.placeB
                x_values = placeB_x_values
                y_values = placeB_y_values
                located_recs = self.placeB_recs

            located = self._assign_coords(index, place, x_values, y_values, rect, located_recs)
            
            if(not located): 
                # If couldn't locate on one place, try the other
                if((index-1) % 2 == 0): # Place A
                    located = self._assign_coords(index, self.placeB, placeB_x_values, placeB_y_values, rect, self.placeB_recs)
                else: # Place B
                    located = self._assign_coords(index, self.placeA, placeA_x_values, placeA_y_values, rect, self.placeA_recs)

                #if(index == self.monitor):
                #    print(f'PLACE A-Y:{placeA_y_values}')
                #    print(f'PLACE B-Y:{placeB_y_values}')

            if(index == self.monitor): 
                print(f'LAST: {rect.rotated_corners}, WIDTH:{rect.width}, HEIGHT:{rect.height}')

        loc_recs = len(self.placeA_recs) + len(self.placeB_recs)
        print(f'No ubicados: {len(self.unlocated_recs) - loc_recs}')
        print(f'Ubicados: {loc_recs}')
        print(f'Patio A {len(self.placeA_recs)}')
        print(f'Patio B {len(self.placeB_recs)}')
        return self.placeA_recs, self.placeB_recs
    
    def _move_point_to_align(self,point_x, line_spacing):
        #line_spacing = 4.4
        closest_line_x = round(point_x / line_spacing) * line_spacing
        difference = closest_line_x - point_x
        return difference
