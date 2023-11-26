# hash_table.py

class HashTable:
    def __init__(self, table_size=41):
        self.table_size = table_size
        self.table = [None] * table_size

    def custom_hash(self, package_id):
        # Calculate the hash value using the custom hash function
        index = int(package_id) % self.table_size
        return index

    def insert(self, package):
        # Insert a package into the hash table
        index = self.custom_hash(package.package_id)
        # print(f"Inserting package {package.package_id} at index {index}")
        if self.table[index] is None:
            self.table[index] = []
        self.table[index].append(package)

    def lookup(self, package_id):
        # Look up a package by package_id
        index = self.custom_hash(package_id)
        if self.table[index] is not None:
            for package in self.table[index]:
                if package.package_id == package_id:
                    return package
        return None

    def get_all_packages(self):
        # Return a list containing all packages in the hashtable
        all_packages = []
        for bucket in self.table:
            if bucket is not None:
                all_packages.extend(bucket)
        return all_packages
