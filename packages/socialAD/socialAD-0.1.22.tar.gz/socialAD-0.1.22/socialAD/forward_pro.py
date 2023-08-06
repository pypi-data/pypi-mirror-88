import numpy as np
import socialAD.forward as f
from socialAD.forward import forwardAD

class forwardAD_pro:

    def __init__(self, val=None, der_vector=None, numvar = 1, idx = 0, func=None, dera=None):
        
        if (func == None) and (dera == None): 
            self.func = forwardAD(val, der_vector, numvar, idx)
            self.dera = 1.0
        else:
            self.func = func
            self.dera = dera


    #Overloaded addition
    def __add__(self, other):

        #For adding of the same class, add derivatives
        try:
            out_func = self.func + other.func
            out_dera = self.dera + other.dera

        #For adding a float, keep derivative
        except AttributeError:
            out_func = self.func + other
            out_dera = self.dera

        return forwardAD_pro(func=out_func, dera=out_dera)

    #Overloaded subtraction
    def __sub__(self, other):

        #For subtracting of the same class, subtract derivatives
        try:
            out_func = self.func - other.func
            out_dera = self.dera - other.dera

        #For subtracting a float, keep derivative
        except AttributeError:
            out_func = self.func - other
            out_dera = self.dera

        return forwardAD_pro(func=out_func, dera=out_dera)

    #Overloaded multiplication
    def __mul__(self, other):

        #For multiplying the same class, use product rule
        try:
            out_func = self.func * other.func
            out_dera = self.dera * other.func + self.func * other.dera

        #For multiplying a float, multiply the value
        except AttributeError:
            out_func = self.func * other
            out_dera = self.dera * other

#        print((out_func.der[0]))

        return forwardAD_pro(func=out_func, dera=out_dera)

    #Overloaded division
    def __truediv__(self, other):

        #For dividing the same class, use quotient rule
        try:
            out_func = self.func / other.func
            out_dera = (self.dera * other.func - self.func * other.dera)/(other.func ** 2.0)

        #For dividing a float, divide the funcue
        except AttributeError:
            out_func = self.func / other
            out_dera = self.dera / other

        return forwardAD_pro(func=out_func, dera=out_dera)

    #Overloaded power
    def __pow__(self, other):

    #For power to same class, use logarithmic differentiation
        try:
            out_func = self.func ** other.func
            out_dera = (other.dera * f.log(self.func) + other.func * (self.dera / self.func)) * (self.func ** other.func)

        #For raising to a float, do power rule
        except AttributeError:
            out_func = self.func ** other
            out_dera = self.dera * other * self.func **(other - 1.0)

        return forwardAD_pro(func=out_func, dera=out_dera)

    ### Reversed Operations ###

    # Addition is commutative
    def __radd__(self, other):
        return self.__add__(other)

    # Reverse subtraction
    def __rsub__(self, other):

        #If another of same type, then reverse ordera of subtraction
        try:
            out_func = other.func - self.func
            out_dera = other.dera - self.dera

        #If a float, then reverse ordera subtract
        except AttributeError:
            out_func = other - self.func
            out_dera = -1.0 * self.dera

        return forwardAD_pro(func=out_func, dera=out_dera)

    #Multiplication is commutative
    def __rmul__(self, other):
        return self.__mul__(other)

    #Reverse division
    def __rtruediv__(self, other):
        #For dividing the same class, use reversed quotient rule
        try:
            out_func = other.func / self.func
            out_dera = (other.dera * self.func - other.func * self.dera)/(self.func ** 2.0)

        #For dividing a float, take deraivative of f**(-1) using power rule
        except AttributeError:
            out_func = other / self.func
            out_dera = (-1.0) * other * self.dera / (self.func**2.0)

        return forwardAD_pro(func=out_func, dera=out_dera)

    #Reverse power
    def __rpow__(self, other):

        #If base is same class, do logarithmic differentiation
        try:
            out_func = other.func ** self.func
            out_dera = (self.dera * f.log(other.func) + self.func * (other.dera / other.func)) * (other.func ** self.func)

        #If base is a float, then b^x deraivative rule
        except AttributeError:
            out_func = other ** self.func
            out_dera = other ** self.func * self.dera * f.log(other)

        return forwardAD_pro(func=out_func, dera=out_dera)


##############################################
######       Elementary Functions       ######
##############################################

#For getting an 'e'
class e(forwardAD_pro):
    def __init__(self, func=f.e(), dera=0.0):
        self.func = func
        self.dera = dera

#For getting a log, defaults to natural log
class log(forwardAD_pro):
    def __init__(self, inputs, base = f.e()):

        #For getting log of variable expression, log is derivative/val
        try:
            self.func = f.log(inputs.func)/f.log(base)
            self.dera = inputs.dera / inputs.func

        #For log of float, use numpy.log
        except AttributeError:
            self.func = f.log(inputs) / f.log(base)
            self.dera = 0.0


#####  Trignometric Functions #####

#For getting a sine
class sin(forwardAD_pro):
    def __init__(self, inputs):

        #For getting sine of variable expression, der = in.dera * cos(in.func)
        try:
            self.func = f.sin(inputs.func)
            self.dera = inputs.dera * f.cos(inputs.func)

        #For sine of float, use numpy.sin
        except AttributeError:
            self.func = f.sin(inputs)
            self.dera = 0.0


#For getting a cosine
class cos(forwardAD_pro):
    def __init__(self, inputs):

        #For getting cosine of variable expression, der = -in.dera * sin(in.func)
        try:
            self.func = f.cos(inputs.func)
            self.dera = -inputs.dera * f.sin(inputs.func)

        #For cosine of float, use numpy.cos
        except AttributeError:
            self.func = f.cos(inputs)
            self.dera = 0.0


#For getting a tangent
class tan(forwardAD_pro):
    def __init__(self, inputs):

        #For getting tangent of variable expression, der = in.dera * (1 + tan(in.func)^2)
        try:
            self.func = f.tan(inputs.func)
            self.dera = inputs.dera * (1 + f.tan(inputs.func)**2)

        #For tanget of float, use numpy.tan
        except AttributeError:
            self.func = f.tan(inputs)
            self.dera = 0.0


##### Inverse Trignometric Functions #####

#For getting a inverse sine
class arcsin(forwardAD_pro):
    def __init__(self, inputs):

        #For getting arcsin of variable expression, der = in.dera * (1/sqrt(1-inputs.func**2))
        try:
            self.func = f.arcsin(inputs.func)
            self.dera = inputs.dera * (1/f.sqrt(1-inputs.func**2))

        #For arcsin of float, use numpy.arcsin
        except AttributeError:
            self.func = f.arcsin(inputs)
            self.dera = 0.0


#For getting a inverse cosine
class arccos(forwardAD_pro):
    def __init__(self, inputs):

        #For getting arccos of variable expression, der = -in.dera * sin(in.func)
        try:
            self.func = f.arccos(inputs.func)
            self.dera = -inputs.dera * (1/f.sqrt(1-inputs.func**2))

        #For arccos of float, use numpy.arccos
        except AttributeError:
            self.func = f.arccos(inputs)
            self.dera = 0.0


#For getting a inverse tangent
class arctan(forwardAD_pro):
    def __init__(self, inputs):

        #For getting arctan of variable expression, der = in.dera * (1 / in.func^2)
        try:
            self.func = f.arctan(inputs.func)
            self.dera = inputs.dera * (1/(1+inputs.func**2))

        #For arctan of float, use numpy.arctan
        except AttributeError:
            self.func = f.arctan(inputs)
            self.dera = 0.0

##### Hyperbolic Trignometric Functions #####

#For getting a hyperbolic sine
class sinh(forwardAD_pro):
    def __init__(self, inputs):

        #For getting sinh of variable expression, der = in.dera * sinh(in.func)
        try:
            self.func = f.sinh(inputs.func)
            self.dera = f.cosh(inputs.func)

        #For sine of float, use numpy.tan
        except AttributeError:
            self.func = f.sinh(inputs)
            self.dera = 0.0


#For getting a hyperbolic cosh
class cosh(forwardAD_pro):
    def __init__(self, inputs):

        #For getting cosh of variable expression, der = in.dera * sinh(in.func)
        try:
            self.func = f.cosh(inputs.func)
            self.dera = f.sinh(inputs.func)

        #For sine of float, use numpy.cos
        except AttributeError:
            self.func = f.cosh(inputs)
            self.dera = 0.0

#For getting a hyperbolic tangent
class tanh(forwardAD_pro):
    def __init__(self, inputs):

        #For getting tangent of variable expression, der = in.dera * (1 + tan(in.func)^2)
        try:
            self.func = f.tanh(inputs.func)
            self.dera = inputs.dera * (1 - f.tanh(inputs.func)**2)

        #For sine of float, use numpy.tan
        except AttributeError:
            self.func = f.tanh(inputs)
            self.dera = 0.0


#Vector Implementation
class vector_func: #vector_func(f1, f2, ...)
    def __init__(self, *args): #  
        jacobian_array = []
        values_array = []
        for function in args: 
                jacobian_array.append(list(function.func.der))
                values_array.append(list(function.func.val))
                hessian_array.append(list(function.dera.der))
        self.jacobian_array = np.array(jacobian_array)
        self.values_array = np.array(values_array)

    def jacobian(self):
        return self.jacobian_array
    def values(self):
        return self.values_array



