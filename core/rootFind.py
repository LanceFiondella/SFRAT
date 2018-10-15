import scipy.optimize


class RootFind():
    """Root Finding object that will return a root based on the algorithm
    selected
    """
    bracketedAlgos = ['brentq', 'brenth', 'ridder', 'bisect']
    nonbracketedAlgos = ['newton']

    def __init__(self, *args, **kwargs):
        """
        Initializes the RootFind object

        Keyword Args:
            algoName: string of algorithm to be used
            equation: function whose root is to be found
            data: Data being used (Can be useful to find root)

        """
        self.algoName = kwargs['rootAlgoName']
        self.algo = getattr(scipy.optimize, self.algoName)
        if self.algoName in self.bracketedAlgos:
            self.bracket = True
        else:
            self.bracket = False
        self.equation = kwargs['equation']
        self.data = kwargs['data']

    def findEndpoints(self, maxIterations=100000):
        """
        Finds the end points to find roots

        Keyword Args:
            maxIterations: Maximum iterations to search for end points
                           for root finding
        Returns:
            Left and right endpoints as a tuple
        """
        leftEndPoint = len(self.data)
        rightEndPoint = 2 * len(self.data)
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
            root = self.algo(self.equation, leftEndPoint,
                             rightEndPoint, maxiter=10000,
                             full_output=False, disp=True)
        else:
            x0 = len(self.data)
            root = self.algo(self.equation, x0, maxiter=10000)

        return root
