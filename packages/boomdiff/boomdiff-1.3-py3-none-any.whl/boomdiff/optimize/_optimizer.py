import numpy as np

import matplotlib.pyplot as plt

from boomdiff.autodiff import AD


class Optimizer():
    """Base class for all optimizers.

    You should not use this class directly, but instead instantiate one of its
    subclasses such as `GD`, `BFGS`, etc.

    Contains step and minimize methods, while _apply_gradient is implemented by
    separately for different algorithms.

    Check subclasses (such as gradient_descent) for usage examples

    Learning rate defines the size of the iteration steps. Default value is 0.1
    but it can be increased for speed up or decreased for more accurate results.
    """

    def __init__(self, learning_rate=0.1):
        assert isinstance(learning_rate, (float,int, np.number)), "learning_rate should be int or float!"
        self.lr = learning_rate

        self.iterations = 0 # Record iteration number
        self.loss_track = [] #loss function value for each iteration

    def step(self, loss, var_list, learning_rate=None, record=False):
        """update the variables for one step, to minimize the loss value

        Parameters
        ----------
        loss: callable
            objective function, takes no arguments and output an AD instance

        var_list: 1D list/array of AD instances (variables)
            the variable lists that you want to update. It can be part of the variables in loss callable.

        learning_rate: int or float
            You can also specify the learning rate here

        record: Bool, default False
            Whether you want to append the current loss to class attribute loss_track. 

        Returns
        -------
        Self, optimizer instance. It will directly update variables in var_list

        """

        if isinstance(learning_rate, (int, float, np.number)):
            self.lr = learning_rate
        elif learning_rate is None:
            pass
        else:
            raise Exception("learning_rate should be int or float!")

        assert callable(loss), "loss should be a callable function!"
        assert isinstance(var_list, (np.ndarray,list)), "var_list should be a variable list or array!"
        # Change to duck-typing check in each subclass, for performance consideration
        #for var in var_list:
        #    assert isinstance(var, AD), "Elements in var_list should be AD variables! Or make your var_list 1D!"

        current_loss = loss()
        assert isinstance(current_loss, AD), "The output of loss callable should be an AD instance!"

        #add loss function value before optimization
        if (self.iterations == 0) and (record == True):
            self.loss_track.append(loss().func_val)

        # Apply the gradient to update variables.
        # This method should be implemeneted in each algorithm subclass
        grad_dict = current_loss.partial_dict
        #print("grad_dict: ", grad_dict)
        self._apply_gradient(loss, var_list, grad_dict)

        #print("current loss: ", loss())
        #print("current loss().func_val: ", loss().func_val)
        # Record the iteration number
        self.iterations += 1

        #record loss function value for this iteration
        if record == True:
            self.loss_track.append(loss().func_val)

    def minimize(self, loss, var_list, steps=100, learning_rates=None, record=False):
        """update multiple steps with user-specified learning_rate series

        Parameters
        ----------
        loss: callable
            objective function, takes no arguments and output an AD instance.

        var_list: 1D list/array of AD instances (variables)
            the variable lists that you want to update. It can be part of the variables in loss callable.

        steps: positive int
            number of steps you want to update

        learning_rates: int, float, list of values, 1D numpy array of values
            use-specifed learning_rates, can be a list with length equal to step numbers

        record: Bool, default False
            Whether you want to append the current loss to class attribute loss_track. 

        Returns
        -------
        Self, Optimizer instance. It will directly update variables in var_list
        """
        assert (isinstance(steps, int)) & (steps > 0), "Steps should be positive int!"

        if isinstance(learning_rates, np.ndarray):
            assert (learning_rates.ndim == 1) & (len(learning_rates) == steps), "learning_rates should be 1D list/array with length equal to steps, or single value!"
            for i in range(steps):
               self.step(loss, var_list, learning_rates[i], record)

        elif isinstance(learning_rates, list):
            assert (len(learning_rates) == steps), "learning_rates should be 1D list/array with length equal to steps, or single value!"
            for i in range(steps):
               self.step(loss, var_list, learning_rates[i], record)

        else:
            for i in range(steps):
               self.step(loss, var_list, learning_rates, record)


    def _apply_gradient(self, loss, var_list, grad_dict):
        """
        Apply the gradient to update variables.
        This method should be implemeneted in each algorithm subclass
        """
        raise NotImplementedError("Please use subclass with specific algorithms, like boomdiff.optimize.GD")

    def plot_loss_func(self):
        '''
        Helper method, quickily plot the loss function value vs iteration step #
        '''
        plt.plot(np.arange(self.iterations + 1), self.loss_track)
        plt.xlabel("itertion #")
        plt.ylabel("loss function value")
        plt.show()
