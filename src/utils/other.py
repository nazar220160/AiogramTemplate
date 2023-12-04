import time


class AutoExpireList:
    def __init__(self):
        self.data = []

    def add_item(self, item, expiration_time):
        self.data.append((item, time.time() + expiration_time))

    def get_items(self, expiration: bool = False):
        current_time = time.time()
        self.data = [(item, expiration) for item, expiration in self.data if expiration > current_time]
        if expiration is True:
            return [item for item in self.data]
        else:
            return [item[0] for item in self.data]
