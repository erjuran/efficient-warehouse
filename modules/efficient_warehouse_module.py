from datetime import datetime
import pandas as pd

from .excel_interface_module import ExcelInterface
from .sort_inventory_module import InventorySorter

class EfficientWarehouse:

    def __init__(self, input_inventory_filename, input_warehouses_filename, opt_style="storage-days"):
        self.excel_interface = ExcelInterface()
        self.inv_sorter = InventorySorter
        self.excel_interface.import_inventory(input_inventory_filename)
        self.original_inv = self.excel_interface.get_inventory()

        self.warehouses = self.excel_interface.get_dataframe_from_excel(input_warehouses_filename)
        self._format_data()

        if(opt_style == "remaining-days"):
            rem_inv = self._calculate_remaining_days(self.original_inv)
            self.inventories = self._split_inventory(rem_inv)
            InventorySorter.opt_style = 'remaining-days'
        else:
            self.inventories = self._split_inventory(self.original_inv)

        self.sorted_inventories = []

    def _format_data(self):
        """
        """
        # Remove the empty space at the end of some column names
        self.original_inv.columns = self.original_inv.columns.str.rstrip()

        # Remove the space at the end of the 'Lugar de almacenamiento' value 
        self.original_inv['Lugar de almacenamiento'] = self.original_inv['Lugar de almacenamiento'].str.rstrip()

        # Remove the space at the end of the 'GRUPO' value 
        self.original_inv['GRUPO'] = self.original_inv['GRUPO'].str.rstrip()

    def _calculate_remaining_days(self, original_inv):
        """
        """
        # get current date and time
        current_date_time = datetime.now()
        # create a Pandas timestamp from the current date and time
        current_timestamp = pd.Timestamp(current_date_time)

        def calculate_rows(row):
            rem_days = (row['Salida'] - current_timestamp).days
            return rem_days

        original_inv['Días restantes'] = original_inv.apply(calculate_rows,axis=1)
        return original_inv


    
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

        # Add column for adding the equipment records to the warehouse file
        
        self.warehouses["EQUIPOS"] = [[] for _ in range(len(self.warehouses))]

        for place in self.inventories:
            if(place != no_sort_place):
                warehouse = self.warehouses.query("PLANO == @place")
                sorted_inv, sorting_tags = InventorySorter.sort_by_all_types(self.inventories[place], warehouse)

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
    
    def generate_sorted_inventories(self, output_inv_filename, output_warehouse_filename):
        """
        """
        sorted_inventories, sheet_names = self.sort_inventories()

        self.excel_interface.export_multiple_inventories("outputs/"+output_inv_filename,sorted_inventories,sheet_names)
        self.excel_interface.export_inventory("outputs/"+output_warehouse_filename,self.warehouses)







        


