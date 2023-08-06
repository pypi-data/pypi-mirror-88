"""
Interface for SGD opimizer subclass
""" 

__all__ = ['SGD']

import numpy as np
from .optimizer import Optimizer
from boomdiff.autodiff import AD


class SGD(Optimizer):
    """
    SGD optimizer subclass

    Usage:
    ```python
    >>> # Instantiate an SGD optimizer
    >>> opt = boomdiff.optimize.SGD(learning_rate=0.1)

    >>> # 'loss' should be a callable that takes no arguments and output an AD instance
    >>> # should only use operations supported by AD class
    >>> loss = lambda: var1**2 + var2**2

    >>> # initialize the variables for the objective function
    >>> # make sure the name string in the dict is corresponding with the variable name
    >>> var1 = AD(1, {'var1': 1})
    >>> var2 = AD(2, {'var2': 1})

    >>> # Call step method, update the variables for one step, to minimize the loss value
    >>> # var_list are the variable lists that you want to update
    >>> # It can be part of the variables in loss callable.
    >>> # The step method will update the variables defined before
    >>> opt.step(loss, var_list=[var1, var2])

    >>> # The var1 and var2 will be updated, - learning_rate * grad
    >>> var1
    0.8 ({'var1': 1})
    >>> var2
    1.6 ({'var2': 1})

    >>> # Or you can call minimize method, to update multiple steps
    >>> # With user-specified learning_rate series
    >>> opt.miminize(loss, var_list[var1, var2], learning_rates=np.linspace(0.1,0.01,100), steps=100)

    >>> # This will give some final optimization results if converged
    >>> var1
    0.0 ({'var1': 1})
    >>> var2
    0.0 ({'var2': 1})
    ```
    """

    def __init__(self, learning_rate=0.1, **kwargs):

        super(SGD, self).__init__(learning_rate)

        #TODO, other SGD-specific initializations, like momentum
        #...


    def _apply_gradient(self, loss, var_list, grad_dict):
        """Apply the gradient to update variables, with SGD algorithm

        """
        # TODO, use SGD algorithms, update the variables in the var_list
        # Simple demo codes are:
        # >>> for var in var_list:
        # >>>       var.func_val -= self.lr * grad_dict[var.name()[0]]
        # self.lr is learning rate
        # var.name() is a new method added to AD class, return the keys list in the partial_dict, which is the variable name
        # The simple demo codes should already work to gradient descent the loss fucntion, by updating the vars
        # Need to add some codes to make this method more robust 






















