

class Sorter:

    def __init__(self, unlocated_recs, place):
        self.unlocated_recs = unlocated_recs
        self.located_recs = []
        self.place = place
        self.model = place.model
        
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
    
    def locate_rects(self):
        index = 0
        x_values = self.place.x_values

        for rect in self.unlocated_recs:
            #for y_patio in y_values:

            index += 1
            #print(f'\n\nRECT {index}\n')

            for x_patio in x_values:

                fits = False
                overlap = False

                corners = rect.rotated_corners
                left_corner = corners[0]

                # Check if rectangle fits inside the plane
                fits = self._rect_fits_poly(corners, self.place)
                #if(fits): print(f'Rect {index}: Fit!')

                if(len(self.located_recs)>0):
                    # Compare the rectangles
                    for other in self.located_recs:
                        if(rect.overlap(other)):
                            #print(f'Rect {index}: Overlap!')
                            overlap = True
                            break
                else:
                    overlap = False
                
                if(fits and not overlap):
                    # Rectangle located
                    #print(f'Rect {index}: Located!')
                    self.located_recs.append(rect)
                    #unlocated_recs.remove(rect)
                    break
                else:
                    x_diff = abs(x_patio - left_corner[0])
                    # Move the X coordinates a bit a try again
                    
                    rect.update_coords(x_diff,0)
                    #print(f'Rect {index}: Updating coords')
        
        return self.located_recs