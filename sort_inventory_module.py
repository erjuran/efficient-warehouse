
class InventorySorter:
    """
    """

    def __init__(self, inventory):
        self.inventory = inventory

    def sort_by_group(self):
        '''
        WARNING: There is an empty space an the end of the column names.
        It comes like that from the excel file. If new excel files are read
        in the future and the column names don't contain the empty space at
        the end, the code will fail.
        '''
        sorted_inventory = self.inventory.sort_values(['GRUPO ','Días de almacenamiento ']).groupby('GRUPO ').head()
        #sorted_inventory = self.inventory.groupby(['GRUPO ']).sort_values(['Días de almacenamiento '])
        return sorted_inventory
    
    def sort_by_days(self):
        sorted_inventory = self.inventory.sort_values(['Días de almacenamiento '])
        return sorted_inventory