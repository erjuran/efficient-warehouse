

class DualSorter:

    def __init__(self, unlocated_recs, placeA, placeB):
        self.unlocated_recs = unlocated_recs
        self.placeA_recs = []
        self.placeB_recs = []
        #self.place = single_place
        #self.model = single_place.model

        self.placeA = placeA
        self.placeB = placeB
        
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
    
    # def _assign_coords(self):
    #     if(not located):
    #         for x_patio in x_values:

    #             fits = False
    #             overlap = False

    #             corners = rect.rotated_corners
    #             left_corner = corners[0]

    #             # Check if rectangle fits inside the plane A first, then checks the plane B
    #             fits = self._rect_fits_poly(corners, place)
    #             if(fits):
    #                 #if(index == monitor): print(f'Fit!')

    #                 if(len(located_recs)>0):
    #                     # Compare the rectangles
    #                     for other in located_recs:
    #                         if(rect.overlap(other)):
    #                             overlap = True
    #                             break
    #                 else:
    #                     overlap = False
                    
    #                 if(not overlap):
    #                     located_recs.append(rect)
    #                     located = True
    #                     break
    #                 else:
    #                     x_diff = abs(x_patio - left_corner[0])
    #                     # Move the X coordinates a bit a try again
    #                     rect.update_coords(x_diff,0)

    #             else:
    #                 x_diff = abs(x_patio - left_corner[0])
    #                 # Move the X coordinates a bit a try again
    #                 rect.update_coords(x_diff,0)
            
    #     if(not located):
    #         if(index-1 % 2 == 0):
    #             y_patio = y_patioA
    #         else:
    #             y_patio = y_patioB

    #         y_diff = abs(y_patio - left_corner[1])
    #         # Move the Y coordinates a bit a try again
    #         rect.update_coords(0, y_diff)
    #     else:
    #         break

    
    def locate_rects(self):
        monitor = 19
        index = 0

        x_values = self.placeA.x_values
        placeA_y_values = self.placeA.y_values
        placeB_y_values = self.placeB.y_values


        for rect in self.unlocated_recs:
            index += 1
            #print(f'\n\nRECT {index}\n')
            if(index == monitor):
                print(f'ORIGINAL:{rect.rotated_corners}')

            if((index-1) % 2 == 0):
                place = self.placeA
                located_recs = self.placeA_recs
            else:
                place = self.placeB
                located_recs = self.placeB_recs

            located = False
            for y_patioA, y_patioB in zip(placeA_y_values,placeB_y_values):
                


                if(not located):
                    for x_patio in x_values:

                        fits = False
                        overlap = False

                        corners = rect.rotated_corners
                        left_corner = corners[0]

                        # Check if rectangle fits inside the plane A first, then checks the plane B
                        fits = self._rect_fits_poly(corners, place)
                        if(fits):
                            #if(index == monitor): print(f'Fit!')

                            if(len(located_recs)>0):
                                # Compare the rectangles
                                for other in located_recs:
                                    if(rect.overlap(other)):
                                        overlap = True
                                        break
                            else:
                                overlap = False
                            
                            if(not overlap):
                                located_recs.append(rect)
                                located = True
                                break
                            else:
                                x_diff = abs(x_patio - left_corner[0])
                                # Move the X coordinates a bit a try again
                                rect.update_coords(x_diff,0)

                        else:
                            x_diff = abs(x_patio - left_corner[0])
                            # Move the X coordinates a bit a try again
                            rect.update_coords(x_diff,0)
                    
                if(not located):
                    if(index-1 % 2 == 0):
                        y_patio = y_patioA
                    else:
                        y_patio = y_patioB

                    y_diff = abs(y_patio - left_corner[1])
                    # Move the Y coordinates a bit a try again
                    rect.update_coords(0, y_diff)
                else:
                    break
            
            #if(not located): print(f'NOT LOCATED:{index}')
            if(index == monitor): print(f'LAST: {rect.rotated_corners}')

        print(f'Unlocated: {len(self.unlocated_recs)}')
        print(f'Located: {len(self.placeA_recs) + len(self.placeB_recs)}')
        return self.placeA_recs, self.placeB_recs