def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            break
    else:
        return n


def find_previous_prime(n):
    return find_next_prime(n, offset=0)


def find_next_prime(n, offset=1):
    p = n
    while p < 2 * n:
        p += 1 * offset
        if is_prime(p):
            break
    return p


class HashTable:

    def __init__(self, table_size, hash_type='Open'):
        self.table_size = table_size
        self.hash_type = hash_type
        self.table = {}

    def __str__(self):
        return str(self.table)

    def hash_function(self, value):
        return (value % find_previous_prime(self.table_size)) + 1

    def insert(self, value):
        if self.hash_type == 'Open':
            key = self.hash_function(value)
            if key in self.table:
                self.table[key].append(value)
            else:
                self.table[key] = [value]
        else:
            self.table[self.hash_function(value)] = value
