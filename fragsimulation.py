from matplotlib import pyplot as pp
import numpy as np
import random
import itertools

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

def holeSize(a,b):
	"for readability: finds the size of the hole in memory between two points"
	return b-a

def randomSize():
	return random.randint(1,10)

def randomTime():
	return random.randint(1,20)

class Program(object):
	def __init__(self):
		self.size = randomSize()
		self.position = -1
		self.time = randomTime()
		
	def getSize(self):
		return self.size
	def getPosition(self):
		return self.position
	def getTime(self):
		return self.time

	def decrement(self):
		self.time -= 1
	def rightEndPoint(self):
		return self.position + self.size


class Memory(object):
	def __init__(self, size):
		self.size = size
		self.contents = []

	def getContents(self):
		return self.contents
	def numPrograms(self):
		return len(self.contents)
	def getSize(self):
		return self.size

	def addProgram(self, p):
		n = self.numPrograms()
		tmp = 0
		if n == 0:
			self.contents.append(p)
			p.position = 0
		elif n == 1:
			if self.contents[0].getPosition() >= p.getSize():
				p.position = 0
				self.contents.append(p)
			else:
				self.contents.append(p)
				p.position = self.contents[0].getSize()
		else:
			if self.contents[0].getPosition() >= p.getSize():
				p.position = 0
				self.contents.append(p)
				tmp = 1
			if tmp == 0:
				for pairs in pairwise(self.contents):
					if p.getSize() <= holeSize(pairs[0].rightEndPoint(), pairs[1].getPosition()):
						self.contents.append(p)
						p.position = pairs[0].rightEndPoint()
						break
				else:
					"checks last hole"
					if p.getSize() <= holeSize(self.contents[n-1].rightEndPoint(), self.getSize()):
						self.contents.append(p)
						p.position = self.contents[n-1].rightEndPoint()

	def sort(self):
		self.contents = sorted(self.getContents(), key=lambda p: p.getPosition())

	def removeProgram(self):
		for p in self.getContents():
			if p.getTime() == 0:
				self.contents.remove(p)

def simulate(memSize, numTimeSteps):
	m = Memory(memSize)
	tmp = 0
	for i in xrange(numTimeSteps):
		m.addProgram(Program())
		for p in m.getContents():
			p.decrement()
		m.removeProgram()
		m.sort()
	for p in m.getContents():
		tmp += p.getSize()
	print float(tmp)/memSize
	memArray = []
	for p in pairwise(m.getContents()):
		memArray.extend([1 for j in xrange(p[0].getSize())])
		memArray.extend([0 for j in xrange(holeSize(p[0].rightEndPoint(), p[1].getPosition()))])
	memArray.extend([1 for j in xrange(m.getContents()[m.numPrograms()-1].getSize())])
	memArray.extend([0 for j in xrange(memSize - len(memArray))])
	x = [i for i in xrange(memSize)]
	ymin = [0 for i in xrange(memSize)]
	a = np.array(memArray)
	pp.vlines(x, ymin, a)
	pp.ylim(0,1)
	pp.show()
	

simulate(1000, 1000)

