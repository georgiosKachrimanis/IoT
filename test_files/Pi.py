class Pi:
    def __init__(self, name, battery, memory, position, available_storage, is_ap=False, next_ap=[]):
        self.name = name
        self.battery = battery
        self.memory = memory
        self.position = position
        self.available_storage = available_storage
        self.is_ap = is_ap

