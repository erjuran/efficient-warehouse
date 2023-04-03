
class InventorySorter:
    """
    """
    sort_types = ['GROUP','DAYS']

    @staticmethod
    def sort_by_group(external_inventory):
        """
        """
        sorted_inventory = external_inventory.sort_values(['GRUPO','Días de almacenamiento']).groupby('GRUPO').head()
        return sorted_inventory
    
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

    
    