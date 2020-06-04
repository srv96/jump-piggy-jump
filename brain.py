import numpy as np

class Brain:
	def __init__(self,n_input=None,n_hidden=None,n_output=None,brain=None,flag=False):
		if brain != None:
			self.n = brain.n
			self.weight_0 = brain.weight_0
			self.weight_1 = brain.weight_1

			self.bias_0 = brain.bias_0
			self.bias_1 = brain.bias_1
		else:
			self.n = n_input
			self.weight_0 = np.random.randn(n_hidden,n_input)*0.1
			self.weight_1 = np.random.randn(n_output,n_hidden)*0.1

			self.bias_0 = np.zeros(shape=(n_hidden,1))
			self.bias_1 = np.zeros(shape=(n_output,1))
	def sigmoid(self,input):
		return 1/(1+np.exp(-input))

	def predict(self,input):
		input = np.array(input)
		input.resize((self.n,1))
		z1 = np.dot(self.weight_0,input)+self.bias_0
		a1 = self.sigmoid(z1)
		z2 = np.dot(self.weight_1,a1)+self.bias_1
		a2 = self.sigmoid(z2)
		return a2

	def mutate(self):
		self.weight_0 = self.mutateFunc(self.weight_0)
		self.weight_1 = self.mutateFunc(self.weight_1)
		self.bias_0 = self.mutateFunc(self.bias_0)
		self.bias_1 = self.mutateFunc(self.bias_1)

	def mutateFunc(self,x):
		if np.random.random()<1:
			return x + np.random.normal(0,1)
		else:
			return x
	