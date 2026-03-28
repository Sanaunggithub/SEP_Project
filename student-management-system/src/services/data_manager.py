class DataManager:
    def __init__(self):
        self.data_store = {}

    def save_data(self, key, value):
        self.data_store[key] = value

    def get_data(self, key):
        return self.data_store.get(key, None)

    def delete_data(self, key):
        if key in self.data_store:
            del self.data_store[key]

    def clear_data(self):
        self.data_store.clear()