import boomdiff
from boomdiff import AD
import doctest
import pytest
import numpy as np

@pytest.fixture
def var1():
    var1 = AD(100, {'var1': 1})
    return var1

@pytest.fixture
def var2():
    var2 = AD(1, {'var2': 1})
    return var2

#cover optimizer exceptions
def test_optim_exc(var1, var2):
    opt = boomdiff.optimize._gradient_descent.GD(learning_rate=0.1)
    loss = lambda: var1**2 + var2**2
    opt.step(loss, var_list=[var1, var2], learning_rate= 0.2, record=True)
    assert var1 == AD(60, {'var1': 1})
    assert var2 == AD(0.6, {'var2': 1})

    with pytest.raises(Exception):
        opt.step(loss, var_list=[var1, var2], learning_rate= 'a')

def test_optim_lists(var1, var2):
    opt = boomdiff.optimize._gradient_descent.GD(learning_rate=0.1)
    loss = lambda: var1**2 + var2**2
    opt.minimize(loss, var_list=[var1, var2], steps=2, learning_rates= [0.2, 0.4], record=False)
    assert var1 == AD(12.0, {'var1': 1})
    assert var2 == AD(0.12, {'var2': 1})



def test_optim_array(var1, var2):
    opt = boomdiff.optimize._gradient_descent.GD(learning_rate=0.1)
    loss = lambda: var1**2 + var2**2
    opt.minimize(loss, var_list=[var1, var2], steps=2, learning_rates= np.array([0.2, 0.4]), record=False)

    assert var1 == AD(12.0, {'var1': 1})
    assert var2 == AD(0.12, {'var2': 1})

def test_warnings(var1, var2):
    loss = lambda: -var1**2 - var2**2

    opt = boomdiff.optimize.GD(learning_rate=0.1)
    with pytest.warns(UserWarning):
        opt.minimize(loss, var_list=[var1, var2])

    opt = boomdiff.optimize.Adam(learning_rate=0.1)
    with pytest.warns(UserWarning):
        opt.minimize(loss, var_list=[var1, var2])

    opt = boomdiff.optimize.Momentum(learning_rate=0.1)
    with pytest.warns(UserWarning):
        opt.minimize(loss, var_list=[var1, var2])
