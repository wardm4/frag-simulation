from matplotlib import pyplot as pp
import numpy as np
import random

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

	def checkHole(self, i, p):
		return p.getSize() <= self.contents[i+1].getPosition() - (self.contents[i].getPosition() + self.contents[i].getSize())

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
				for i in range(n-2):
					if self.checkHole(i,p):
						self.contents.append(p)
						p.position = self.contents[i].getPosition() + self.contents[i].getSize()
						tmp = 1
						break
			if tmp == 0:
				if p.getSize() <= self.getSize() - (self.contents[n-1].getPosition() + self.contents[n-1].getSize()):
					self.contents.append(p)
					p.position = self.contents[n-1].getPosition() + self.contents[n-1].getSize()

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
	for i in xrange(len(m.getContents())-1):
		memArray.extend([1 for j in range(m.getContents()[i].getSize())])
		memArray.extend([0 for j in range(m.getContents()[i+1].getPosition()-(m.contents[i].getPosition() + m.contents[i].getSize()))])
	memArray.extend([1 for j in range(m.getContents()[m.numPrograms()-1].getSize())])
	memArray.extend([0 for j in range(100- len(memArray))])
	x = [i for i in range(100)]
	ymin = [0 for i in range(100)]
	a = np.array(memArray)
	pp.vlines(x, ymin, a)
	pp.ylim(0,1)
	pp.show()
	

simulate(100, 100)

