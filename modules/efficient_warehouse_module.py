from excel_interface_module import ExcelInterface
from sort_inventory_module import InventorySorter

class EfficientWarehouse:

    def __init__(self, input_inventory_name):
        self.excel_interface = ExcelInterface()
        self.excel_interface.import_inventory(input_inventory_name)
        self.original_inv = self.excel_interface.get_inventory()

        self.inventories = []
        #inventory_sorter = InventorySorter(self.original_inv)


    def _format_data(self):
        """
        """
        # Remove the empty space at the end of some column names
        self.original_inv.columns = self.original_inv.str.replace(' ','')

        # Remove the space at the end of the 'Lugar de almacenamiento' value 
        self.original_inv['Lugar de almacenamiento'] = self.original_inv['Lugar de almacenamiento'].str.rstrip()

        # Remove the space at the end of the 'GRUPO' value 
        self.original_inv['GRUPO'] = self.original_inv['GRUPO'].str.rstrip()

    
    def _split_inventory(self):
        """
        """
        self.inventories = self.original_inv.groupby('Lugar de almacenamiento')
        


