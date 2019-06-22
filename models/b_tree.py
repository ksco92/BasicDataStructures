#
# B-tree set (Python)
#
# Copyright (c) 2018 Project Nayuki. (MIT License)
# https://www.nayuki.io/page/btree-set
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# - The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# - The Software is provided "as is", without warranty of any kind, express or
#   implied, including but not limited to the warranties of merchantability,
#   fitness for a particular purpose and noninfringement. In no event shall the
#   authors or copyright holders be liable for any claim, damages or other
#   liability, whether in an action of contract, tort or otherwise, arising from,
#   out of or in connection with the Software or the use or other dealings in the
#   Software.
#

import numbers


class BTree(object):

    # The degree is the minimum number of children each non-root internal node must have.
    def __init__(self, degree, coll=None):
        if not isinstance(degree, numbers.Integral):
            raise TypeError()
        if degree < 2:
            raise ValueError("Degree must be at least 2")
        self.minkeys = degree - 1  # At least 1, equal to degree-1
        self.maxkeys = degree * 2 - 1  # At least 3, odd number, equal to minkeys*2+1

        self.clear()
        if coll is not None:
            for obj in coll:
                self.insert(obj)

    def __len__(self):
        return self.size

    def clear(self):
        self.root = BTree.Node(self.maxkeys, True)
        self.size = 0

    def __contains__(self, obj):
        # Walk down the tree
        node = self.root
        while True:
            found, index = node.search(obj)
            if found:
                return True
            elif node.is_leaf():
                return False
            else:  # Internal node
                node = node.children[index]

    def insert(self, obj):
        # Special preprocessing to split root node
        root = self.root
        if len(root.keys) == self.maxkeys:
            child = root
            self.root = root = BTree.Node(self.maxkeys, False)  # Increment tree height
            root.children.append(child)
            root.split_child(self.minkeys, self.maxkeys, 0)

        # Walk down the tree
        node = root
        while True:
            # Search for index in current node
            assert len(node.keys) < self.maxkeys
            assert node is root or len(node.keys) >= self.minkeys
            found, index = node.search(obj)
            if found:
                return  # Key already exists in tree

            if node.is_leaf():  # Simple insertion into leaf
                node.keys.insert(index, obj)
                self.size += 1
                return  # Successfully added

            else:  # Handle internal node
                child = node.children[index]
                if len(child.keys) == self.maxkeys:  # Split child node
                    node.split_child(self.minkeys, self.maxkeys, index)
                    if obj == node.keys[index]:
                        return  # Key already exists in tree
                    elif obj > node.keys[index]:
                        child = node.children[index + 1]
                node = child

    def remove(self, obj):
        if not self._remove(obj):
            raise KeyError(str(obj))

    def discard(self, obj):
        self._remove(obj)

    # Returns whether an object was removed.
    def _remove(self, obj):
        # Walk down the tree
        root = self.root
        found, index = root.search(obj)
        node = root
        while True:
            assert len(node.keys) <= self.maxkeys
            assert node is root or len(node.keys) > self.minkeys
            if node.is_leaf():
                if found:  # Simple removal from leaf
                    node.remove_key(index)
                    assert self.size > 0
                    self.size -= 1
                return found

            else:  # Internal node
                if found:  # Key is stored at current node
                    left, right = node.children[index: index + 2]
                    if len(left.keys) > self.minkeys:  # Replace key with predecessor
                        node.keys[index] = left.remove_max(self.minkeys)
                        assert self.size > 0
                        self.size -= 1
                        return True
                    elif len(right.keys) > self.minkeys:
                        node.keys[index] = right.remove_min(self.minkeys)
                        assert self.size > 0
                        self.size -= 1
                        return True
                    else:  # Merge key and right node into left node, then recurse
                        node.merge_children(self.minkeys, index)
                        if node is root and len(root.keys) == 0:
                            assert len(root.children) == 1
                            self.root = root = left  # Decrement tree height
                        node = left
                        index = self.minkeys  # Index known due to merging; no need to search

                else:  # Key might be found in some child
                    child = node.ensure_child_remove(self.minkeys, index)
                    if node is root and len(root.keys) == 0:
                        assert len(root.children) == 1
                        self.root = root = root.children[0]  # Decrement tree height
                    node = child
                    found, index = node.search(obj)

    # Note: Not fail-fast on concurrent modification.
    def __iter__(self):
        # Initialization
        stack = []

        def push_left_path(node):
            while True:
                stack.append((node, 0))
                if node.is_leaf():
                    break
                node = node.children[0]

        push_left_path(self.root)

        # Generate elements
        while len(stack) > 0:
            node, index = stack.pop()
            if node.is_leaf():
                assert index == 0
                for obj in node.keys:
                    yield obj
            else:
                yield node.keys[index]
                index += 1
                if index < len(node.keys):
                    stack.append((node, index))
                push_left_path(node.children[index])

    # For unit tests
    def check_structure(self):
        # Check size and root node properties
        size = self.size
        root = self.root
        if not isinstance(root, BTree.Node) or size < 0 or (size > self.maxkeys and root.is_leaf()) \
                or (size <= self.minkeys * 2 and (not root.is_leaf() or len(root.keys) != size)):
            raise AssertionError("Invalid size or root type")

        # Calculate height by descending into one branch
        height = 0
        node = root
        while not node.is_leaf():
            height += 1
            node = node.children[0]

        # Check all nodes and total size
        if root.check_structure(self.minkeys, self.maxkeys, True, height, None, None) != size:
            raise AssertionError("Size mismatch")

    # ---- Helper class ----

    class Node(object):

        # -- Constructor --

        # Note: Once created, a node's structure never changes between a leaf and internal node.
        def __init__(self, maxkeys, leaf):
            assert maxkeys >= 3 and maxkeys % 2 == 1
            self.keys = []  # Length is in [0, maxkeys] for root node, [minkeys, maxkeys] for all other nodes
            self.children = None if leaf else []  # If internal node, then length always equals len(keys)+1

        # -- Methods for getting info --

        def is_leaf(self):
            return self.children is None

        # Searches this node's keys list and returns (True, i) if obj equals keys[i],
        # otherwise returns (False, i) if children[i] should be explored. For simplicity,
        # the implementation uses linear search. It's possible to replace it with binary search for speed.
        def search(self, obj):
            keys = self.keys
            i = 0
            while i < len(keys):
                if obj == keys[i]:
                    assert 0 <= i < len(keys)
                    return (True, i)  # Key found
                elif obj > keys[i]:
                    i += 1
                else:
                    break
            assert 0 <= i <= len(keys)
            return (False, i)  # Not found, caller should recurse on child

        # -- Methods for insertion --

        # For the child node at the given index, this moves the right half of keys and children to a new node,
        # and adds the middle key and new child to this node. The left half of child's data is not moved.
        def split_child(self, minkeys, maxkeys, index):
            assert not self.is_leaf() and 0 <= index <= len(self.keys) < maxkeys
            left = self.children[index]
            assert len(left.keys) == maxkeys
            right = BTree.Node(maxkeys, left.is_leaf())
            self.children.insert(index + 1, right)

            # Handle children
            if not left.is_leaf():
                right.children.extend(left.children[minkeys + 1:])
                del left.children[minkeys + 1:]

            # Handle keys
            self.keys.insert(index, left.keys[minkeys])
            right.keys.extend(left.keys[minkeys + 1:])
            del left.keys[minkeys:]

        # -- Methods for removal --

        # Performs modifications to ensure that this node's child at the given index has at least
        # minKeys+1 keys in preparation for a single removal. The child may gain a key and subchild
        # from its sibling, or it may be merged with a sibling, or nothing needs to be done.
        # A reference to the appropriate child is returned, which is helpful if the old child no longer exists.
        def ensure_child_remove(self, minkeys, index):
            # Preliminaries
            assert not self.is_leaf() and 0 <= index < len(self.children)
            child = self.children[index]
            if len(child.keys) > minkeys:  # Already satisfies the condition
                return child
            assert len(child.keys) == minkeys

            # Get siblings
            left = self.children[index - 1] if index >= 1 else None
            right = self.children[index + 1] if index < len(self.keys) else None
            internal = not child.is_leaf()
            assert left is not None or right is not None  # At least one sibling exists because degree >= 2
            assert left is None or left.is_leaf() != internal  # Sibling must be same type (internal/leaf) as child
            assert right is None or right.is_leaf() != internal  # Sibling must be same type (internal/leaf) as child

            if left is not None and len(left.keys) > minkeys:  # Steal rightmost item from left sibling
                if internal:
                    child.children.insert(0, left.children.pop(-1))
                child.keys.insert(0, self.keys[index - 1])
                self.keys[index - 1] = left.remove_key(len(left.keys) - 1)
                return child
            elif right is not None and len(right.keys) > minkeys:  # Steal leftmost item from right sibling
                if internal:
                    child.children.append(right.children.pop(0))
                child.keys.append(self.keys[index])
                self.keys[index] = right.remove_key(0)
                return child
            elif left is not None:  # Merge child into left sibling
                self.merge_children(minkeys, index - 1)
                return left  # This is the only case where the return value is different
            elif right is not None:  # Merge right sibling into child
                self.merge_children(minkeys, index)
                return child
            else:
                raise AssertionError("Impossible condition")

        # Merges the child node at index+1 into the child node at index,
        # assuming the current node is not empty and both children have minkeys.
        def merge_children(self, minkeys, index):
            assert not self.is_leaf() and 0 <= index < len(self.keys)
            left, right = self.children[index: index + 2]
            assert len(left.keys) == len(right.keys) == minkeys
            if not left.is_leaf():
                left.children.extend(right.children)
            del self.children[index + 1]
            left.keys.append(self.remove_key(index))
            left.keys.extend(right.keys)

        # Removes and returns the minimum key among the whole subtree rooted at this node.
        # Requires this node to be preprocessed to have at least minkeys+1 keys.
        def remove_min(self, minkeys):
            node = self
            while True:
                assert len(node.keys) > minkeys
                if node.is_leaf():
                    return node.remove_key(0)
                else:
                    node = node.ensure_child_remove(minkeys, 0)

        # Removes and returns the maximum key among the whole subtree rooted at this node.
        # Requires this node to be preprocessed to have at least minkeys+1 keys.
        def remove_max(self, minkeys):
            node = self
            while True:
                assert len(node.keys) > minkeys
                if node.is_leaf():
                    return node.remove_key(len(node.keys) - 1)
                else:
                    node = node.ensure_child_remove(minkeys, len(node.children) - 1)

        # Removes and returns this node's key at the given index.
        def remove_key(self, index):
            assert 0 <= index < len(self.keys)
            return self.keys.pop(index)

        # -- Miscellaneous methods --

        # Checks the structure recursively and returns the total number
        # of keys in the subtree rooted at this node. For unit tests.
        def check_structure(self, minkeys, maxkeys, isroot, leafdepth, min, max):
            # Check basic fields
            keys = self.keys
            numkeys = len(keys)
            if self.is_leaf() != (leafdepth == 0):
                raise AssertionError("Incorrect leaf/internal node type")
            if numkeys > maxkeys:
                raise AssertionError("Invalid number of keys")
            if isroot and not self.is_leaf() and numkeys == 0:
                raise AssertionError("Invalid number of keys")
            if not isroot and numkeys < minkeys:
                raise AssertionError("Invalid number of keys")

            # Check keys for strict increasing order
            tempkeys = [min] + keys + [max]
            for i in range(len(tempkeys) - 1):
                x = tempkeys[i]
                y = tempkeys[i + 1]
                if x is not None and y is not None and y <= x:
                    raise AssertionError("Invalid key ordering")

            # Check children recursively and count keys in this subtree
            count = numkeys
            if not self.is_leaf():
                if len(self.children) != numkeys + 1:
                    raise AssertionError("Invalid number of children")
                for (i, child) in enumerate(self.children):
                    # Check children pointers and recurse
                    if not isinstance(child, BTree.Node):
                        raise TypeError()
                    count += child.check_structure(minkeys, maxkeys, False,
                                                   leafdepth - 1, tempkeys[i], tempkeys[i + 1])
            return count

















































# import bisect
# import itertools
# import operator
#
#
# class _BNode(object):
#     __slots__ = ["tree", "contents", "children"]
#
#     def __init__(self, tree, contents=None, children=None):
#         self.tree = tree
#         self.contents = contents or []
#         self.children = children or []
#         if self.children:
#             assert len(self.contents) + 1 == len(self.children), \
#                     "one more child than data item required"
#
#     def __repr__(self):
#         name = getattr(self, "children", 0) and "Branch" or "Leaf"
#         return "<%s %s>" % (name, ", ".join(map(str, self.contents)))
#
#     def lateral(self, parent, parent_index, dest, dest_index):
#         if parent_index > dest_index:
#             dest.contents.append(parent.contents[dest_index])
#             parent.contents[dest_index] = self.contents.pop(0)
#             if self.children:
#                 dest.children.append(self.children.pop(0))
#         else:
#             dest.contents.insert(0, parent.contents[parent_index])
#             parent.contents[parent_index] = self.contents.pop()
#             if self.children:
#                 dest.children.insert(0, self.children.pop())
#
#     def shrink(self, ancestors):
#         parent = None
#
#         if ancestors:
#             parent, parent_index = ancestors.pop()
#             # try to lend to the left neighboring sibling
#             if parent_index:
#                 left_sib = parent.children[parent_index - 1]
#                 if len(left_sib.contents) < self.tree.order:
#                     self.lateral(
#                             parent, parent_index, left_sib, parent_index - 1)
#                     return
#
#             # try the right neighbor
#             if parent_index + 1 < len(parent.children):
#                 right_sib = parent.children[parent_index + 1]
#                 if len(right_sib.contents) < self.tree.order:
#                     self.lateral(
#                             parent, parent_index, right_sib, parent_index + 1)
#                     return
#
#         center = len(self.contents) // 2
#         sibling, push = self.split()
#
#         if not parent:
#             parent, parent_index = self.tree.BRANCH(
#                     self.tree, children=[self]), 0
#             self.tree._root = parent
#
#         # pass the median up to the parent
#         parent.contents.insert(parent_index, push)
#         parent.children.insert(parent_index + 1, sibling)
#         if len(parent.contents) > parent.tree.order:
#             parent.shrink(ancestors)
#
#     def grow(self, ancestors):
#         parent, parent_index = ancestors.pop()
#
#         minimum = self.tree.order // 2
#         left_sib = right_sib = None
#
#         # try to borrow from the right sibling
#         if parent_index + 1 < len(parent.children):
#             right_sib = parent.children[parent_index + 1]
#             if len(right_sib.contents) > minimum:
#                 right_sib.lateral(parent, parent_index + 1, self, parent_index)
#                 return
#
#         # try to borrow from the left sibling
#         if parent_index:
#             left_sib = parent.children[parent_index - 1]
#             if len(left_sib.contents) > minimum:
#                 left_sib.lateral(parent, parent_index - 1, self, parent_index)
#                 return
#
#         # consolidate with a sibling - try left first
#         if left_sib:
#             left_sib.contents.append(parent.contents[parent_index - 1])
#             left_sib.contents.extend(self.contents)
#             if self.children:
#                 left_sib.children.extend(self.children)
#             parent.contents.pop(parent_index - 1)
#             parent.children.pop(parent_index)
#         else:
#             self.contents.append(parent.contents[parent_index])
#             self.contents.extend(right_sib.contents)
#             if self.children:
#                 self.children.extend(right_sib.children)
#             parent.contents.pop(parent_index)
#             parent.children.pop(parent_index + 1)
#
#         if len(parent.contents) < minimum:
#             if ancestors:
#                 # parent is not the root
#                 parent.grow(ancestors)
#             elif not parent.contents:
#                 # parent is root, and its now empty
#                 self.tree._root = left_sib or self
#
#     def split(self):
#         center = len(self.contents) // 2
#         median = self.contents[center]
#         sibling = type(self)(
#                 self.tree,
#                 self.contents[center + 1:],
#                 self.children[center + 1:])
#         self.contents = self.contents[:center]
#         self.children = self.children[:center + 1]
#         return sibling, median
#
#     def insert(self, index, item, ancestors):
#         self.contents.insert(index, item)
#         if len(self.contents) > self.tree.order:
#             self.shrink(ancestors)
#
#     def remove(self, index, ancestors):
#         minimum = self.tree.order // 2
#
#         if self.children:
#             # try promoting from the right subtree first,
#             # but only if it won't have to resize
#             additional_ancestors = [(self, index + 1)]
#             descendent = self.children[index + 1]
#             while descendent.children:
#                 additional_ancestors.append((descendent, 0))
#                 descendent = descendent.children[0]
#             if len(descendent.contents) > minimum:
#                 ancestors.extend(additional_ancestors)
#                 self.contents[index] = descendent.contents[0]
#                 descendent.remove(0, ancestors)
#                 return
#
#             # fall back to the left child
#             additional_ancestors = [(self, index)]
#             descendent = self.children[index]
#             while descendent.children:
#                 additional_ancestors.append(
#                         (descendent, len(descendent.children) - 1))
#                 descendent = descendent.children[-1]
#             ancestors.extend(additional_ancestors)
#             self.contents[index] = descendent.contents[-1]
#             descendent.remove(len(descendent.children) - 1, ancestors)
#         else:
#             self.contents.pop(index)
#             if len(self.contents) < minimum and ancestors:
#                 self.grow(ancestors)
#
#
# class _BPlusLeaf(_BNode):
#     __slots__ = ["tree", "contents", "data", "next"]
#
#     def __init__(self, tree, contents=None, data=None, next=None):
#         self.tree = tree
#         self.contents = contents or []
#         self.data = data or []
#         self.next = next
#         assert len(self.contents) == len(self.data), "one data per key"
#
#     def insert(self, index, key, data, ancestors):
#         self.contents.insert(index, key)
#         self.data.insert(index, data)
#
#         if len(self.contents) > self.tree.order:
#             self.shrink(ancestors)
#
#     def lateral(self, parent, parent_index, dest, dest_index):
#         if parent_index > dest_index:
#             dest.contents.append(self.contents.pop(0))
#             dest.data.append(self.data.pop(0))
#             parent.contents[dest_index] = self.contents[0]
#         else:
#             dest.contents.insert(0, self.contents.pop())
#             dest.data.insert(0, self.data.pop())
#             parent.contents[parent_index] = dest.contents[0]
#
#     def split(self):
#         center = len(self.contents) // 2
#         median = self.contents[center - 1]
#         sibling = type(self)(
#                 self.tree,
#                 self.contents[center:],
#                 self.data[center:],
#                 self.next)
#         self.contents = self.contents[:center]
#         self.data = self.data[:center]
#         self.next = sibling
#         return sibling, sibling.contents[0]
#
#     def remove(self, index, ancestors):
#         minimum = self.tree.order // 2
#         if index >= len(self.contents):
#             self, index = self.next, 0
#
#         key = self.contents[index]
#
#         # if any leaf that could accept the key can do so
#         # without any rebalancing necessary, then go that route
#         current = self
#         while current is not None and current.contents[0] == key:
#             if len(current.contents) > minimum:
#                 if current.contents[0] == key:
#                     index = 0
#                 else:
#                     index = bisect.bisect_left(current.contents, key)
#                 current.contents.pop(index)
#                 current.data.pop(index)
#                 return
#             current = current.next
#
#         self.grow(ancestors)
#
#     def grow(self, ancestors):
#         minimum = self.tree.order // 2
#         parent, parent_index = ancestors.pop()
#         left_sib = right_sib = None
#
#         # try borrowing from a neighbor - try right first
#         if parent_index + 1 < len(parent.children):
#             right_sib = parent.children[parent_index + 1]
#             if len(right_sib.contents) > minimum:
#                 right_sib.lateral(parent, parent_index + 1, self, parent_index)
#                 return
#
#         # fallback to left
#         if parent_index:
#             left_sib = parent.children[parent_index - 1]
#             if len(left_sib.contents) > minimum:
#                 left_sib.lateral(parent, parent_index - 1, self, parent_index)
#                 return
#
#         # join with a neighbor - try left first
#         if left_sib:
#             left_sib.contents.extend(self.contents)
#             left_sib.data.extend(self.data)
#             parent.remove(parent_index - 1, ancestors)
#             return
#
#         # fallback to right
#         self.contents.extend(right_sib.contents)
#         self.data.extend(right_sib.data)
#         parent.remove(parent_index, ancestors)
#
#
# class BTree(object):
#     BRANCH = LEAF = _BNode
#
#     def __init__(self, order):
#         self.order = order
#         self._root = self._bottom = self.LEAF(self)
#
#     def _path_to(self, item):
#         current = self._root
#         ancestry = []
#
#         while getattr(current, "children", None):
#             index = bisect.bisect_left(current.contents, item)
#             ancestry.append((current, index))
#             if index < len(current.contents) \
#                     and current.contents[index] == item:
#                 return ancestry
#             current = current.children[index]
#
#         index = bisect.bisect_left(current.contents, item)
#         ancestry.append((current, index))
#         present = index < len(current.contents)
#         present = present and current.contents[index] == item
#
#         return ancestry
#
#     def _present(self, item, ancestors):
#         last, index = ancestors[-1]
#         return index < len(last.contents) and last.contents[index] == item
#
#     def insert(self, item):
#         current = self._root
#         ancestors = self._path_to(item)
#         node, index = ancestors[-1]
#         while getattr(node, "children", None):
#             node = node.children[index]
#             index = bisect.bisect_left(node.contents, item)
#             ancestors.append((node, index))
#         node, index = ancestors.pop()
#         node.insert(index, item, ancestors)
#
#     def remove(self, item):
#         current = self._root
#         ancestors = self._path_to(item)
#
#         if self._present(item, ancestors):
#             node, index = ancestors.pop()
#             node.remove(index, ancestors)
#         else:
#             raise ValueError("%r not in %s" % (item, self.__class__.__name__))
#
#     def __contains__(self, item):
#         return self._present(item, self._path_to(item))
#
#     def __iter__(self):
#         def _recurse(node):
#             if node.children:
#                 for child, item in zip(node.children, node.contents):
#                     for child_item in _recurse(child):
#                         yield child_item
#                     yield item
#                 for child_item in _recurse(node.children[-1]):
#                     yield child_item
#             else:
#                 for item in node.contents:
#                     yield item
#
#         for item in _recurse(self._root):
#             yield item
#
#     def __repr__(self):
#         def recurse(node, accum, depth):
#             accum.append(("  " * depth) + repr(node))
#             for node in getattr(node, "children", []):
#                 recurse(node, accum, depth + 1)
#
#         accum = []
#         recurse(self._root, accum, 0)
#         return "\n".join(accum)
#
#     @classmethod
#     def bulkload(cls, items, order):
#         tree = object.__new__(cls)
#         tree.order = order
#
#         leaves = tree._build_bulkloaded_leaves(items)
#         tree._build_bulkloaded_branches(leaves[0], leaves[1])
#
#         return tree
#
#     def _build_bulkloaded_leaves(self, items):
#         minimum = self.order // 2
#         leaves, seps = [[]], []
#
#         for item in items:
#             if len(leaves[-1]) < self.order:
#                 leaves[-1].append(item)
#             else:
#                 seps.append(item)
#                 leaves.append([])
#
#         if len(leaves[-1]) < minimum and seps:
#             last_two = leaves[-2] + [seps.pop()] + leaves[-1]
#             leaves[-2] = last_two[:minimum]
#             leaves[-1] = last_two[minimum + 1:]
#             seps.append(last_two[minimum])
#
#         return [self.LEAF(self, contents=node) for node in leaves], seps
#
#     def _build_bulkloaded_branches(self, leaves, seps):
#         minimum = self.order // 2
#         levels = [leaves]
#
#         while len(seps) > self.order + 1:
#             items, nodes, seps = seps, [[]], []
#
#             for item in items:
#                 if len(nodes[-1]) < self.order:
#                     nodes[-1].append(item)
#                 else:
#                     seps.append(item)
#                     nodes.append([])
#
#             if len(nodes[-1]) < minimum and seps:
#                 last_two = nodes[-2] + [seps.pop()] + nodes[-1]
#                 nodes[-2] = last_two[:minimum]
#                 nodes[-1] = last_two[minimum + 1:]
#                 seps.append(last_two[minimum])
#
#             offset = 0
#             for i, node in enumerate(nodes):
#                 children = levels[-1][offset:offset + len(node) + 1]
#                 nodes[i] = self.BRANCH(self, contents=node, children=children)
#                 offset += len(node) + 1
#
#             levels.append(nodes)
#
#         self._root = self.BRANCH(self, contents=seps, children=levels[-1])
#
#
# class BPlusTree(BTree):
#     LEAF = _BPlusLeaf
#
#     def _get(self, key):
#         node, index = self._path_to(key)[-1]
#
#         if index == len(node.contents):
#             if node.next:
#                 node, index = node.next, 0
#             else:
#                 return
#
#         while node.contents[index] == key:
#             yield node.data[index]
#             index += 1
#             if index == len(node.contents):
#                 if node.next:
#                     node, index = node.next, 0
#                 else:
#                     return
#
#     def _path_to(self, item):
#         path = super(BPlusTree, self)._path_to(item)
#         node, index = path[-1]
#         while hasattr(node, "children"):
#             node = node.children[index]
#             index = bisect.bisect_left(node.contents, item)
#             path.append((node, index))
#         return path
#
#     def get(self, key, default=None):
#         try:
#             return self._get(key).next()
#         except StopIteration:
#             return default
#
#     def getlist(self, key):
#         return list(self._get(key))
#
#     def insert(self, key, data):
#         path = self._path_to(key)
#         node, index = path.pop()
#         node.insert(index, key, data, path)
#
#     def remove(self, key):
#         path = self._path_to(key)
#         node, index = path.pop()
#         node.remove(index, path)
#
#     __getitem__ = get
#     __setitem__ = insert
#     __delitem__ = remove
#
#     def __contains__(self, key):
#         for item in self._get(key):
#             return True
#         return False
#
#     def iteritems(self):
#         node = self._root
#         while hasattr(node, "children"):
#             node = node.children[0]
#
#         while node:
#             for pair in itertools.izip(node.contents, node.data):
#                 yield pair
#             node = node.next
#
#     def iterkeys(self):
#         return itertools.imap(operator.itemgetter(0), self.iteritems())
#
#     def itervalues(self):
#         return itertools.imap(operator.itemgetter(1), self.iteritems())
#
#     __iter__ = iterkeys
#
#     def items(self):
#         return list(self.iteritems())
#
#     def keys(self):
#         return list(self.iterkeys())
#
#     def values(self):
#         return list(self.itervalues())
#
#     def _build_bulkloaded_leaves(self, items):
#         minimum = self.order // 2
#         leaves, seps = [[]], []
#
#         for item in items:
#             if len(leaves[-1]) >= self.order:
#                 seps.append(item)
#                 leaves.append([])
#             leaves[-1].append(item)
#
#         if len(leaves[-1]) < minimum and seps:
#             last_two = leaves[-2] + leaves[-1]
#             leaves[-2] = last_two[:minimum]
#             leaves[-1] = last_two[minimum:]
#             seps.append(last_two[minimum])
#
#         leaves = [self.LEAF(
#                 self,
#                 contents=[p[0] for p in pairs],
#                 data=[p[1] for p in pairs])
#             for pairs in leaves]
#
#         for i in xrange(len(leaves) - 1):
#             leaves[i].next = leaves[i + 1]
#
#         return leaves, [s[0] for s in seps]