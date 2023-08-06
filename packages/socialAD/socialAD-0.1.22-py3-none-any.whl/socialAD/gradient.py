import numpy as np
from socialAD.forward import forwardAD

def gradient_descent(variables, f, cur_x, rate, precision, previous_step_size, max_iters):
    if isinstance(f, str):

    #If just one string, convert to list
        if isinstance(variables, str):

            variables = [variables]

        #Convert to numpy arrays
        variables = np.array(variables)
        cur_x = np.array(cur_x)

        iters = 0
        while previous_step_size > precision and iters < max_iters:
            for index, variable in enumerate(variables):

                #Store to variable name
                name = variable
                #Save as forwardAD object
                exec(name + " = forwardAD(np.array(cur_x[index]), numvar = len(variables), idx = index)")
            #Stores full function as a forwardAD object
            AD_function = eval(f)
            
            prev_x = cur_x #Store current x value in prev_x
            cur_x = cur_x - rate * AD_function.der #Grad descent
            previous_step_size = np.sum(abs(cur_x - prev_x)) #Change in x
            iters += 1 #iteration count
            
    print("Iteration",iters) #,"\nX value is", cur_x) #Print iterations
    print("The local minimum occurs at", cur_x)


def gd_backtrack(variables, f, cur_x, precision, previous_step_size, max_iters):
    if isinstance(f, str):

    #If just one string, convert to list
        if isinstance(variables, str):

            variables = [variables]

        #Convert to numpy arrays
        variables = np.array(variables)
        cur_x = np.array(cur_x)
        
        f_x = f
        
        if len(variables) > 1:    
            
            for idx_var in np.arange(0, len(variables)):
                f_x = f_x.replace(variables[idx_var], variables[0] + '[' + str(idx_var) + ']')
        to_be_eval = "lambda " + variables[0] + " : " + f_x
        f_ex = eval( to_be_eval)
#        print(f_ex(cur_x))
#######################################
# ITERATIONS >>>>>>>>>>>>>>>>>>>>>>>>>

        iters = 0
        while previous_step_size > precision and iters < max_iters:
            for index, variable in enumerate(variables):

                #Store to variable name
                name = variable

                #Save as forwardAD object
                exec(name + " = forwardAD(np.array(cur_x[index]), numvar = len(variables), idx = index)")
#                print(eval(name))
                
            #Stores full function as a forwardAD object
            AD_function = eval(f)
            
            prev_x = cur_x #Store current x value in prev_x
            ##### ESTIMATE THE MOST EFFICIENT RATE 
            t = 1
            count = 1
            alpha = 0.3
            beta = 0.8
            while (AD_function.val - (f_ex(cur_x - t* AD_function.der) + alpha * t * np.dot( AD_function.der,  AD_function.der))) < 0 and count < max_iters:
                t *= beta

                count += 1
            
            rate = t
            #####
            
            cur_x = cur_x - rate * AD_function.der #Grad descent
            previous_step_size = np.sum(abs(cur_x - prev_x))  #Change in x
            iters += 1 #iteration count
    #        print("Iteration",iters,"\nX value is", cur_x) #Print iterations
#######################################
    print("Iteration",iters)
    print("The local minimum occurs at", cur_x)
    
# BFGS

def BFGS(variables, f, cur_x, precision, max_iters):

    if isinstance(f, str):
    #If just one string, convert to list
        if isinstance(variables, str):

            variables = [variables]

        #Convert to numpy arrays
        variables = np.array(variables)
        cur_x = np.array(cur_x) # points = np.array([2, 2])
        f_x = f
        
        if len(variables) > 1:    
            
            for idx_var in np.arange(0, len(variables)):
                f_x = f_x.replace(variables[idx_var], variables[0] + '[' + str(idx_var) + ']')
    

        to_be_eval = "lambda " + variables[0] + " : " + f_x
        f_ex = eval( to_be_eval)
#######################################        
        previous_step_size = 1
        p = 1e-8
        I = np.identity(len(variables))
        Hk = I
#######################################
# ITERATIONS >>>>>>>>>>>>>>>>>>>>>>>>>

        rate = 0.1
        iters = 0
        while previous_step_size > precision and iters < max_iters:
            for index, variable in enumerate(variables):

                #Store to variable name
                name = variable

                #Save as forwardAD object
                exec(name + " = forwardAD(np.array(cur_x[index]), numvar = len(variables), idx = index)")

            #Stores full function as a forwardAD object
            AD_function = eval(f)
            prev_x = cur_x
            
            neg_f_xk =  - AD_function.der
            s_k = Hk @ neg_f_xk * 0.0001 # with fix learning rate

            cur_x = prev_x + s_k
            y_k = f_ex(cur_x) + neg_f_xk
    
            rho_k = 1/(np.transpose(y_k) @ s_k)
            new_Hk = (I - s_k * rho_k @ np.transpose(y_k)) \
            @ Hk @ (I - rho_k * y_k@np.transpose(s_k))\
            + rho_k * s_k@np.transpose(s_k)
            Hk = new_Hk

            prev_x = cur_x #Store current x value in prev_x
            ##### ESTIMATE THE MOST EFFICIENT RATE 
            #####
            #print(rate)
            #print(AD_function.der)
            cur_x = cur_x - rate * AD_function.der #Grad descent
            previous_step_size = np.sum(abs(cur_x - prev_x)) #Change in x
            iters += 1 #iteration count
            #print("Iteration",iters,"\nX value is", cur_x) #Print iterations
#######################################
    print("Iteration",iters)
    print("The local minimum occurs at", cur_x)
    
    
    
# BFGS

def BFGS_backtrack(variables, f, cur_x, precision, max_iters):
    



    if isinstance(f, str):
    #If just one string, convert to list
        if isinstance(variables, str):

            variables = [variables]

        #Convert to numpy arrays
        variables = np.array(variables)
        cur_x = np.array(cur_x) # points = np.array([2, 2])
       
        f_x = f
        
        if len(variables) > 1:    
            
            for idx_var in np.arange(0, len(variables)):
                f_x = f_x.replace(variables[idx_var], variables[0] + '[' + str(idx_var) + ']')
    
        to_be_eval = "lambda " + variables[0] + " : " + f_x
        f_ex = eval( to_be_eval)
#######################################        
        previous_step_size = 1
        p = 1e-8
        I = np.identity(len(variables))
        Hk = I
#######################################
# ITERATIONS >>>>>>>>>>>>>>>>>>>>>>>>>

        rate = 0.1
        iters = 0
        while previous_step_size > precision and iters < max_iters:
            for index, variable in enumerate(variables):

                #Store to variable name
                name = variable

                #Save as forwardAD object
                exec(name + " = forwardAD(np.array(cur_x[index]), numvar = len(variables), idx = index)")

            #Stores full function as a forwardAD object
            #print(f)
            AD_function = eval(f) ## prev step 
            prev_x = cur_x
            
            neg_f_xk =  - AD_function.der
            s_k = Hk @ neg_f_xk * 0.0001 # with fix learning rate

            cur_x = prev_x + s_k
            
            #######################
            ## backtrack_AD
            #######################
#            t = backtrack_AD(points, 1, alpha, beta, 1)
            
            t = 1
            count = 1
           # print('=============')
           # print(AD_function.val) #<-- SHOULD BE ONE
           # print(cur_x )
           # print(- t* AD_function.der)
            alpha = 0.3
            beta = 0.8
            while (AD_function.val - (f_ex(cur_x - t* AD_function.der) + alpha * t * np.dot( AD_function.der,  AD_function.der))) < 0 and count < max_iters:
                t *= beta
                count += 1
            
            #print(f't: {t}')
            rate = t
            ######################
            y_k = f_ex(cur_x) + neg_f_xk * t 
    
            rho_k = 1/(np.transpose(y_k) @ s_k)
            new_Hk = (I - s_k * rho_k @ np.transpose(y_k)) \
            @ Hk @ (I - rho_k * y_k@np.transpose(s_k))\
            + rho_k * s_k@np.transpose(s_k)
            Hk = new_Hk

            prev_x = cur_x #Store current x value in prev_x
            ##### ESTIMATE THE MOST EFFICIENT RATE 
            #####
            #print(AD_function.der)
            cur_x = cur_x - rate * AD_function.der #Grad descent
            previous_step_size =  np.sum(abs(cur_x - prev_x))  #Change in x
            iters += 1 #iteration count
            #print("Iteration",iters,"\nX value is", cur_x) #Print iterations
#######################################
    print("Iteration",iters)
    print("The local minimum occurs at", cur_x)
    
    
    

