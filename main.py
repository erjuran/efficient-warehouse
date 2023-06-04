from modules.efficient_warehouse_module import EfficientWarehouse
from modules.tetris.Polynomial import PolyRegressor


if __name__ == '__main__':
    
    storage_days_warehouse = EfficientWarehouse("inputs/Equipos.xlsx", "inputs/WarehouseDimensions.xlsx", "storage-days")
    storage_days_warehouse.generate_sorted_inventories("MultipleSortedInvsByStorageDays.xlsx","WarehouseByStorageDays.xlsx")

    '''
    remaining_days_warehouse = EfficientWarehouse("inputs/Equipos_fechas_2023-2024.xlsx", "inputs/WarehouseDimensions.xlsx", "remaining-days")
    remaining_days_warehouse.generate_sorted_inventories("MultipleSortedInvsByRemainingDays.xlsx","WarehouseByRemainingDays.xlsx")
    '''