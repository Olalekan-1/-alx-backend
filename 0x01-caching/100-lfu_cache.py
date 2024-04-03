#!/usr/bin/python3
""" LFUCache module
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache inherits from BaseCaching and is a caching system
    """

    def __init__(self):
        """ Initialize the LFUCache
        """
        super().__init__()
        self.frequency = {}
        self.min_frequency = 0

    def update_frequency(self, key):
        """ Update the frequency of access for the given key
        """
        if key in self.frequency:
            self.frequency[key] += 1
        else:
            self.frequency[key] = 1

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            min_frequency_keys = [key for key,
                                  freq in self.frequency.items()
                                  if freq == self.min_frequency]

            if len(min_frequency_keys) > 1:
                lru_key = min_frequency_keys[0]
                for k in min_frequency_keys:
                    if self.cache_data[k] < self.cache_data[lru_key]:
                        lru_key = k
                min_frequency_keys = [lru_key]
            for k in min_frequency_keys:
                del self.cache_data[k]
                del self.frequency[k]
                print("DISCARD:", k)

        self.cache_data[key] = item
        self.frequency[key] = 1
        self.min_frequency = 1

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        self.update_frequency(key)
        return self.cache_data[key]
