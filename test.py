from models.avl_tree import AVLTree
b = AVLTree()
b.add_element(5)
b.add_element(3)
b.add_element(8)
b.add_element(10)
b.add_element(11)
b.add_element(12)
b.add_element(13)
b.add_element(14)
# print(b)
print(b.pre_order())
