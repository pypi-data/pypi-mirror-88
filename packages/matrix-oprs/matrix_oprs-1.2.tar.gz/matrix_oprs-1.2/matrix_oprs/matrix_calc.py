class Matrix:

	def __init__(self, dims, fill):
		
		self.rows = dims[0]
		self.cols = dims[1]

		self.A = [[fill] * self.cols for i in range(self.rows)]


	def __str__(self):
	    m = len(self.A) # Get the first dimension
	    mtxStr = ''
	    
	    mtxStr += '------------- output -------------\n'
	    
	    for i in range(m):
	        mtxStr += ('|' + ', '.join( map(lambda x:'{0:8.3f}'.format(x), self.A[i])) + '| \n')

	    mtxStr += '----------------------------------'
	
	    return mtxStr

	def __add__(self, other):

		#Create a new matrix
		C = Matrix( dims = (self.rows, self.cols), fill = 0)

		#Check if the other object is of type Matrix
		if isinstance (other, Matrix):
			#Add the corresponding element of 1 matrices to another
			for i in range(self.rows):
				for j in range(self.cols):
					C.A[i][j] = self.A[i][j] + other.A[i][j]

		#If the other object is a scaler
		elif isinstance (other, (int, float)):
			#Add that constant to every element of A
			for i in range(self.rows):
				for j in range(self.cols):
					C.A[i][j] = self.A[i][j] + other


		return C

	#Right addition can be done by calling left addition
	def __radd__(self, other):
		return self.__add__(other)

	def __mul__(self, other): #pointwise multiplication

		C = Matrix( dims = (self.rows, self.cols), fill = 0)
		if isinstance(other, Matrix):

			for i in range(self.rows):
				for j in range(self.cols):
					C.A[i][j] = self.A[i][j] * other.A[i][j]

		#Scaler multiplication
		elif isinstance(other, (int, float)):

			for i in range(self.rows):
				for j in range(self.cols):
					C.A[i][j] = self.A[i][j] * other

		return C