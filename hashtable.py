# Initialize Hash Table Class
class HashTable:
    def __init__(self, size=40):
        self.size = size
        self.table = []
        for i in range(self.size):
            self.table.append([])

    # Hash Function
    def _hash(self, key):
        return hash(key) % self.size

    # Insert package data into hash function
    def insert(self, id, address, city, state, zipcode, deadline, weight, special_notes, status, delivery_time = ''):
        data = {
            "PackageID": id,
            "Address": address,
            "City": city,
            "State": state,
            "zipcode": zipcode,
            "deadline": deadline,
            "Weight": weight,
            "SpecialNotes": special_notes,
            "status": status,
            "delivery_time": delivery_time
        }
        index = self._hash(id)
        self.table[index].append((id, data))

    # Lookup Package Data In Hash Table
    def lookup(self, id):
        index = self._hash(id)
        for key, value in self.table[index]:
            if key == id:
                return value
        return None
    
