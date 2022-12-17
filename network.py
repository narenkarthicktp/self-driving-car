import numpy
import pickle
from random import random

class layer():

	def __init__( self, noi, noo) -> None:

		self.noi = noi
		self.noo = noo

		self.weights = numpy.array([ [ -random() for j in range(noi) ] for i in range(noo) ])
		self.biases =  numpy.array([ random()*2-1 for i in range(noo) ])
		self.outputs = numpy.array([ 0 for i in range(noo) ])

	def forward( self, inputs):

		for i in range(self.noo):
			self.outputs[i] = 1 if numpy.dot( self.weights[i], inputs) > self.biases[i] else 0
		return self.outputs

class feed_forward():

	def __init__( self, npl) -> None:

		self.npl = npl
		self.layers = []
		for i in range(len(npl)-1):
			self.layers.append(layer( npl[i],npl[i+1]))

	def forward( self, inputs):

		buffer = self.layers[0].forward(inputs)
		for i in range(1,len(self.layers)):
			buffer = self.layers[i].forward(buffer)
		return buffer

	def serialize( self, filename):

		# print(self.layers[0].weights)
		with open( filename, "wb") as fout:
			pickle.dump( self, fout)

	def mutate( self, amount):

		child = feed_forward(self.npl)
		lerp = lambda a,b,t : a*(1-t) + b*t

		for i in range(len(child.npl)-1):

			for j in range(child.npl[i+1]):
				child.layers[i].biases[j] = lerp( self.layers[i].biases[j], random()*2-1, amount)
				for k in range(child.layers[i].noi):
					child.layers[i].weights[j][k] = lerp( self.layers[i].weights[j][k], random()*2-1, amount)

		return child

def load(filename):
	with open( filename, "rb") as infile:
		some =  pickle.load(infile)
		return some