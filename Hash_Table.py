TOO_FULL = 0.5
GROWTH_RATIO = 2

def probe(index, size):
        '''
        Linearly probes for next available spot in hash table
        '''
        index += 1
        return index % size

class Hash_Table:

    def __init__(self,cells,defval):
        '''
        Construct a new hash table with a fixed number of cells equal to the
        parameter "cells", and which yields the value defval upon a lookup to a
        key that has not previously been inserted
        '''
        self.size = cells
        self.defval = defval
        self.keys = [self.defval] * self.size
        self.values = [self.defval] * self.size
        self.count = 0

    def hash(self, key):
        '''
        Generating indices for keys
        '''
        index = 0
        for char in key:
            index = index * 37
            index += ord(char)
            index = index % self.size
        return index


    def lookup(self,key):
        '''
        Retrieve the value associated with the specified key in the hash table,
        or return the default value if it has not previously been inserted
        '''
        index = self.hash(key)
     
        while self.values[index] != self.defval:
            if self.keys[index] == key:
                return self.values[index]
            else:
                index = probe(index, self.size)
        return self.defval


    def update(self,key,val):
        '''
        Change the value associated with key "key" to value "val".
        If "key" is not currently present in the hash table,  insert it with
        value "val".
        '''
        index = self.hash(key)

        if self.lookup(key) != self.defval:
            while self.keys[index] != key:
                index = probe(index, self.size)
            self.values[index] = val
        else:
            while self.values[index] != self.defval:
                index = probe(index, self.size)
            self.keys[index] = key
            self.values[index] = val
            self.count += 1
            
            if (self.count / self.size) > TOO_FULL:
                self.rehash()


    def rehash(self):
        '''
        Rehash function if too many cells in the hash table are occupied
        '''
        self.size = self.size * GROWTH_RATIO
        new_keys = [self.defval] * self.size
        new_values = [self.defval] * self.size

        for i in range(0, int(self.size / GROWTH_RATIO)):
            new_keys[i] = self.keys[i]
            new_values[i] = self.values[i]
        
        self.keys = new_keys
        self.values = new_values