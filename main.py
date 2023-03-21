from excel_interface_module import ExcelInterface
from sort_inventory_module import InventorySorter


if __name__ == '__main__':
    
    excel_interface = ExcelInterface()
    excel_interface.import_inventory("Equipos.xlsx")

    original_inv = excel_interface.get_inventory()
    inventory_sorter = InventorySorter(original_inv)

    # Sort by group
    inv_sorted_by_group = inventory_sorter.sort_by_group()

    # Sort by days
    inv_sorted_by_days = inventory_sorter.sort_by_days()

    # Export in a single file multiple sheets
    excel_interface.export_multiple_inventories("ExportedInventories.xlsx",
                                                [inv_sorted_by_group, inv_sorted_by_days],
                                                ["Ordenado por grupos","Ordenado por días"])
    

