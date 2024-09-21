import random
import time

class Hashtable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.num_elements = 0
        self.load_factor = 0.75

    def hash_function(self, key):
        return key % self.size

    def rehash(self, key):
        return (key + random.randint(1, 10)) % self.size

    def add_element(self, key, value):
        if self.num_elements / self.size >= self.load_factor:
            self._resize()
        
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = (key, value)
        else:
            new_index = self.rehash(index)
            while self.table[new_index] is not None and new_index != index:
                new_index = self.rehash(new_index)
            if new_index == index:
                raise Exception("Hashtable is full")
            self.table[new_index] = (key, value)
        self.num_elements += 1

    def _resize(self):
        new_size = self.size * 2
        new_table = [None] * new_size
        for item in self.table:
            if item is not None:
                key, value = item
                new_index = self.hash_function(key)
                while new_table[new_index] is not None:
                    new_index = self.rehash(new_index)
                new_table[new_index] = (key, value)
        self.table = new_table
        self.size = new_size

    def search_element(self, key):
        index = self.hash_function(key)
        if self.table[index] is not None and self.table[index][0] == key:
            return self.table[index][1]
        else:
            search_index = self.rehash(index)
            while self.table[search_index] is not None and search_index != index:
                if self.table[search_index][0] == key:
                    return self.table[search_index][1]
                search_index = self.rehash(search_index)
            return None

    def delete_element(self, key):
        index = self.hash_function(key)
        if self.table[index] is not None and self.table[index][0] == key:
            self.table[index] = None
        else:
            search_index = self.rehash(index)
            while self.table[search_index] is not None and search_index != index:
                if self.table[search_index][0] == key:
                    self.table[search_index] = None
                    return
                search_index = self.rehash(search_index)
            raise Exception("Key not found")

# Generate initial random data
data_size = 100
keys = [random.randint(1, 100) for _ in range(data_size)]
values = [str(key) + "_value" for key in keys]

# Populate the hashtable
htable = Hashtable(100)

# Measure time for adding elements
start_time = time.time()
for key, value in zip(keys, values):
    htable.add_element(key, value)
end_time = time.time()
print("Time taken for adding elements:", end_time - start_time, "seconds")

# Test search with hashtable
start_time = time.time()
result = htable.search_element(42)
end_time = time.time()
print("Hashtable search result:", result)
print("Time taken for hashtable search:", end_time - start_time, "seconds")

# Test deletion with hashtable
start_time = time.time()
htable.delete_element(42)
end_time = time.time()
print("Time taken for deleting element:", end_time - start_time, "seconds")