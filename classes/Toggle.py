class Toggle:
    def __init__(self, init_data: bool):
        self.internal_data = init_data
        
    def toggle(self):
        self.internal_data = not self.internal_data
        
    def data(self) -> bool:
        return self.internal_data