"""
Interface for Momentum accelerated Gradient Descent
"""

__all__ = ['Momentum']

import warnings

import numpy as np

from boomdiff.autodiff import AD
from ._optimizer import Optimizer

class Momentum(Optimizer):
    """
    Momentum accelerated Gradient Descent subclass 
    Adding a fraction gamma of the update vector of the past time step to the current update vector:
    v_t = gamma * v_{t-1} + lr * gradient
    theta = theta - v_t

    Usage:
    >>> a = AD(2, 'a')
    >>> loss = lambda: a**2
    >>> # for a installed package, the api is boomdiff.optimize.Momentum() 
    >>> opt_mom = Momentum(learning_rate=0.1, gamma=0.9)
    >>> opt_mom.minimize(loss, [a])
    >>> print(a.round(2))
    -0.01 ({'a': 1.0})
    >>> x1 = AD(5, 'x1')
    >>> x2 = AD(7, 'x2')
    >>> loss2 = lambda: x1**2 + x2**2 + (x1-x2)**2
    >>> opt_mom.init(learning_rate=0.1)
    >>> opt_mom.minimize(loss2, [x1, x2], steps=300)
    >>> print(x1.round(3), x2.round(3))
    0.0 ({'x1': 1.0}) 0.0 ({'x2': 1.0})
    """

    def __init__(self, learning_rate=0.1, gamma=0.9):
        """
        Parameters
        ----------
        learning_rate: int or float

        gamma: int or float
            momentum term
        """
        super(Momentum, self).__init__(learning_rate)
        self.gamma = 0.9

    def init(self, learning_rate=0.1, gamma=0.9):
        """
        initialize the optimizer, if u want to drop the history track and use eleswhere
        """
        # Delete the history track attribute
        if hasattr(self, 'last_update'): delattr(self, 'last_update') 

        # Reinitialize the hyperparameters if set
        self.__init__(learning_rate, gamma)


    def _apply_gradient(self, loss, var_list, grad_dict):
        """
        Apply the gradient to update variables, with Momentum algorithm
        v_t = gamma * v_{t-1} + lr * gradient
        theta = theta - v_t
        """
        if not hasattr(self,'last_update'):
            # If no history before, initialize one empty dictionary
            new_update_dict = {}
            # for var in var_list:
            #     try:
            #         new_update_dict[var.name()[0]] = 0.
            #     except:
            #         raise AttributeError("Elements in var_list should be AD variables! Or make your var_list 1D!")
            self.last_update = new_update_dict

        assert isinstance(self.last_update, dict), "last update should be a dictionary!"

        # new_update_dict = {}
        for var in var_list:
            try:
                grad = grad_dict[var.name()[0]]
                # Trivial numerical instability check
                if abs(grad) > 10**8:
                    warnings.warn("Gradient is too large: potential numerical instability")
                
                try: 
                    v_tm1 = self.last_update[var.name()[0]]
                except KeyError:
                    self.last_update[var.name()[0]] = 0.
                    v_tm1 = self.last_update[var.name()[0]]

                v_t = self.gamma * v_tm1 + self.lr * grad
                
                # update the variable value
                var.func_val -= v_t

                # update the last_update dictionary
                self.last_update[var.name()[0]] = v_t
            except:
                raise AttributeError("Var_list should be 1D, with AD instances as elements, which are variables in loss!")





        
