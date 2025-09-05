class HFNode:
	index = -1  # if leaf, saves the position in alphabet; otherwise, -1;
	level = 0 # level of the node in the tree
	left, right = None, None  # left and right child nodes. If leaf, both are None
	
	
	def __init__(self, i, lv, l=None, r=None):
		self.index = i
		self.level = lv
		self.left = l
		self.right = r
	
	# check if node is leaf
	def isLeaf(self):
		return self.left == None and self.right == None
			
class HuffmanTree:
	root = curNode = None  

	def __init__(self, root=None, curNode=None):
		if not root:
			root = HFNode(-1, 0)
			curNode = root
		self.root = root
		self.curNode = curNode
		
	

	def resetCurNode(self):
		self.curNode = self.root
	
	def addNode(self, s, ind, verbose=False):

		tmp = self.root
		lv = 0 
		l = len(s)

		found = False
		pos = -3
					
		while lv < l and not found:
			# trying to create son of leaf --> error, not prefix code
			if tmp.index != -1:
				pos = -2
				found = True
			else:
				direction = s[lv]
				
				if direction == '0': # LEFT

					if lv != l-1 and tmp.left != None:  # keep on going down
						tmp = tmp.left

					elif tmp.left != None: # already inserted
						pos = -1
						found = True
					
					
					else: # create node in the left
						if lv == l-1:  # leaf						
							index = ind
						else:
							index = -1

						hf = HFNode(index, lv+1)
						tmp.left = hf
						tmp = tmp.left
				
				
				elif direction == '1': # RIGHT
				
					if lv != l -1 and tmp.right != None: # keep on going down
						tmp = tmp.right

					elif tmp.right != None: # already inserted
						pos = -1
						found = True
					
					else: # create node in the right
						if lv == l-1:  # leaf
							index = ind
						else:
							index = -1

						hf = HFNode(index, lv+1)
						tmp.right = hf
						tmp = tmp.right
							
			lv += 1	
				
		if not found:
			pos = tmp.index
			
		if verbose:
			if pos == -1:
				print("Code '" + s + "' already inserted!!!")
			elif pos == -2:
				print("Code '" + s + "' trying to extend leaf - no prefix code!!!")
			else:
				print("Code '" + s + "' successfully inserted!!!")
		
		return pos	
	
	def findNode(self, s, cur=None, verbose=False):
		if cur == None:
			cur = self.root
			
		tmp = cur
		lv = 0
		l = len(s)
		found = True
		
		while lv < l and found:
		
			direction = s[lv]
			
			if direction == '0':
				if tmp.left != None:
					tmp = tmp.left
				else:
					found = False
			
			elif direction == '1':
				if tmp.right != None:
					tmp = tmp.right
				else:
					found = False
			
			lv += 1
				
		if not found:
			pos = -1
		elif tmp.index == -1:
			pos = -2
		else:
			pos = tmp.index
			
		if verbose:
			if pos == -1:
				print("Code '" + s + "' not found!!!")
			elif pos == -2:
				print("Code '" + s + "': not found but prefix!!!")
			else:
				print("Code '" + s + "' found, alphabet position: " + str(pos) )
						
		return pos

	def nextNode(self, dir):		
		if self.curNode.isLeaf():
			return -1
		
		if dir == '0':
			if self.curNode.left != None:
				self.curNode = self.curNode.left
				if self.curNode.isLeaf():
					pos = self.curNode.index
				else:
					pos = -2
			else:
				pos = -1
			return pos

		elif dir == '1':
			if self.curNode.right != None:
				self.curNode = self.curNode.right
				if self.curNode.isLeaf():
					pos = self.curNode.index
				else:
					pos = -2
			
			else:
				pos = -1	
			return pos							
		return pos