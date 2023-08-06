# check out https://docs.pytest.org/en/stable/getting-started.html#getstarted
import boomdiff
from boomdiff import AD
import pytest
import numpy as np

#creating templates that will be used to test the functions
@pytest.fixture
def trig_cls():
    x = AD(np.pi/4, {'x1': 1.})
    return x

@pytest.fixture
def trig_var():
    x = np.pi/4
    return x

@pytest.fixture
def basic_cls():
    x = AD(2, {'x1': 1.})
    return x

@pytest.fixture
def basic_var():
    x = 0.5
    return x

@pytest.fixture
def less1_cls(): #less than 1 variables for inverse trig functions
    x = AD(0.25, {'x1': 1.})
    return x

@pytest.fixture
def less1_var():
    x = 0.25
    return x

#testing basic functions
def test_init(trig_cls):
    assert trig_cls.func_val == np.pi/4
    assert trig_cls.partial_dict['x1'] == 1
    assert len(trig_cls.partial_dict.keys()) == 1

def test_sin(trig_cls, trig_var):
    f1 = AD.sin(trig_cls)
    f2 = AD.sin(trig_var)

    assert f1.func_val == np.sin(np.pi/4)
    assert f1.partial_dict['x1'] == np.cos(np.pi/4)
    assert f2 == np.sin(np.pi/4)

def test_cos(trig_cls, trig_var):
    f1 = AD.cos(trig_cls)
    f2 = AD.cos(trig_var)

    assert f1.func_val == np.cos(np.pi/4)
    assert f1.partial_dict['x1'] == -np.sin(np.pi/4)
    assert f2 == np.cos(np.pi/4)

def test_tan(trig_cls, trig_var):
    f1 = AD.tan(trig_cls)
    f2 = AD.tan(trig_var)

    assert f1.func_val == np.tan(np.pi/4)
    assert f1.partial_dict['x1'] == 1/(np.cos(np.pi/4)**2)
    assert f2 == np.tan(np.pi/4)

def test_arcsin(less1_cls, less1_var):
    f1 = AD.arcsin(less1_cls)
    f2 = AD.arcsin(less1_var)

    assert f1.func_val == np.arcsin(0.25)
    assert f1.partial_dict['x1'] == 1 / np.sqrt(1 - 0.25**2)
    assert f2 == np.arcsin(0.25)

def test_arccos(less1_cls, less1_var):
    f1 = AD.arccos(less1_cls)
    f2 = AD.arccos(less1_var)

    assert f1.func_val == np.arccos(0.25)
    assert f1.partial_dict['x1'] == - 1 / np.sqrt(1 - 0.25**2)
    assert f2 == np.arccos(0.25)

def test_arctan(less1_cls, less1_var):
    f1 = AD.arctan(less1_cls)
    f2 = AD.arctan(less1_var)

    assert f1.func_val == np.arctan(0.25)
    assert f1.partial_dict['x1'] == 1 / (1 + 0.25**2)
    assert f2 == np.arctan(0.25)

def test_log(trig_cls, trig_var):
    f1 = AD.log(trig_cls)
    f2 = AD.log(trig_var)

    assert f1.func_val == np.log(np.pi/4)
    assert f1.partial_dict['x1'] == 1/(np.pi/4)
    assert f2 == np.log(np.pi/4)

def test_exp(basic_cls, basic_var):
    f1 = AD.exp(basic_cls)
    f2 = AD.exp(basic_var)

    assert f1.func_val == np.e**(2)
    assert f1.partial_dict['x1'] == np.e**(2)
    assert f2 == np.exp(0.5)

def test_ops(basic_cls, basic_var):
    assert (basic_cls + basic_var).func_val == 2.5
    assert (basic_var + basic_cls).func_val == 2.5
    assert (basic_cls + basic_cls).func_val == 4
    assert (basic_cls + basic_var).partial_dict['x1']  == 1
    assert (basic_var + basic_cls).partial_dict['x1']  == 1
    assert (basic_cls + basic_cls).partial_dict['x1']  == 2


    assert (basic_cls - basic_var).func_val == 1.5
    assert (basic_var - basic_cls).func_val == -1.5
    assert (basic_cls - basic_cls).func_val == 0
    assert (basic_cls - basic_var).partial_dict['x1']  == 1
    assert (basic_var - basic_cls).partial_dict['x1']  == -1
    assert (basic_cls - basic_cls).partial_dict['x1']  == 0

    assert (basic_cls * basic_var).func_val == 1
    assert (basic_var * basic_cls).func_val == 1
    assert (basic_cls * basic_cls).func_val == 4
    assert (basic_cls * basic_var).partial_dict['x1']  == 0.5
    assert (basic_var * basic_cls).partial_dict['x1']  == 0.5
    assert (basic_cls * basic_cls).partial_dict['x1']  == 4

    assert (basic_cls / basic_var).func_val == 4
    assert (basic_var / basic_cls).func_val == 0.25
    assert (basic_cls / basic_cls).func_val == 1
    assert (basic_cls / basic_var).partial_dict['x1']  == 2
    assert (basic_var / basic_cls).partial_dict['x1']  == -0.125
    assert (basic_cls / basic_cls).partial_dict['x1']  == 0

    assert (basic_cls**basic_var).func_val == 1.4142135623730951
    assert (basic_var**basic_cls).func_val == 0.25
    assert (basic_cls**basic_cls).func_val == 4
    assert (basic_cls**basic_var).partial_dict['x1']  == 0.3535533905932738
    assert (basic_var**basic_cls).partial_dict['x1']  == -0.17328679513998632
    assert (basic_cls**basic_cls).partial_dict['x1']  == 6.772588722239782
