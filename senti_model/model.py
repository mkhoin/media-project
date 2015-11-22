import numpy as np
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC

class StatModel:
	name = ""
	
	def train(self, samples, labels):
		pass
	
	def predict(self, samples):
		pass


class NaiveBayes(StatModel):
	def __init__(self):
		self.name  = "nb"
		self.model = BernoulliNB()

	def train(self, samples, labels):
		self.model.fit(samples, labels)
				
	def predict(self, samples):
		return self.model.predict(samples)
		

class SVM(StatModel):
	def __init__(self, g = 0):
		self.name = "svm"
		if g == 0: self.model = SVC(kernel="rbf")
		else: self.model = SVC(kernel="rbf", gamma=g)

	def train(self, samples, labels):
		self.model.fit(samples, labels)

	def predict(self, samples):
		return self.model.predict(samples)

