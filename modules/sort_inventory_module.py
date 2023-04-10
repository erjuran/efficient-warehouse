import pandas as pd

class InventorySorter:
    """
    """
    sort_types = ['GROUP','DAYS']

    @staticmethod
    def sort_by_group(external_inventory):
        """
        """
        sorted_inventory = external_inventory.sort_values(['GRUPO','Días de almacenamiento']).groupby('GRUPO')
        sorted_inventory_df = sorted_inventory.apply(lambda x: x.reset_index(drop=True))
        return sorted_inventory_df
    
    @staticmethod
    def sort_by_days(external_inventory):
        """
        """
        sorted_inventory = external_inventory.sort_values(['Días de almacenamiento'])
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
                case _:
                    # Default case
                    method = InventorySorter.sort_by_group

            sorting_tags.append(sort_type)
            sorting_methods.append(method)
        
        return sorting_methods, sorting_tags
        

    @staticmethod
    def sort_by_all_types(external_inventory):
        """
        """
        sorting_methods, sorting_tags = InventorySorter._get_sorting_methods()

        return [method(external_inventory) for method in sorting_methods], sorting_tags
    

    @staticmethod
    def optimize_slots(sorted_inventory, warehouse_dimensions):
        """
        Warning: The name of the storage place from the inventory, must match the name of the place
        in the warehouse dimensions

        The sorted inventory comes ordered by less days to more days of storage
        """
        
        sorted_inventory["Detalle de almacenamiento"] = ''

        #TODO: Gotta decide if we take the whole warehouse as input or if we take it already filtered
        warehouse = warehouse_dimensions.query("PLANO == 'Pulmon 3'")
        warehouse["EQUIPOS"] = [[] for _ in range(len(warehouse))]

        warehouse_groups = warehouse.groupby('DIVISION')
        a_group = warehouse_groups.get_group('A')
        b_group = warehouse_groups.get_group('B')

        located_equips = 0
        for index, equip in sorted_inventory.iterrows():

            equip_len = equip['Largo+FS (m)']
            equip_summary = {
                "GRUPO":equip["GRUPO"],
                "TAG": equip["TAG"],
                "LARGO": equip_len,
                "DIAS": equip['Días de almacenamiento']
            }

            located = False

            # Warning: for this to work properly, group A and B need to have the same size
            for i in range(len(a_group)):

                # 1. Check if the equipment fits in closest empty slot in group A
                a_slot = a_group.iloc[i]
                a_slot_summary = {
                    "DIVISION" : a_slot['DIVISION'],
                    "CARRIL": a_slot['CARRIL']
                }

                b_slot = b_group.iloc[i]
                b_slot_summary = {
                    "DIVISION" : b_slot['DIVISION'],
                    "CARRIL": b_slot['CARRIL']
                }

                if(len(a_slot['EQUIPOS']) == 0):
                    if(equip_len <= a_slot['LONGITUD']):
                        a_slot['EQUIPOS'].append(equip_summary)

                        # Change this to add storage details
                        sorted_inventory.at[index,'Detalle de almacenamiento'] = a_slot_summary
                        located_equips += 1
                        located = True
                        break

                # 2. Check if the equipment fits in closest empty slot in group B
                if(len(b_slot['EQUIPOS']) == 0):
                    if(equip_len <= b_slot['LONGITUD']):
                        b_slot['EQUIPOS'].append(equip_summary)
                        # Change this to add storage details
                        sorted_inventory.at[index,'Detalle de almacenamiento'] = b_slot_summary
                        located_equips += 1
                        located = True
                        break
            
            if(not located):
                for i in range(len(a_group)):

                    a_slot = a_group.iloc[i]
                    b_slot = b_group.iloc[i]

                    # 3. Check if the equipment fits in closest non-empty slot in group A
                    if(len(a_slot['EQUIPOS']) != 0):
                        available_space = 0

                        # Calculate the remaining space in a non-empty slot
                        for stored_equip in a_slot['EQUIPOS']:
                            available_space += stored_equip['LARGO']
                        
                        available_space = a_slot['LONGITUD'] - available_space

                        if(equip_len <= available_space):
                            a_slot['EQUIPOS'].append(equip_summary)

                            # Change this to add storage details
                            sorted_inventory.at[index,'Detalle de almacenamiento'] = a_slot_summary
                            located_equips += 1
                            break


                        # 4. Check if the equipment fits in closest non-empty slot in group B
                    if(len(b_slot['EQUIPOS']) != 0):
                        available_space = 0

                        # Calculate the remaining space in a non-empty slot
                        for stored_equip in b_slot['EQUIPOS']:
                            available_space += stored_equip['LARGO']
                        
                        available_space = b_slot['LONGITUD'] - available_space

                        if(equip_len <= available_space):
                            b_slot['EQUIPOS'].append(equip_summary)
                            # Change this to add storage details
                            sorted_inventory.at[index,'Detalle de almacenamiento'] = b_slot_summary
                            located_equips += 1
                            break

        
        print("Total equips:", sorted_inventory.shape[0])
        print("Located equips:",located_equips)
        print(sorted_inventory[['Largo+FS (m)','Detalle de almacenamiento']])
        print(warehouse[["GRUPO","LONGITUD","EQUIPOS"]])

        print(a_group)
        print(b_group)


        # ESTA FUNCIONANDO. AHORA AL MOMENTO DE GENERAR LOS ORDENAMIENTOS, TRAS GENERAR EL ORDENAMIENTO
        # DE DIAS, SE DEBE GENERAR EL ORDENAMIENTO DE SLOTS



                    

        

    
    