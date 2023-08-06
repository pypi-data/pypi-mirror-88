"""
Interface for Adaptive Moment Estimation (Adam) optimizer
"""

__all__ = ['Adam']

import warnings

import numpy as np

from boomdiff.autodiff import AD
from ._optimizer import Optimizer

class Adam(Optimizer):
    """
    Adaptive Moment Estimation (Adam) optimization algorithm, computes adaptive learning rates for each parameter.

    Usage:
    >>> a = AD(2, 'a')
    >>> loss = lambda: a**2
    >>> opt_adam = Adam(learning_rate=0.1)
    >>> opt_adam.minimize(loss, [a], steps=10)
    >>> print(a.round(2))
    0.35 ({'a': 1.0})
    >>> x1 = AD(5, 'x1')
    >>> x2 = AD(7, 'x2')
    >>> loss2 = lambda: x1**2 + x2**2 + (x1-x2)**2
    >>> opt_adam.init(learning_rate=0.1)
    >>> opt_adam.minimize(loss2, [x1, x2], steps=300)
    >>> print(x1.round(3), x2.round(3))
    0.0 ({'x1': 1.0}) 0.0 ({'x2': 1.0})
    """

    def __init__(self, learning_rate=0.001, betas=(0.9, 0.999), eps=1e-08):
        """
        Parameters
        ----------
        learning_rate: int or float, default 1e-03

        betas: tuple[float, float], default (0.9, 0.999)
            coefficients used for computing running averages of gradient and its square

        eps: float, default 1e-08
            term added to the denominator to improve numerical stability
        """
        super(Adam, self).__init__(learning_rate)
        
        assert isinstance(betas, tuple) and (len(betas) == 2), "Betas should be a tuple with 2 float elements!"
        for beta in betas:
            assert isinstance(beta, float), "Betas should be a tuple with 2 float elements!"
        self.beta1 = betas[0]
        self.beta2 = betas[1]

        assert (isinstance(eps, float)) and (eps < 1e-05), "epsilon should be a small float!"
        self.eps = eps

    def init(self, learning_rate=0.001, betas=(0.9, 0.999), eps=1e-08):
        """
        initialize the optimizer, if u want to drop the history track and use eleswhere
        """
        # Delete the history track attribute
        if hasattr(self,'_mt'): delattr(self, '_mt') 
        if hasattr(self,'_vt'): delattr(self, '_vt') 

        # Reinitialize the hyperparameters if set
        self.__init__(learning_rate, betas, eps)

    def _apply_gradient(self, loss, var_list, grad_dict):
        """
        Computes adaptive learning rates for each parameter for each iteration:
        
        1. compute the decaying averages of past and past squared gradients
        m_t = beta1 * m_{t-1} + (1-beta1) * grad
        v_t = beta2 * v_{t-1} + (1-beta2) * grad**2
        
        2. compute bias-corrected first and second moment estimates
        m_hat_t = m_t / (1 - beta1)
        v_hat_t = v_t / (1 - beta2)

        3. update the parameters
        theta_{t+1} = theta_t - lr * m_hat_t / (sqrt(v_hat_t) + eps)
        """
        if not hasattr(self,'_mt'):
            # If no first moment history before, initialize one
            new_mt_dict = {}
            # for var in var_list:
            #     try:
            #         new_mt_dict[var.name()[0]] = 0.
            #     except:
            #         raise AttributeError("Elements in var_list should be AD variables! Or make your var_list 1D!")
            self._mt = new_mt_dict

        if not hasattr(self,'_vt'):
            # If no second moment history before, initialize one
            new_vt_dict = {}
            # for var in var_list:
            #     try:
            #         new_vt_dict[var.name()[0]] = 0.
            #     except:
            #         raise AttributeError("Elements in var_list should be AD variables! Or make your var_list 1D!")
            self._vt = new_vt_dict

        assert isinstance(self._mt, dict), "_mt attribute should be a dictionary!"
        assert isinstance(self._vt, dict), "_vt attribute should be a dictionary!"

        # new_mt_dict = {}
        # new_vt_dict = {}
        for var in var_list:
            try:
                grad = grad_dict[var.name()[0]]
                # Trivial numerical instability check
                if abs(grad) > 10**8:
                    warnings.warn("Gradient is too large: potential numerical instability")

                try:
                    # Step1: compute the decaying averages of past and past squared gradients
                    new_mt = self.beta1 * self._mt[var.name()[0]] + (1-self.beta1) * grad
                    new_vt = self.beta2 * self._vt[var.name()[0]] + (1-self.beta2) * grad**2
                except KeyError:
                    self._mt[var.name()[0]] = 0.
                    self._vt[var.name()[0]] = 0.
                    new_mt = self.beta1 * self._mt[var.name()[0]] + (1-self.beta1) * grad
                    new_vt = self.beta2 * self._vt[var.name()[0]] + (1-self.beta2) * grad**2

                # Step2: compute bias-corrected first and second moment estimates
                new_m_hat = new_mt / (1-self.beta1)
                new_v_hat = new_vt / (1-self.beta2)

                # Step3: update the variable
                var.func_val -= self.lr * new_m_hat / (np.sqrt(new_v_hat) + self.eps)

                # Store the new mt, vt
                self._mt[var.name()[0]] = new_mt
                self._vt[var.name()[0]] = new_vt
            except:
                raise AttributeError("Var_list should be 1D, with AD instances as elements, which are variables in loss!")
                
        # self._mt = new_mt_dict
        # self._vt = new_vt_dict












