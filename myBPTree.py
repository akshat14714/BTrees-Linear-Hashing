import sys
import os
from bisect import bisect

class Node:

	def __init__(self):
		self.keys = list()
		self.children = list()
		self.is_leaf = True
		self.next = None

	def splitNode(self):
		newNode = Node()

		mid = int(len(self.keys) / 2)
		midKey = self.keys[mid]

		if not self.is_leaf:
			newNode.is_leaf = False

			newNode.keys, newNode.children = self.keys[mid+1:], self.children[mid+1:]

			self.keys, self.children = self.keys[:mid], self.children[:mid+1]

		else:
			newNode.is_leaf = True

			newNode.keys, newNode.children = self.keys[mid:], self.children[mid:]

			self.keys, self.children = self.keys[:mid], self.children[:mid]

			newNode.next = self.next
			self.next = newNode

		return midKey, newNode

class BPlusTree:

	def __init__(self, factor):
		self.factor = factor
		self.root = Node()
		self.root.is_leaf = True
		self.root.keys = list()
		self.root.children = list()
		self.root.next = None
	
	def insert_routine(self, key):
		ans, newNode =  self.tree_insert(key, self.root)

		if ans:
			newRoot = Node()
			newRoot.is_leaf, newRoot.keys, newRoot.children = False, [ans], [self.root, newNode]

			self.root = newRoot

	def tree_insert(self, key, node):
		ans = None

		if node.is_leaf:
			index = bisect(node.keys, key)
			node.keys[index:index] = [key]
			node.children[index:index] = [key]

			if len(node.keys) <= self.factor-1:
				return None, None
			else:
				midKey, newNode = node.splitNode()
				return midKey, newNode
		else:
			if key < node.keys[0]:
				ans, newNode = self.tree_insert(key, node.children[0])

			for i in range(len(node.keys) - 1):
				if key >= node.keys[i] and key < node.keys[i + 1]:
					ans, newNode = self.tree_insert(key, node.children[i+1])

			if key >= node.keys[-1]:
				ans, newNode = self.tree_insert(key, node.children[-1])

		if ans:
			index = bisect(node.keys, ans)
			node.keys[index:index] = [ans]
			node.children[index+1:index+1] = [newNode]
			if len(node.keys) <= self.factor-1:
				return None, None
			else:
				midKey, newNode = node.splitNode()
				return midKey, newNode
		else:
			return None, None

	def tree_search_for_query(self, key, node):

		if node.is_leaf:
			return node

		if key <= node.keys[0]:
			return self.tree_search_for_query(key, node.children[0])

		for i in range(len(node.keys)-1):
			if key>node.keys[i] and key<=node.keys[i+1]:
				return self.tree_search_for_query(key, node.children[i+1])

		if key > node.keys[-1]:
			return self.tree_search_for_query(key, node.children[-1])

	def count_query(self, key):
		count = 0

		start_leaf = self.tree_search_for_query(key, self.root)

		key_count, next_node = self.get_keys_in_range(key, key, start_leaf)
		count += key_count

		while next_node:
			key_count, next_node = self.get_keys_in_range(key, key, next_node)
			count += key_count

		return count

	def range_query(self, keyMin, keyMax):
		count = 0

		start_leaf = self.tree_search_for_query(keyMin, self.root)

		key_count, next_node = self.get_keys_in_range(keyMin, keyMax, start_leaf)
		count += key_count

		while next_node:
			key_count, next_node = self.get_keys_in_range(keyMin, keyMax, next_node)
			count += key_count

		return count

	def get_keys_in_range(self, keyMin, keyMax, node):
		count = 0

		for i in range(len(node.keys)):
			key = node.keys[i]
			if keyMin <= key and key <= keyMax:
				count += 1

		next_node = None

		if len(node.keys) == 0:
			return 0, next_node

		if node.keys[-1] > keyMax:
			next_node = None

		else:
			if node.next:
				next_node = node.next
			else:
				next_node = None

		return count, next_node

def perform(cmnd):
	global output_buffer

	if cmnd[0] == "INSERT":
		tree.insert_routine(int(cmnd[1]))

	elif cmnd[0] == "FIND":
		res = tree.count_query(int(cmnd[1]))
		if res != 0:
			output_buffer.append("YES")
		else:
			output_buffer.append("NO")

	elif cmnd[0] == "COUNT":
		res = tree.count_query(int(cmnd[1]))
		output_buffer.append(res)

	elif cmnd[0] == "RANGE":
		res = tree.range_query(int(cmnd[1]), int(cmnd[2]))
		output_buffer.append(res)

	if len(output_buffer) >= ((B * 1.0) / 10.0):
		for res in output_buffer:
			print(res)
		output_buffer = []

if __name__ == "__main__":
	filename = sys.argv[1]

	M = int(sys.argv[2])
	B = int(sys.argv[3])

	if not os.path.isfile(filename):
		print("Invalid File")
		exit(-1)

	input_buffer, output_buffer = list(), list()
	
	pointer_count = ((B - 8) / 12) + 1

	if pointer_count <= 2:
		pointer_count = 2
	if M <= 2:
		M = 2
	if B <= 20:
		B = 20

	tree = BPlusTree(pointer_count)

	with open(filename) as fh:
		for line in fh:
			cmnd = line.strip().split()
			input_buffer.append(cmnd)
			if len(input_buffer) >= (((M-1) * B) / 10.0) :
				for cmnd in input_buffer:
					perform(cmnd)
				input_buffer = []

		for cmnd in input_buffer:
			perform(cmnd)
		input_buffer = []

	for res in output_buffer:
		print(res)
	output_buffer = []