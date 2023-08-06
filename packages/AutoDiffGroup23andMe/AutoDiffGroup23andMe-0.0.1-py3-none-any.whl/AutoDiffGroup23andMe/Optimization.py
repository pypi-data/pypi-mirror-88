from AutoDiffGroup23andMe import AutoDiff as ad
import numpy as np
import matplotlib.pyplot as plt


class Optimizer():
    '''
    abstract class for optimization and visualization
    
    Parameters:
    ----------
    cur_x : int, float, ad.AutoDiff object, numpy.ndarray, or list
        starting x value(s) for minimum
    func : function
        function with single output taking same number of inputs as the length of cur_x
    epsilon: float, optional (default epsilon = .00001)
        step size stopping condition, algorithm stops if the absolute value of step size is below epsilon
    eta: float, optional (default eta=0.01)
        learning rate for algorithm
    max_iter: int, optional (default = 10000)
        maximum number of iterations for algorithm, algorithm stops after reaching maximum number
        
    '''
    def __init__(self, cur_x, func, epsilon = 0.00001, eta=0.01, max_iter = 10000):
        self.cur_x = cur_x
        self.func = func
        self.epsilon = epsilon
        self.eta = eta
        self.max_iter = max_iter
        self.x_history = [] # stores history of x value(s)
        self.h_history=[] # stores history of function value(s)
        self.grad_history = [] # stores history of gradient value(s)
        self.iters = 0 # records number of iterations

    def optimize(self):
        '''
        not implemented in abstract class
        '''
        raise NotImplementedError
    
    def plot_history(self, position = None):
        '''
        function for visualizing x_history, h_history, and grad_history
        
        Parameters:
        ----------
        position : int, optional for single inputs
            column index of x variable that is to be graphed
            
        '''
        assert self.x_history != [], "History is empty"
        # creates list of x values to be graphed (based on position if there are more than 1 x variable)
        if hasattr(self.x_history[0], "__len__") and len(self.x_history[0])>1:
            assert position is not None, "Specify position of x to graph"
            x_history = [x[position] for x in self.x_history]
            grad_history = [grad[position] for grad in self.grad_history]
        else:
            x_history = self.x_history
            grad_history = self.grad_history
        # generates plot
        fig, ax = plt.subplots()
        ax.plot(x_history,self.h_history,label='Function')
        ax.plot(x_history,grad_history,label='Derivative')
        m = ax.scatter(x_history,self.h_history, label='Steps', c = np.arange(self.iters+1), cmap = "viridis")
        cbar = plt.colorbar(m, label='Iterations')
        ax.set_xlabel("Variable Value")
        ax.set_xlabel("Function Value")
        ax.set_title("Function and Derivative Plot Across Iterations")
        ax.legend()
        plt.show()

class GradientDescent(Optimizer):
    '''
    
    class for gradient descent algorithm for finding minimum of function
    
    see parameters of Optimizer class
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optimize(self):
        '''
        Parameters:
        ----------
        None
        
        Returns:
        ----------
        x_val : float (if single variable)
            minimum value
        x_val_1d : numpy.array of floats (if multiple variables)
            minimum values
        
        '''
        # multivariable case of gradient descent
        if hasattr(self.cur_x, "__len__"):
            if len(self.cur_x) > 1:
                x_values = ad.makeVars(self.cur_x)
                m = len(x_values)
                h = self.func(*x_values)
                x_val_1d = np.array([x.val for x in x_values]).reshape(-1)
                self.x_history.append(x_val_1d)
                self.h_history.append(h.val)
                self.grad_history.append(h.der)
                for i in range(self.max_iter):
                    self.iters+=1
                    step_size = self.eta * h.der
                    x_val_1d = x_val_1d - step_size
                    self.cur_x = x_val_1d
                    x_values = ad.makeVars(x_val_1d)
                    h = self.func(*x_values)
                    self.x_history.append(x_val_1d)
                    self.h_history.append(h.val)
                    self.grad_history.append(h.der)
                    abs_step_size = np.linalg.norm(step_size)
                    if abs_step_size < self.epsilon:
                        break
                return x_val_1d
            else:
                self.cur_x = self.cur_x[0]
        
        # single variable case of gradient descent
        if not isinstance(self.cur_x, ad.AutoDiff):
            self.cur_x = ad.AutoDiff(self.cur_x, 1)
        h = self.func(self.cur_x)
        self.x_history.append(self.cur_x.val)
        self.h_history.append(h.val)
        self.grad_history.append(h.der)
        for i in range(self.max_iter):
            self.iters += 1
            step_size = ad.AutoDiff(self.eta*h.der,0)
            self.cur_x = self.cur_x - step_size
            h = self.func(self.cur_x)
            self.x_history.append(self.cur_x.val)
            self.h_history.append(h.val)
            self.grad_history.append(h.der)
            abs_step_size = np.absolute(step_size.val)
            if abs_step_size < self.epsilon:
                break
        return self.cur_x.val

class StochasticGradientDescent(Optimizer):
    '''
    class for stochastic gradient descent and regular gradient descent algorithm for finding parameters of linear regression function with mean-squared error loss function
    
    Parameters:
    cur_x : numpy.ndarray or list
        first value is starting bias value, other values are starting predictor values
    data : numpy.ndarray
        data with last column as response variable and 1st through 2nd to last columns as predictor variables
    batch_size : int, optional (default = None)
        sample size for each iteration of stochastic gradient descent
    epsilon: float, optional (default epsilon = .00001)
        step size stopping condition, algorithm stops if the absolute value of step size is below epsilon
    eta: float, optional (default eta=0.01)
        learning rate for algorithm
    max_iter: int, optional (default = 10000)
        maximum number of iterations for algorithm, algorithm stops after reaching maximum number
        
    '''
    def __init__(self, cur_x, data, batch_size = None, epsilon = 0.00001, eta=0.01, max_iter = 10000):
        self.data = data
        self.batch_size = batch_size
        self.cur_x = cur_x
        self.epsilon = epsilon
        self.eta = eta
        self.max_iter = max_iter
        self.x_history = []
        self.grad_history = []
        self.h_history=[]
        self.iters = 0
        

    def optimize(self):
        '''
        Parameters:
        ----------
        None
        
        Returns:
        ----------
        x_val : float (if single variable)
            minimum value
        x_val_1d : numpy.array of floats (if multiple variables)
            minimum values
        '''
        n_all = len(self.data)
        if self.batch_size is None:
            self.batch_size = n_all
        assert self.batch_size <= n_all, "Batch size must be smaller than number of observations"
        num_weights = len(self.data[0])
        assert n_all > 0 and num_weights >= 2, "Data must have 1 or more rows and 2 or more columns"
        assert isinstance(self.cur_x, list), "Current x values must be list"
        assert num_weights == len(self.cur_x), "Number of predictors must match the number of current x values"
        X_all = self.data[:,:-1]
        y_all = self.data[:,-1]
        
        self.cur_x= [ad.AutoDiff(self.cur_x[i], _init_grad_vec(num_weights, i)) for i in range(num_weights)]
        def loss(weights, X, y, n):
            return (1 / n) * sum([(np.dot(weights[1:], X[i]) + weights[0] - y[i]) ** 2 for i in range(n)])
        X, y = _make_batch(X_all, y_all, self.batch_size)
        h = loss(self.cur_x, X, y, self.batch_size)
        x_val_1d = np.reshape(np.array([x_i.val for x_i in self.cur_x]), (-1))
        self.x_history.append(x_val_1d)
        self.h_history.append(h.val)
        self.grad_history.append(h.der)

        for i in range(self.max_iter):
            X, y = _make_batch(X_all, y_all, self.batch_size)
            self.iters+=1
            step_size = self.eta * h.der
            x_val_1d = x_val_1d - step_size
            self.cur_x = [ad.AutoDiff(x_i_val, _init_grad_vec(num_weights, i)) for i, x_i_val in enumerate(x_val_1d)]
            h = loss(self.cur_x, X, y, self.batch_size)
            self.x_history.append(x_val_1d)
            self.h_history.append(h.val)
            self.grad_history.append(h.der)
            abs_step_size = sum(np.absolute(step_size))
            if abs_step_size < self.epsilon:
                break
                
        return x_val_1d

def _init_grad_vec(length, position):
    '''
    helper function for creating gradient vectors for multidimensional case
    parameters are length and position
    returns a numpy.ndarray with length "length" of all zeros as elements except for a 1 at position "position"
    '''
    vec = np.zeros(length)
    vec[position] = 1
    return vec

def _make_batch(X, y, batch_size):
    '''
    helper function for randomly creating batches
    parameters are X and y, both numpy.ndarrays, and batch_size, which is an int
    returns a subset of X and y with batch_size number of rows
    '''
    if batch_size == X.shape[0]:
        return X, y
    random_ind = np.random.choice(X.shape[0], size=batch_size, replace=False)
    return X[random_ind, :], y[random_ind]



class BFGS(Optimizer):
    '''
    class for Broyden–Fletcher–Goldfarb–Shanno algorithm for finding minimum of function
    
    see parameters of Optimizer class
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optimize(self):
        '''
        Parameters:
        ----------
        None
        
        Returns:
        ----------
        x_val : float (if single variable)
            minimum value
        x_val_1d : numpy.array of floats (if multiple variables)
            minimum values
        
        '''
        if hasattr(self.cur_x, "__len__"): 
            # multivariable case of BFGS
            if len(self.cur_x) > 1:
                x_values = ad.makeVars(self.cur_x)
                m = len(x_values)
                identity = np.identity(m)
                h = self.func(*x_values)
                x_val_1d = np.array([x.val for x in x_values]).reshape(-1)
                self.x_history.append(x_val_1d)
                self.h_history.append(h.val)
                self.grad_history.append(h.der)
                inv_hess = np.identity(m)

                for i in range(self.max_iter):
                    self.iters += 1
                    step_size = (-1*inv_hess @ h.der.reshape((m,1))).reshape(-1)
                    old_x = x_val_1d
                    x_val_1d = x_val_1d + step_size
                    self.cur_x = x_val_1d
                    x_values = ad.makeVars(x_val_1d)
                    h = self.func(*x_values)
                    self.x_history.append(x_val_1d)
                    self.h_history.append(h.val)
                    self.grad_history.append(h.der)
                    abs_step_size = np.linalg.norm(step_size)
                    if abs_step_size < self.epsilon:
                        break

                    y = self.func(*ad.makeVars(x_val_1d)).der - self.func(*ad.makeVars(old_x)).der

                    rho = 1 / np.dot(y,step_size)
                    delta_hess = (identity - rho*step_size.reshape((m,1)) @ y.reshape((1,m)) ) @ inv_hess @ (identity - rho * y.reshape((m,1)) @ step_size.reshape((1,m)) ) + (rho * step_size.reshape((m,1)) @ step_size.reshape((1,m)) )
                    inv_hess = delta_hess

                return x_val_1d

            else:
                self.cur_x = self.cur_x[0]
        # scalar case of BFGS
        if not isinstance(self.cur_x, ad.AutoDiff):
            self.cur_x = ad.AutoDiff(self.cur_x, 1)
        h = self.func(self.cur_x)
        self.x_history.append(self.cur_x.val)
        self.h_history.append(h.val)
        self.grad_history.append(h.der)
        inv_hess = np.identity(1)
        for i in range(self.max_iter):
            self.iters += 1
            step_size = ad.AutoDiff((-1*inv_hess * h.der)[0][0], 0)
            new_x = self.cur_x + step_size
            h = self.func(new_x)
            self.x_history.append(self.cur_x.val)
            self.h_history.append(h.val)
            self.grad_history.append(h.der)
            abs_step_size = np.absolute(step_size.val)
            if abs_step_size < self.epsilon:
                break
            y = self.func(new_x).der - self.func(self.cur_x).der
            identity = np.identity(1)
            rho = 1 / (y * step_size.val)
            delta_hess = (identity - step_size.val * rho * y) * inv_hess * (identity - rho * y * step_size.val) + rho * step_size.val * step_size.val
            self.cur_x = new_x
            inv_hess = delta_hess

        return self.cur_x.val

class ConjugateGradientDescent(Optimizer):
    '''
    class for conjugate gradient descent algorithm for finding minimum of function
    
    see parameters of Optimizer class
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optimize(self):
        '''
        Parameters:
        ----------
        None
        
        Returns:
        ----------
        x_val : float (if single variable)
            minimum value
        x_val_1d : numpy.array of floats (if multiple variables)
            minimum values
        
        '''
        if hasattr(self.cur_x, "__len__"): 
            # multivariable case of gradient decent
            if len(self.cur_x) > 1:
                x_values = ad.makeVars(self.cur_x)
                m = len(x_values)
                h = self.func(*x_values)
                x_val_1d = np.array([x.val for x in x_values]).reshape(-1)
                self.x_history.append(x_val_1d)
                self.h_history.append(h.val)
                self.grad_history.append(h.der)
                for i in range(self.max_iter):
                    self.iters+=1
                    x_values = ad.makeVars(x_val_1d)
                    h = self.func(*x_values)
                    delta_x = -h.der
                    if i == 0:
                        step_size = delta_x
                    else:
                        step_size = delta_x + (np.dot(delta_x,delta_x)/np.dot(prev_delta_x,prev_delta_x))*prev_step_size
                    alpha = _BFGS_linesearch(self.func, x_val_1d, step_size)
                    x_val_1d = x_val_1d + alpha*step_size
                    prev_delta_x = delta_x
                    prev_step_size = step_size
                    self.cur_x = x_val_1d
                    self.x_history.append(x_val_1d)
                    self.h_history.append(h.val)
                    self.grad_history.append(h.der)
                    abs_step_size = np.linalg.norm(alpha*step_size)
                    if abs_step_size < self.epsilon:
                        break
                return x_val_1d
            else:
                self.cur_x = self.cur_x[0]
        if not isinstance(self.cur_x, ad.AutoDiff):
            self.cur_x = ad.AutoDiff(self.cur_x, 1)
        h = self.func(self.cur_x)
        self.x_history.append(self.cur_x.val)
        self.h_history.append(h.val)
        self.grad_history.append(h.der)
        for i in range(self.max_iter):
            self.iters += 1
            h = self.func(self.cur_x)
            delta_x = -h.der
            if i == 0:
                step_size = delta_x
            else:
                step_size = delta_x + (delta_x**2/prev_delta_x**2)*prev_step_size
            alpha = _BFGS_linesearch(self.func, self.cur_x.val, step_size)
            self.cur_x = self.cur_x + step_size*alpha
            prev_delta_x = delta_x
            prev_step_size = step_size
            self.x_history.append(self.cur_x.val)
            self.h_history.append(h.val)
            self.grad_history.append(h.der)
            abs_step_size = np.absolute(step_size*alpha)
            if abs_step_size < self.epsilon:
                break
        return self.cur_x.val

def _BFGS_linesearch(func, xk, dk):
    # helper function for conjugate gradient descent algorithm
    phi = _make_phi(func,xk,dk)
    bfgs_minimizer = BFGS(cur_x = 0.01, func = phi)
    bfgs_min = bfgs_minimizer.optimize()
    return bfgs_min

def _make_phi(func, xk, dk):
    # helper function for conjugate gradient descent algorithm
    def phi(alpha):
        if hasattr(xk,'__len__') and hasattr(dk,'__len__'):
            to_eval = [alpha*d+x for x, d in zip(xk,dk)]
            return func(*to_eval)
        else:
            to_eval = alpha*dk+xk
            return func(to_eval)
    return phi
