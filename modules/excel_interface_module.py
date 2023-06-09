import pandas as pd

class ExcelInterface:
    """
    TODO: Turn the methods into static methods
    This class helps to transform data coming from excel into dataframes
    and turn the dataframes back to excel.
    """

    def __init__(self):
        """
        Initialize the class variables
        """
        self.__inventory = None

    def import_inventory(self, input_filename):
        """ Reads an input excel file and turns it into a pandas dataframe
            If there is an error reading the file, an Exception is thrown.

            Parameters
            __________
            input_filename : str
                The name of the excel file to read
        """
        try:
            self.__inventory = pd.read_excel(input_filename)

        except Exception as e:
            print(e)

    def export_inventory(self, output_filename, external_inventory=None):
        """ Exports an excel file from a dataframe and assigns a name to the file
            If there is an error writing the file, an Exception is thrown.

            Parameters
            __________
            output_filename : str
                The name of the excel file to export
            inventory (optional): Dataframe
                External inventory to make the exporting process directly
                without using the set_inventory method
        """
        try:
            if(external_inventory is None):
                self.__inventory.to_excel(output_filename)
            else:
                self.set_inventory(external_inventory)
                external_inventory.to_excel(output_filename)

        except Exception as e:
            print(e)

    def export_multiple_inventories(self, output_filename, external_inventories, sheet_names):
        """ Exports an excel file from multiple dataframe and assigns a name to the file and every sheet
            If there is an error writing the file, an Exception is thrown.

            Parameters
            __________
            output_filename : str
                The name of the excel file to export
            external_inventories: list
                External inventories coming as dataframes
            sheet_names: list
                Names for each sheet created from a dataframe
        """

        try:
            num_invs = len(external_inventories)
            if(num_invs > 0 and num_invs == len(sheet_names)):
                with pd.ExcelWriter(output_filename) as writer:
                    for i in range(0, num_invs):
                        external_inventories[i].to_excel(writer, sheet_name=sheet_names[i], index=False)
            else:
                raise Exception("Invalid inputs")

        except Exception as e:
            print(e)

    def get_inventory(self):
        """Return the dataframe object that contains the inventory data"""
        return self.__inventory

    def set_inventory(self, modified_inventory):
        """Modifies the dataframe object that contains the inventory data
        
        Parameters
        __________
        modified_inventory : pandas dataframe
            Inventory with modifications
        """
        self.__inventory = modified_inventory

    @staticmethod
    def get_dataframe_from_excel(excel_filename):
        """
        """
        try:
            return pd.read_excel(excel_filename)

        except Exception as e:
            print(e)
            return None




####### Tests
'''
# 1. Create an instance of the class
excel_interface = ExcelInterface()

# 2. Import the input file from excel
excel_interface.import_inventory("Equipos.xlsx")

# 3. Check if the data was uploaded correctly
print(excel_interface.get_inventory())

# 4. Generate the output excel file
excel_interface.export_inventory("Exported.xlsx")
'''


