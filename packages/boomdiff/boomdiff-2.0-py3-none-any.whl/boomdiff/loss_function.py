import numpy as np
from boomdiff.autodiff import AD

"""Defines a series of loss functions to be called in various use-case
methods"""


def _rowsums(data, var_list):
    """Helper method for creating rows of data as AD objects using a format
    where data is an n x m array (no outcome data provided) and var_list is a
    length m list or broadcastable
    
    Parameters
    ----------
    data: np.array
        should be a n x m numpy array representing n observations and m
        features (excluding outcome)
    var_list: list or np.array
        list or array of AD objects
    
    Returns
    -------
    length n array representing rows of data matrix as AD objects
    """
    return AD.sum(data * np.array(var_list).reshape(1,-1), axis=1)

def linear_mse(inputs, outputs, var_list):
    """Calculates mean squared error for AD objects. All objects passed to var_list
    must be instantiated AD objects. Highly preferable for data to be input as numpy
    array with observations as rows and features as columns.
    
    Parameters
    ----------
    inputs: np.array
        Input data. This will be the X matrix, without the outcome variables considered.
    outputs:
	Numpy array of output data. Should be ordered according to rows of input data
    var_list: list; AD object
        list of AD objects to be included in function
    outputs:
        index of outcome in data
    
    Examples
    --------
    >>> x = np.array([[2, 3], [5, 6]])
    >>> y = np.array([1, 4])
    >>> v1 = AD(0.0, 'v1')
    >>> v2 = AD(0.0, 'v2')
    >>> varlist = [v1, v2]
    >>> linear_mse(x, y, varlist)
    8.5 ({'v1': -22.0, 'v2': -27.0})
    """

    # Step 1: Convert data to array format and confirm it is 2-dimensional
    # If not, could be converted by np.reshape(n,p) to get to n x p matrix
    inputs = np.array(inputs)
    assert inputs.ndim == 2, 'data must be convertible to 2-D array!'        
	
    outputs = np.array(outputs)
    if outputs.ndim == 2:
        assert (outputs.shape[1] == 1) or (outputs.shape[0] == 1), 'Outputs cannot be multidimensional!'
    else:
        assert outputs.ndim == 1, 'Outputs cannot have more than 2 dimensions!'
 
    # Step 1A: Check that size of data are compatible
    outputs = outputs.reshape(-1)
    assert _rowsums(inputs, var_list).shape[0] == outputs.shape[0], 'Input and output must be of same dimension'
    
    # Step 3: Calculate loss function - _rowsums() method can be used to
    # make x, beta to x*beta step
    sse = AD.sum((outputs - _rowsums(inputs, var_list)) ** 2)
    # Note: Linear MSE could be calculated in one step
    return (1/len(outputs))*sse


def logistic_cross_entropy(inputs, outputs, var_list):
    """Calculates the binary cross-entropy between true_label and predictions
    
    Parameters
    ----------
    inputs: np.array
        Input data. This will be the X matrix, without the outcome variables considered.
    outputs:
	Numpy array of output data. Should be ordered according to rows of input data
    var_list: list; AD object
        list of AD objects to be included in function
    outputs:
        index of outcome in data
     
    Returns
    -------
    Binary cross-entropy between labels
    
    Examples
    --------
    >>> x = np.array([[2, 3], [5, 6]])
    >>> y = np.array([1,0])
    >>> v1 = AD(0.0, 'v1')
    >>> v2 = AD(0.0, 'v2')
    >>> varlist = [v1, v2]
    >>> logistic_cross_entropy(x, y, varlist)
    0.6931471805599453 ({'v1': 0.75, 'v2': 0.75})
    >>> assert type(logistic_cross_entropy(x, y, varlist)) == AD
    """

    # Step 1: Convert data to array format and confirm it is 2-dimensional
    # If not, could be converted by np.reshape(n,p) to get to n x p matrix
    inputs = np.array(inputs)
    assert inputs.ndim == 2, 'data must be convertible to 2-D array!'

    
    # Step 2A (optional): Validate data. Because this is a logistic regression
    # output, we check that all data is zero or one
    outputs = np.array(outputs)
    if outputs.ndim == 2:
        assert (outputs.shape[1] == 1) or (outputs.shape[0] == 1), 'Outputs cannot be multidimensional!'
    else:
        assert outputs.ndim == 1, 'Outputs cannot have more than 2 dimensions!'
    
    for x in outputs:
        assert x in [0, 1], 'All outcomes must be 0 or 1!'
    outputs = outputs.reshape(-1)
        
    # Step 3: Calculate loss function
    # Note: Because this is a logistic cross_entropy function,
    # we use AD.logisitc() to convert our linear row sums to probabilities
    pred_probs = AD.logistic(_rowsums(inputs, var_list))
    
    # Note: Factors are calculated separately to present information cleanly,
    # could be combined
    log_probs = AD.log(pred_probs)
    log_1_probs = AD.log(1 - pred_probs)
    mf = -(1/len(outputs))
    return mf*np.sum((outputs*log_probs) + (1 - outputs)*log_1_probs)

    
