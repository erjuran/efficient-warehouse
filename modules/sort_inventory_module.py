import pandas as pd
import itertools
from .tetris.DualSorter import DualSorter
from .tetris.Rectangle import Rectangle
from .tetris.Plotter import Plotter
from .tetris.Polynomial import Polynomial, PolyRegressor

class InventorySorter:
    """
    """
    sort_types = ['GROUP','DAYS','SLOTS','TETRIS','IDEAL-SLOT']
    #sort_types = ['DAYS','TETRIS']
    #sort_types = ['GROUP','DAYS']
    opt_style = "storage-days"

    @staticmethod
    def sort_by_group(external_inventory):
        """
        """
        column = 'Días de almacenamiento' if InventorySorter.opt_style == 'storage-days' else 'Días restantes'

        sorted_inventory = external_inventory.sort_values(['GRUPO',column]).groupby('GRUPO')
        sorted_inventory_df = sorted_inventory.apply(lambda x: x.reset_index(drop=True))
        return sorted_inventory_df
    
    @staticmethod
    def sort_by_days(external_inventory):
        """
        """
        column = 'Días de almacenamiento' if InventorySorter.opt_style == 'storage-days' else 'Días restantes'
        sorted_inventory = external_inventory.sort_values([column])
        return sorted_inventory

    @staticmethod
    def sort_by_tetris_slots(sorted_inventory, slot_size=0):

        sorted_inventory["Detalle de almacenamiento"] = ''

        located_equips = 0
        unlocated_recs = []

        for index, equip in sorted_inventory.iterrows():

            equip_summary = {
                "INDEX": index,
                #"GRUPO":equip["GRUPO"],
                #"TAG": equip["TAG"],
                #"LARGO": equip['Largo+FS (m)'],
                #"ANCHO": equip['Ancho+FS (m)'],
                #"DIAS": equip['Días de almacenamiento']
            }

            unlocated_recs.append(Rectangle(equip['Ancho+FS (m)'], equip['Largo+FS (m)'], -30, equip_summary))
        
        
        place = sorted_inventory.sample(n=1)['Lugar de almacenamiento'].values[0]
        valid_place = False

        print(f'\n{place}\n')

        match place:
            case 'Pulmon 1':
                placeA_model = 'Pulmon1A.joblib'
                placeB_model = 'Pulmon1B.joblib'
                placeA_x_range = (0, 250)
                placeB_x_range = (0, 250)
                valid_place = True
                
            case 'Pulmon 2':
                placeA_model = 'Pulmon2A.joblib'
                placeB_model = 'Pulmon2B.joblib'
                placeA_x_range = (0, 220)
                placeB_x_range = (0, 250)
                valid_place = True

            case 'Pulmon 3':
                placeA_model = 'Pulmon3A.joblib'
                placeB_model = 'Pulmon3B.joblib'
                placeA_x_range = (0, 130)
                placeB_x_range = (0, 130)
                valid_place = True

            case _:
                valid_place = False
                pass
                
        if(valid_place):
            placeA = Polynomial(placeA_x_range,'modules/tetris/math_models/' + placeA_model, slot_size)
            placeB = Polynomial(placeB_x_range,'modules/tetris/math_models/' + placeB_model, slot_size)

            sorter = DualSorter(unlocated_recs,placeA,placeB, slot_size)
            placeA_recs, placeB_recs = sorter.locate_rects()

            if(slot_size>0): 
                mode='idealslot' 
                grid = True
            else: 
                mode='tetris'
                grid = False

            Plotter.save_model_rectangles(placeA.model, placeA_x_range, placeA_recs, place + "A", "outputs/" + mode + "/" + mode + place + "A.png", grid)
            Plotter.save_model_rectangles(placeB.model, placeB_x_range, placeB_recs, place + "B", "outputs/" + mode + "/" + mode + place + "B.png", grid)
            
            # Add the information to the excel table about equipment location
            for equip in placeA_recs:
                summary = equip.summary
                index = summary['INDEX']

                # Refactor the summary
                del summary['INDEX']
                summary['PATIO'] = 'A'
                summary['COORDS'] = equip.rotated_corners
                
                # Add the summary to the dataframe row
                summary_string = ''
                for key in summary:
                    summary_string += key + ':' + str(summary[key]) + ' '

                sorted_inventory.at[index,'Detalle de almacenamiento'] = summary_string
            
            for equip in placeB_recs:
                summary = equip.summary
                index = summary['INDEX']

                # Refactor the summary
                del summary['INDEX']
                summary['PATIO'] = 'B'
                summary['COORDS'] = equip.rotated_corners
                

                # Add the summary to the dataframe row
                summary_string = ''
                for key in summary:
                    summary_string += key + ':' + str(summary[key]) + ' '

                sorted_inventory.at[index,'Detalle de almacenamiento'] = summary_string
        
        return sorted_inventory

    @staticmethod
    def _compare_slot_size(slot, equip_summary, index, sorted_inventory, located_equips, empty_slot):
        # 1. Check if the equipment fits in closest empty slot in group A or B
        
        located = False
        
        slot_summary = {
            "DIVISION" : slot['DIVISION'],
            "CARRIL": slot['CARRIL']
        }

        summary_string = ''
        for key in slot_summary:
            summary_string += key + ':' + str(slot_summary[key]) + ' '

        
        equip_summary_string = 'GRUPO:' + equip_summary['GRUPO'] + '-TAG:' +  equip_summary['TAG'] + ', '

        equip_len = equip_summary['LARGO']
        condition = (len(slot['EQUIPOS']) == 0) if empty_slot else (len(slot['EQUIPOS']) != 0)

        if(empty_slot):
            condition = (len(slot['EQUIPOS']) == 0)
            available_space = slot['LONGITUD']
        else:
            condition = (len(slot['EQUIPOS']) != 0)
            available_space = 0
            # Calculate the remaining space in a non-empty slot
            for stored_equip in slot['EQUIPOS']:
                available_space += stored_equip['LARGO']
            
            available_space = slot['LONGITUD'] - available_space

        if(condition):
            if(equip_len <= available_space):
                slot['EQUIPOS'].append(equip_summary)

                # Change this to add storage details
                sorted_inventory.at[index,'Detalle de almacenamiento'] = summary_string
                located_equips += 1
                located = True

        return located, located_equips

    @staticmethod
    def optimize_slots(sorted_inventory, warehouse):
        """
        Warning: The name of the storage place from the inventory, must match the name of the place
        in the warehouse dimensions

        The sorted inventory comes ordered by less days to more days of storage
        """
        
        sorted_inventory["Detalle de almacenamiento"] = ''

        warehouse_groups = warehouse.groupby('DIVISION')
        a_group = warehouse_groups.get_group('A').to_dict(orient='records')
        b_group = warehouse_groups.get_group('B').to_dict(orient='records')

        ab_list = list(itertools.zip_longest(a_group, b_group))

        located_equips = 0
        for index, equip in sorted_inventory.iterrows():

            equip_summary = {
                "GRUPO":equip["GRUPO"],
                "TAG": equip["TAG"],
                "LARGO": equip['Largo+FS (m)'],
                "DIAS": equip['Días de almacenamiento']
            }

            located = False

            
            for slots in ab_list:
                
                # Check on empty slots in both A and B sides
                if(not located):
                    for slot in slots:
                        #print(slots)
                        if(slot != None):
                            located, located_equips = InventorySorter._compare_slot_size(slot, equip_summary,index,sorted_inventory, located_equips, empty_slot=True)
                            if(located):
                                break
                    if(located):
                        break
                
            # Check on non-empty slots in both A and B sides
            if(not located):
                for slots in ab_list:
                    for slot in slots:
                        if(slot != None):
                            located, located_equips = InventorySorter._compare_slot_size(slot, equip_summary,index,sorted_inventory,located_equips, empty_slot=False)
                            if(located):
                                break
                    if(located):
                        break
        
        return sorted_inventory


    @staticmethod
    def _get_sorting_methods():
        """
        """
        sorting_methods = []
        sorting_tags = []

        for sort_type in InventorySorter.sort_types:
            match sort_type:
                case "GROUP":
                    method = InventorySorter.sort_by_group
                case "DAYS":
                    method = InventorySorter.sort_by_days
                case "SLOTS":
                    method = InventorySorter.optimize_slots
                case "TETRIS":
                    method = InventorySorter.sort_by_tetris_slots
                case "IDEAL-SLOT":
                    method = InventorySorter.sort_by_tetris_slots
                case _:
                    # Default case
                    method = InventorySorter.sort_by_group

            sorting_tags.append(sort_type)
            sorting_methods.append(method)
        
        return sorting_methods, sorting_tags
        

    @staticmethod
    def sort_by_all_types(external_inventory, warehouse):
        """
        """
        sorting_methods, sorting_tags = InventorySorter._get_sorting_methods()

        sorted_invs = []

        # For the slot sorting, the inventory sorted by days is the input
        sorted_by_days_inv = None
        sorted_inv = None

        for i in range(len(sorting_methods)):

            if(sorting_tags[i] == 'DAYS'):
                sorted_inv = sorting_methods[i](external_inventory)
                sorted_by_days_inv = sorted_inv

            elif(sorting_tags[i] == 'GROUP'):
                sorted_inv = sorting_methods[i](external_inventory)

            elif(sorting_tags[i] == 'SLOTS'):
                sorted_inv = sorting_methods[i](sorted_by_days_inv.copy(), warehouse)

            elif(sorting_tags[i] == 'TETRIS'):
                sorted_inv = sorting_methods[i](sorted_by_days_inv.copy())

            elif(sorting_tags[i] == 'IDEAL-SLOT'):
                sorted_inv = sorting_methods[i](sorted_by_days_inv.copy(), 4.4)

            #else:
            #    sorted_inv = sorting_methods[i](external_inventory)
            
            sorted_invs.append(sorted_inv)

        return sorted_invs, sorting_tags

        

    
    