import boomdiff
from boomdiff import AD
import doctest
import pytest
import numpy as np


@pytest.fixture
def data():
    x = np.array([[1, 2, 3], [4, 5, 6]])
    return x

@pytest.fixture
def v1():
    v1 = AD(0.0, 'v1')
    return v1

@pytest.fixture 
def v2():
    v2 = AD(0.0, 'v2')
    return v2

# Test loss function capabilities
def test_rowsum():
    x = np.array([[1, 2, 3], [4, 5, 6]])
    v1 = AD(0.0, 'v1')
    v2 = AD(0.0, 'v2')
    v3 = AD(0.0, 'v3')
    f = boomdiff.loss_function._rowsums(x, [v1, v2, v3])
    assert f[0] == AD(0.0, {'v1': 1.0, 'v2': 2.0, 'v3':3.0})
    assert f[1] == AD(0.0, {'v1': 4.0, 'v2': 5.0, 'v3': 6.0})

# MSE
def test_mse_diffdim():
    x = np.array([[1,2], [3,4]])
    y = np.array([1,2,3])
    v1 = AD(1., 'v1')
    v2 = AD(1., 'v2')
    with pytest.raises(AssertionError):
        boomdiff.loss_function.linear_mse(x, y, [v1, v2])    

def test_mse_outputdim():
    x = np.array([[1,2], [3,4]])
    y = np.array([[1,2], [3,4]])
    v1 = AD(1., 'v1')
    v2 = AD(1., 'v2')
    with pytest.raises(AssertionError):
        boomdiff.loss_function.linear_mse(x, y, [v1, v2])   

# CROSS ENTROPY
def test_ce_diffdim():
    x = np.array([[1,2], [3,4]])
    y = np.array([1,1,0])
    v1 = AD(1., 'v1')
    v2 = AD(1., 'v2')
    with pytest.raises(ValueError):
        boomdiff.loss_function.logistic_cross_entropy(x, y, [v1, v2])    

def test_ce_outputdim():
    x = np.array([[1,2], [3,4]])
    y = np.array([[1,0], [1,1]])
    v1 = AD(1., 'v1')
    v2 = AD(1., 'v2')
    with pytest.raises(AssertionError):
        boomdiff.loss_function.logistic_cross_entropy(x, y, [v1, v2])   