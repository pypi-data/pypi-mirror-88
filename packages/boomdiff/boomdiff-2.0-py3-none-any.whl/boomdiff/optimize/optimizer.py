import numpy as np
from boomdiff.autodiff import AD


class Optimizer():
    """Base class for all optimizers.

    You should not use this class directly, but instead instantiate one of its
    subclasses such as `boomdiff.optimize.SGD`, `boomdiff.optimize.BFGS`, etc.


    Example:
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

    def __init__(self, learning_rate=0.1):
        assert isinstance(learning_rate, (float,int)), "learning_rate should be int or float!"
        self.lr = learning_rate
        # Record iteration number 
        self.iterations = 0 


    def step(self, loss, var_list, learning_rate=None):
        """update the variables for one step, to minimize the loss value

        Parameters
        ----------
        loss: callable
            objective function, takes no arguments and output an AD instance

        var_list: list of AD instances (variables)
            the variable lists that you want to update. It can be part of the variables in loss callable.

        learning_rate: int or float
            You can also specify the learning rate here

        Returns
        -------
        None. It will directly update variables in var_list 

        Examples
        --------
        None
        """
        if isinstance(learning_rate, (int, float)):
            self.lr = learning_rate
        elif learning_rate is None:
            pass
        else:
            raise Exception("learning_rate should be int or float!")

        assert callable(loss), "loss should be a callable function!"
        assert isinstance(var_list), "var_list should be a variable list!"
        for var in var_list:
            assert isinstance(var, AD), "Elements in var_list should be AD variables!"

        current_loss = loss()
        assert isinstance(current_loss, AD), "The output of loss callable should be an AD instance!"

        # Apply the gradient to update variables. 
        # This method should be implemeneted in each algorithm subclass
        grad_dict = current_loss.partial_dict
        self._apply_gradient(loss, var_list, grad_dict)

        # Record the iteration number
        self.iterations += 1

    def minimize(self, loss, var_list, steps=100, learning_rates=None):
        """update multiple steps with user-specified learning_rate series

        Parameters
        ----------
        loss: callable
            objective function, takes no arguments and output an AD instance.

        var_list: list of AD instances (variables)
            the variable lists that you want to update. It can be part of the variables in loss callable.

        steps: positive int
            number of steps you want to update

        learning_rates: int, float, list of values, 1D numpy array of values
            use-specifed learning_rates, can be a list with length equal to step numbers

        Returns
        -------
        None. It will directly update variables in var_list

        Examples
        --------
        ```python
        >>> opt.miminize(loss, var_list[var1, var2], learning_rates=np.linspace(0.1,0.01,100), steps=100)
        ```
        """
        assert (isinstance(steps, int)) & (steps > 0), "Steps should be positive int!"

        if isinstance(learning_rates, np.ndarray):
            assert (learning_rates.ndim == 1) & (len(learning_rates) == steps), "learning_rates should be 1D list/array with length equal to steps, or single value!"
            for i in range(steps):
               self.step(loss, var_list, learning_rates[i])

        elif isinstance(learning_rates, list):
            assert (len(learning_rates) == steps), "learning_rates should be 1D list/array with length equal to steps, or single value!"
            for i in range(steps):
               self.step(loss, var_list, learning_rates[i])

        else:
            for i in range(steps):
               self.step(loss, var_list, learning_rates)


    def _apply_gradient(self, loss, var_list, grad_dict):
        """
        Apply the gradient to update variables.
        This method should be implemeneted in each algorithm subclass
        """
        raise NotImplementedError("Please use subclass with specific algorithms, like boomdiff.optimize.SGD")


















