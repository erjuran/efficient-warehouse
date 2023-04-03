from .excel_interface_module import ExcelInterface
from .sort_inventory_module import InventorySorter

class EfficientWarehouse:

    def __init__(self, input_inventory_name):
        self.excel_interface = ExcelInterface()
        self.inv_sorter = InventorySorter
        self.excel_interface.import_inventory(input_inventory_name)
        self.original_inv = self.excel_interface.get_inventory()
        self._format_data()
        self.inventories = self._split_inventory(self.original_inv)
        self.sorted_inventories = []
        #inventory_sorter = InventorySorter(self.original_inv)

    def _format_data(self):
        """
        """
        # Remove the empty space at the end of some column names
        self.original_inv.columns = self.original_inv.columns.str.rstrip()

        # Remove the space at the end of the 'Lugar de almacenamiento' value 
        self.original_inv['Lugar de almacenamiento'] = self.original_inv['Lugar de almacenamiento'].str.rstrip()

        # Remove the space at the end of the 'GRUPO' value 
        self.original_inv['GRUPO'] = self.original_inv['GRUPO'].str.rstrip()

    
    def _split_inventory(self, original_inv):
        """
        """

        invs = {}
        for name, group in original_inv.groupby('Lugar de almacenamiento'):
            invs[name] = group

        return invs


    def sort_inventories(self):
        """
        """

        self.sorted_inventories = []
        self.sheet_names = []
        unsorted_inv = None
        no_sort_place = 'Directo a planta'

        for place in self.inventories:
            if(place != no_sort_place):
                sorted_inv, sorting_tags = InventorySorter.sort_by_all_types(self.inventories[place])

                # Flatten the lists
                for i in range (len(sorting_tags)):  
                    self.sheet_names.append(place + ' ' + sorting_tags[i])
                    self.sorted_inventories.append(sorted_inv[i])

            else:
                unsorted_inv = self.inventories[place]

        # Add the 'Directo a planta records'
        self.sorted_inventories.append(unsorted_inv)
        self.sheet_names.append(no_sort_place)
        return self.sorted_inventories, self.sheet_names
    
    def generate_sorted_inventories(self, output_filename):
        """
        """
        sorted_inventories, sheet_names = self.sort_inventories()
        self.excel_interface.export_multiple_inventories(output_filename,sorted_inventories,sheet_names)







        


