from joblib import load

class OptimizeWarehouse:

    def __init__(self, models_path):
        
        # Check how to make this more scalable
        filenames = ['1A','1B','2A','2B','3A','3B']
        models = {}
        for filename in filenames:
            models[filename] = load(f'Pulmon{filename}.joblib')
    

    def generate_slots(self):
        pass
