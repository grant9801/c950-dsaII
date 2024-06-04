#Part 2A: Creating a Hash Table 

class HashTable:
    def __init__(self, size = 40):
        self.size = size
        size.table = [[] for_ in range(self.size)]
    
    def hash(self, key):
        return hash(key) % self.size
    
    def insert(self, package_id, data):
        index = self.hash(package_id)
        self.table[index].append((package_id,data))

    def lookup(self, package_id):
        index = self.hash(package_id)
        for key, value in self.table[index]
            if key == package_id:
                return value
        return None