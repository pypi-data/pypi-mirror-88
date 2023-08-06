from socialAD.forward import *
import numpy as np


### Implementation of Broyden's Optimization Method ###
# More computationally efficient than Newton's method #

#Broyden function
def broyden(function, variables, init_values):

	#Check user input types (string or list of strings)
	if not isinstance(function,str):

		#Vector function case
		if not isinstance(function,list):
			raise TypeError('function input must be either string or list of strings')

		if not isinstance(function[0],str):
			raise TypeError('function input must be either string or list of strings')

	#Check user input types (string or list of strings)
	if not isinstance(variables,str):

		#Vector function case
		if not isinstance(variables,list):
			raise TypeError('Each input must be either string or list of strings')

		if not isinstance(variables[0],str):
			raise TypeError('Each input must be either string or list of strings')

	#Check inital values is a list
	if not isinstance(init_values,list):
		
		raise TypeError('initial values must be a list')

	#Check that initial values and variables match in length
	if not len(variables) == len(init_values):

		raise Error('number of initial values must match number of variables')

	#Broyden's method for non-vector function
	if isinstance(function,str):

		#If just one string, convert to list
		if isinstance(variables,str):

			variables = [variables]

		#Convert to numpy arrays
		variables = np.array(variables)
		init_values = np.array(init_values)

		#Loop through variable names
		for index, variable in enumerate(variables):

			#Store to variable name
			name = variable

			#Save as forwardAD object
			exec(name + " = forwardAD(np.array([init_values[index]]), numvar = len(variables), idx = index)")

		#Stores full function as a forwardAD object
		AD_function = eval(function)

		#First iteration is Newton's method
		new_values = init_values - (AD_function.val / AD_function.der)

		#Store init as last values
		previous_values = init_values

		#Stores function value as previoust function value
		previous_function_val = AD_function.val

		#Iterate using finite differences until find good enough root
		while abs(AD_function.val) > 1e-7:

			#Loop through variable names
			for index, variable in enumerate(variables):

				#Store to variable name
				name = variable

				#Save as forwardAD object
				exec(name + " = forwardAD(np.array([new_values[index]]), numvar = len(variables), idx = index)")

			#Stores full function as a forwardAD object
			AD_function = eval(function)

			#Evaluate finite difference
			finite_difference = (AD_function.val - previous_function_val) / (new_values - previous_values)

			#Store function value
			previous_function_val = AD_function.val

			#Store domain values
			previous_values = new_values

			#Next estiamte
			new_values = previous_values - (AD_function.val / finite_difference)

		return new_values, AD_function.val

	#Case of vector function
	else:

		#List to store functions
		vector = []

		#If just one string, convert to list
		if isinstance(variables,str):

			variables = [variables]

		#Convert to numpy arrays
		variables = np.array(variables)
		init_values = np.array(init_values)

		#Loop through functions
		for func in function:

			#Loop through variable names
			for index, variable in enumerate(variables):

				#Store to variable name
				name = variable

				#Save as forwardAD object
				exec(name + " = forwardAD(np.array([init_values[index]]), numvar = len(variables), idx = index)")

			#Stores full function in vector of functions as forwardAD object
			vector.append(eval(func))

		#Store as a vector function
		AD_vector = vector_func(*vector)

		#Store values
		previous_values = init_values
		previous_values = previous_values.reshape(len(previous_values),1)

		#Store jacobian
		previous_jacobian = AD_vector.jacobian()

		#Store function values
		previous_function_val = AD_vector.values()

		new_values = previous_values - np.matmul(np.linalg.pinv(AD_vector.jacobian()),AD_vector.values())
		new_values = new_values.reshape(1,-1)[0]

		#Loop counter
		loop = 0

		#Iterate using finite differences until find good enough root
		while (np.linalg.norm(AD_vector.values()) > 1e-7):

			#List to store functions
			vector = []

			#Loop through functions
			for func in function:

				#Loop through variable names
				for index, variable in enumerate(variables):

					#Store to variable name
					name = variable

					#Save as forwardAD object
					exec(name + " = forwardAD(np.array([new_values[index]]), numvar = len(variables), idx = index)")

				#Stores full function in vector of functions as forwardAD object
				vector.append(eval(func))

			#Store as a vector function
			AD_vector = vector_func(*vector)

			#differences
			previous_values = previous_values.reshape(1,-1)[0]
			delta_f = AD_vector.values() - previous_function_val
			delta_x = new_values - previous_values
			# print(previous_values)
			delta_x = delta_x.reshape(len(delta_x),1)

			#Evaluate finite jacobian
			finite_jacobian = previous_jacobian + np.matmul((delta_f - np.matmul(previous_jacobian, delta_x)) / np.linalg.norm(delta_x),delta_x.T)

			#Store function value
			previous_function_val = AD_vector.values()

			#Store domain values
			previous_values = new_values
			previous_values = previous_values.reshape(len(previous_values),1)

			#Next estiamte
			new_values = previous_values - np.matmul(np.linalg.pinv(finite_jacobian),AD_vector.values())
			new_values = new_values.reshape(1,-1)[0]

			if loop > 10000:

				raise ValueError('Too many iterations - could not converge')

			loop += 1

		return new_values, AD_vector.values()


### Implementation of Newton's Method ###

#Newton function
def newton(function, variables, init_values):

	#Check user input types (string or list of strings)
	if not isinstance(function,str):

		#Vector function case
		if not isinstance(function,list):
			raise TypeError('function input must be either string or list of strings')

		if not isinstance(function[0],str):
			raise TypeError('function input must be either string or list of strings')

	#Check user input types (string or list of strings)
	if not isinstance(variables,str):

		#Vector function case
		if not isinstance(variables,list):
			raise TypeError('Each input must be either string or list of strings')

		if not isinstance(variables[0],str):
			raise TypeError('Each input must be either string or list of strings')

	#Check inital values is a list
	if not isinstance(init_values,list):
		
		raise TypeError('initial values must be a list')

	#Check that initial values and variables match in length
	if not len(variables) == len(init_values):

		raise Error('number of initial values must match number of variables')

	#Broyden's method for non-vector function
	if isinstance(function,str):

		#If just one string, convert to list
		if isinstance(variables,str):

			variables = [variables]

		#Convert to numpy arrays
		variables = np.array(variables)
		init_values = np.array(init_values)

		#Loop through variable names
		for index, variable in enumerate(variables):

			#Store to variable name
			name = variable

			#Save as forwardAD object
			exec(name + " = forwardAD(np.array([init_values[index]]), numvar = len(variables), idx = index)")

		#Stores full function as a forwardAD object
		AD_function = eval(function)

		#First iteration is Newton's method
		new_values = init_values - (AD_function.val / AD_function.der)

		#Store init as last values
		previous_values = init_values

		#Stores function value as previoust function value
		previous_function_val = AD_function.val

		#Iterate using finite differences until find good enough root
		while abs(AD_function.val) > 1e-7:

			#Loop through variable names
			for index, variable in enumerate(variables):

				#Store to variable name
				name = variable

				#Save as forwardAD object
				exec(name + " = forwardAD(np.array([new_values[index]]), numvar = len(variables), idx = index)")

			#Stores full function as a forwardAD object
			AD_function = eval(function)

			#Store function value
			previous_function_val = AD_function.val

			#Store domain values
			previous_values = new_values

			#Next estiamte
			new_values = previous_values - (AD_function.val / AD_function.der)

		return new_values, AD_function.val

	#Case of vector function
	else:

		#List to store functions
		vector = []

		#If just one string, convert to list
		if isinstance(variables,str):

			variables = [variables]

		#Convert to numpy arrays
		variables = np.array(variables)
		init_values = np.array(init_values)

		#Loop through functions
		for func in function:

			#Loop through variable names
			for index, variable in enumerate(variables):

				#Store to variable name
				name = variable

				#Save as forwardAD object
				exec(name + " = forwardAD(np.array([init_values[index]]), numvar = len(variables), idx = index)")

			#Stores full function in vector of functions as forwardAD object
			vector.append(eval(func))

		#Store as a vector function
		AD_vector = vector_func(*vector)

		#Store values
		previous_values = init_values
		previous_values = previous_values.reshape(len(previous_values),1)

		#Store jacobian
		previous_jacobian = AD_vector.jacobian()

		#Store function values
		previous_function_val = AD_vector.values()

		new_values = previous_values - np.matmul(np.linalg.pinv(AD_vector.jacobian()),AD_vector.values())
		new_values = new_values.reshape(1,-1)[0]

		#Loop counter
		loop = 0

		#Iterate using finite differences until find good enough root
		while (np.linalg.norm(AD_vector.values()) > 1e-7):

			#List to store functions
			vector = []

			#Loop through functions
			for func in function:

				#Loop through variable names
				for index, variable in enumerate(variables):

					#Store to variable name
					name = variable

					#Save as forwardAD object
					exec(name + " = forwardAD(np.array([new_values[index]]), numvar = len(variables), idx = index)")

				#Stores full function in vector of functions as forwardAD object
				vector.append(eval(func))

			#Store as a vector function
			AD_vector = vector_func(*vector)

			#Store function value
			previous_function_val = AD_vector.values()

			#Store domain values
			previous_values = new_values
			previous_values = previous_values.reshape(len(previous_values),1)

			#Next estiamte
			new_values = previous_values - np.matmul(np.linalg.pinv(AD_vector.jacobian()),AD_vector.values())
			new_values = new_values.reshape(1,-1)[0]

			if loop > 10000:

				raise ValueError('Too many iterations - could not converge')

			loop += 1

		return new_values, AD_vector.values()

