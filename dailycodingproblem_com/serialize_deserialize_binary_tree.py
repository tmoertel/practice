#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Solve interview problem: serialize and deserialize binary trees.

This problem comes from Daily Coding Problem on 2019-03-27 and was
classified as Medium difficulty:

  Reported source: Google.

  Given the root to a binary tree, implement serialize(root), which
  serializes the tree into a string, and deserialize(s), which
  deserializes the string back into the tree.

  For example, given the following Node class

  class Node:
      def __init__(self, val, left=None, right=None):
          self.val = val
          self.left = left
          self.right = right

  The following test should pass:

  node = Node('root', Node('left', Node('left.left')), Node('right'))
  assert deserialize(serialize(node)).left.left.val == 'left.left'

"""

class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Implementation using straight recursion.
def serialize(tree):
    """Returns an inorder encoding of a tree."""
    output_buffer = []
    def traverse(tree):
        # Base case: empty tree.
        if tree is None:
            output_buffer.append('*')
            return
        # Recursive case: non-empty tree.
        output_buffer.append('(')
        output_buffer.extend([repr(len(tree.val)), ',', tree.val])
        traverse(tree.left)
        traverse(tree.right)
        output_buffer.append(')')
    traverse(tree)
    return ''.join(output_buffer)

# Implementation using recursion simulated on an explicit stack.
# (Avoids Python's recursion-depth limit, which is necessary to
# serialize very deep trees.)
#
# Note how we push instructions onto the the stack in reverse order
# compared to the straight-recursion implementation above. This is so
# that when the instructions are popped from the stack, they will be
# performed in the same sequence as above.
def serialize(tree):
    """Returns an inorder encoding of a tree."""
    output_buffer = []
    # Implement the recursive algorithm on a simple stack machine
    # having two instructions:
    #   ')'  = append ')' to the output
    #   tree = serialize this tree
    stack = [tree]
    while stack:
        instruction = stack.pop()
        if instruction == ')':
            output_buffer.append(')')
            continue
        tree = instruction
        # Base case: empty tree.
        if tree is None:
            output_buffer.append('*')
            continue
        # Recursive case: non-empty tree.
        output_buffer.append('(')
        output_buffer.extend([repr(len(tree.val)), ',', tree.val])
        stack.append(')')
        stack.append(tree.right)
        stack.append(tree.left)
    return ''.join(output_buffer)

def deserialize(serialized_tree):
    """Returns the tree whose serialized form is `serialized_tree`."""
    _start, tree = parse_tree(0, serialized_tree)
    return tree

def parse_string(start, serialized_text):
    """Returns (i, text) where i gives the index after the serialized text."""
    comma_index = serialized_text.find(',', start)
    if comma_index == -1:
        return ValueError('Missing expected value-length comma.')
    text_length = int(serialized_text[start:comma_index])
    text_start = comma_index + 1
    text_end = text_start + text_length  # Exclusive.
    return text_end, serialized_text[text_start:text_end]
        
def parse_tree(start, serialized_tree):
    """Returns (i, tree) where i gives the index after the serialized tree."""
    # The first character tells us what is next.
    start_char = serialized_tree[start:start + 1]
    start += 1
    # Case: empty tree.
    if start_char == '*':
        return start, None
    # Case: non-empty tree.
    if start_char == '(':
        start, val = parse_string(start, serialized_tree)
        start, left = parse_tree(start, serialized_tree)
        start, right = parse_tree(start, serialized_tree)
        if serialized_tree[start:start + 1] == ')':
            return start + 1, Node(val, left, right)
        raise ValueError('Expected ")" to close serialized tree')
    # Everything else is bad data.
    raise ValueError('Expected "*" or "(" to start tree')

def test():
    # Test helper functions.
    assert parse_string(0, '4,text') == (6, 'text')
    assert parse_tree(0, '*') == (1, None)
    assert parse_tree(0, '(3,foo**)')[0] == 9
    # Test tree serialization and deserialization.
    assert serialize(None) == '*'
    assert deserialize('*') == None
    assert serialize(Node('foo')) == '(3,foo**)'
    node = Node('root', Node('left', Node('left.left')), Node('right'))
    assert serialize(node) == '(4,root(4,left(9,left.left**)*)(5,right**))'
    assert deserialize(serialize(node)).left.left.val == 'left.left'
    assert serialize(node) == serialize(deserialize(serialize(node)))
