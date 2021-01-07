import scipy.optimize
#from core import bat


class RootFind():
	"""Root Finding object that will return a root based on the algorithm
	selected
	"""
	bracketedAlgos = ['brentq', 'brenth', 'ridder', 'bisect']
	nonbracketedAlgos = ['newton']
	#swarmAlgos = ['bat']
	
	def __init__(self, *args, **kwargs):
		"""
		Initializes the RootFind object

		Keyword Args:
			algoName: string of algorithm to be used
			equation: function whose root is to be found
			data: Data being used (Can be useful to find root)

		"""
		self.algoName = kwargs['rootAlgoName']

		#if self.algoName in self.swarmAlgos:
		#	self.algo = self.swarmAlgo
		#else:
		self.algo = getattr(scipy.optimize, self.algoName)

		if self.algoName in self.bracketedAlgos:
			self.bracket = True
		else:
			self.bracket = False
		self.equation = kwargs['equation']
		self.data = kwargs['data']
		if 'initialEstimate' in kwargs:
			self.initEstimate = kwargs['initialEstimate']
		else:
			self.initEstimate = len(self.data)

	def swarmAlgo(eqn, x0, maxiter, full_output):
		if self.algo == 'bat':
			'''
			6 6 0.021768 0.917212 0.825154 0.823620
			14 6 0.021768 0.922107 0.825076 0.823620
			6 6 0.046744 0.922789 0.825152 0.755835
			'''
			sspace = [[-1, 1] for i in range(len(x0))]
			pop = [x0 for i in range(6)]
			bats = bat.search(eqn, sspace, 14, pop, 0.021768, 0.922107, 0.825076, 0.823620)
			#bats.sort(key = lambda x: eqn())



	def findEndpoints(self, maxIterations=100000):
		"""
		Finds the end points to find roots

		Keyword Args:
			maxIterations: Maximum iterations to search for end points
						   for root finding
		Returns:
			Left and right endpoints as a tuple
		"""
		leftEndPoint = self.initEstimate
		rightEndPoint = 2 * self.initEstimate
		i = 0
		while (self.equation(leftEndPoint)*self.equation(rightEndPoint) > 0 and
			   i <= maxIterations):
			leftEndPoint = leftEndPoint/2
			rightEndPoint = rightEndPoint*2
			i = i + 1

		return (leftEndPoint, rightEndPoint)

	def findRoot(self):
		"""
		Finds the root of the equation

		Returns:
			root: Root of the given equation using the given method

		"""
		if self.bracket:
			leftEndPoint, rightEndPoint = self.findEndpoints()
			result = scipy.optimize.root_scalar(self.equation, method=self.algoName, bracket=[leftEndPoint, rightEndPoint], maxiter=1000)
			root = result.root
			self.converged = result.converged
		else:
			x0 = self.initEstimate
			root, result = self.algo(self.equation, x0, maxiter=1000, full_output=False)
			self.converged = result.converged

		return root
