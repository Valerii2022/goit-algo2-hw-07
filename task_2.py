import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None
    
    def _splay(self, key, root):
        if root is None or root.key == key:
            return root
        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(key, root.left.left)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(key, root.left.right)
                if root.left.right:
                    root.left = self._rotate_left(root.left)
            return self._rotate_right(root) if root.left else root
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(key, root.right.right)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(key, root.right.left)
                if root.right.left:
                    root.right = self._rotate_right(root.right)
            return self._rotate_left(root) if root.right else root

    def _rotate_left(self, node):
        temp = node.right
        node.right = temp.left
        temp.left = node
        return temp

    def _rotate_right(self, node):
        temp = node.left
        node.left = temp.right
        temp.right = node
        return temp

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayNode(key, value)
            return
        self.root = self._splay(key, self.root)
        if self.root.key == key:
            return
        new_node = SplayNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def find(self, key):
        self.root = self._splay(key, self.root)
        return self.root.value if self.root and self.root.key == key else None

def fibonacci_splay(n, tree):
    if n < 2:
        return n
    if (cached := tree.find(n)) is not None:
        return cached
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result

n_values = list(range(0, 951, 50))
lru_times = []
splay_times = []

for n in n_values:
    tree = SplayTree()
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=5) / 5
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=5) / 5
    lru_times.append(lru_time)
    splay_times.append(splay_time)

plt.figure(figsize=(10, 5))
plt.plot(n_values, lru_times, label="LRU Cache", marker='o')
plt.plot(n_values, splay_times, label="Splay Tree", marker='s')
plt.xlabel("n (Fibonacci number index)")
plt.ylabel("Execution Time (s)")
plt.title("Fibonacci Computation Performance: LRU Cache vs Splay Tree")
plt.legend()
plt.grid()
plt.show()

table_format = "{:<10} {:<20} {:<20}"
print(table_format.format("n", "LRU Cache Time (s)", "Splay Tree Time (s)"))
print("-" * 50)
for n, lru, splay in zip(n_values, lru_times, splay_times):
    print(table_format.format(n, f"{lru:.10f}", f"{splay:.10f}"))
