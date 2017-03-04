import unittest


class BinaryTree:
    """ Alternate implementation of a binary tree. """
    
    def __init__(self, value, left=None, right=None):
        self.value = value
        self._left = left
        self._right = right
    
    @property
    def left(self):
        return self._left
    
    @left.setter
    def left(self, value):
        if self._left:
            self._left.value = value
        else:
            self._left = self.__class__(value)
    
    @property
    def right(self):
        return self._right
        
    @right.setter
    def right(self, value):
        if self._right:
            self._right.value = value
        else:
            self._right = self.__class__(value)
    
    @property
    def is_leaf(self):
        return not self.left and not self.right

    def _as_dict(self, depth=0):
        """ Represent BinaryTree structure in a nested dictionary. """
        dictionary = {}
        dictionary['depth'] = depth
        dictionary['value'] = self.value
        
        if self.left:
            dictionary['left'] = self.left._as_dict(depth=depth + 1)
        else:
            dictionary['left'] = None
            
        if self.right:
            dictionary['right'] = self.right._as_dict(depth=depth + 1)
        else:
            dictionary['right'] = None
            
        return dictionary

    def as_dict(self):
        return self._as_dict(depth=0)
        
    def __str__(self):
        return str(self.as_dict())
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        if self.left:
            yield from iter(self.left)
        yield self.value
        if self.right:
            yield from iter(self.right)
    
    def __eq__(self, other):
        return all(s == o for s, o in zip(self, other))

class BinaryTreeTest(unittest.TestCase):
    def setUp(self):
        self.tree1 = BinaryTree(1)
        self.tree2 = BinaryTree(2, BinaryTree(3))
        self.tree3 = BinaryTree(4, None, BinaryTree(5))
        self.tree4 = BinaryTree(6, BinaryTree(7), BinaryTree(8, BinaryTree(9), BinaryTree(10)))
    
    def test_left_getter(self):
        assert self.tree1.left == None
        assert self.tree2.left.value == 3
        assert self.tree3.left == None
        
    def test_left_setter(self):
        self.tree1.left = 2
        assert self.tree1.left.value == 2
        self.tree2.left = 4
        assert self.tree2.left.value == 4
    
    def test_right_getter(self):
        assert self.tree1.right == None
        assert self.tree2.right == None
        assert self.tree3.right.value == 5
        assert self.tree4.right.value == 8
        assert self.tree4.right.left.value == 9
        assert self.tree4.right.right.value == 10
        
    def test_right_setter(self):
        self.tree1.right = 2
        assert self.tree1.right.value == 2
        self.tree3.right = 6
        assert self.tree3.right.value == 6
        self.tree4.right = 11
        assert self.tree4.right.value == 11
        assert self.tree4.right.left.value == 9
        assert self.tree4.right.right.value == 10
    
    def test_as_dict(self):
        assert self.tree1.as_dict() == {
            'depth': 0,
            'value': 1,
            'left': None,
            'right': None
        }
        assert self.tree2.as_dict() == {
            'depth': 0,
            'value': 2,
            'left': {
                'depth': 1,
                'value': 3,
                'left': None,
                'right': None
            },
            'right': None
        }
        assert self.tree3.as_dict() == {
            'depth': 0,
            'value': 4,
            'left': None,
            'right': {
                'depth': 1,
                'value': 5,
                'left': None,
                'right': None
            }
        }
        assert self.tree4.as_dict() == {
            'depth': 0,
            'value': 6,
            'left': {
                'depth': 1,
                'value': 7,
                'left': None,
                'right': None
            },
            'right': {
                'depth': 1,
                'value': 8,
                'left': {
                    'depth': 2,
                    'value': 9,
                    'left': None,
                    'right': None
                },
                'right': {
                    'depth': 2,
                    'value': 10,
                    'left': None,
                    'right': None
                }
            }
        }
        
    def _verify_traversal(self, tree, expected_values, reverse=False):
        for expected, actual in zip(expected_values, tree):
            assert expected == actual

    def test_traverse(self):
        self._verify_traversal(self.tree1, [1])
        self._verify_traversal(self.tree2, [3, 2])
        self._verify_traversal(self.tree3, [4, 5])
        self._verify_traversal(self.tree4, [7, 6, 9, 8, 10])

if __name__ == '__main__':
    unittest.main()