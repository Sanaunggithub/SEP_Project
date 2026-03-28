class BaseModel:
    def __init__(self):
        self.id = None

    def save(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def delete(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def to_dict(self):
        raise NotImplementedError("Subclasses should implement this method.")