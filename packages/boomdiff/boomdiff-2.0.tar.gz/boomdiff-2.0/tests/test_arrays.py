import boomdiff
from boomdiff import AD
import pytest
import numpy as np

@pytest.fixture
def z(): #less than 1 variables for inverse trig functions
    z = AD(0.5, {'z1': 1.})
    return z

@pytest.fixture
def ar_x():
    x_array = np.array([1.5, 10])
    AD_x_array = AD.from_array(x_array,'x')
    return AD_x_array

@pytest.fixture
def ar_y():
    y_array = np.array([3, 5])
    AD_y_array = AD.from_array(y_array,'y')
    return AD_y_array

@pytest.fixture
def ar_pi():
    pi_array = np.array([np.pi/2, np.pi/4])
    AD_pi_array = AD.from_array(pi_array,'p')
    return AD_pi_array

@pytest.fixture
def ar_2d():
    w_array = np.array([[3.0,2.4],[1.5,3.3]])
    AD_w_array = AD.from_array(w_array, 'w')
    return AD_w_array

def test_errors():
    x_array = np.array([1.5, 10])
    with pytest.raises(AttributeError):
        AD.to_array(x_array)

def test_array_numpy_ops(ar_x):
    assert AD.sum(ar_x).func_val == 11.5
    assert AD.sum(ar_x).partial_dict['x_0'] == 1
    assert AD.sum(ar_x).partial_dict['x_1'] == 1

    assert AD.mean(ar_x).func_val == 5.75
    assert AD.mean(ar_x).partial_dict['x_0'] == 0.5
    assert AD.mean(ar_x).partial_dict['x_1'] == 0.5

    assert AD.dot(ar_x, ar_x).func_val == 102.25
    assert AD.dot(ar_x, ar_x).partial_dict['x_0'] == 3
    assert AD.dot(ar_x, ar_x).partial_dict['x_1'] == 20

def test_array_ops_2arrays(ar_x, ar_y):
    assert (ar_x + ar_y)[0].func_val == 4.5
    assert (ar_x + ar_y)[1].func_val == 15
    assert (ar_x + ar_y)[0].partial_dict['x_0'] == 1
    assert (ar_x + ar_y)[0].partial_dict['y_0'] == 1
    assert (ar_x + ar_y)[1].partial_dict['x_1'] == 1
    assert (ar_x + ar_y)[1].partial_dict['y_1'] == 1

    assert (ar_x - ar_y)[0].func_val == -1.5
    assert (ar_x * ar_y)[0].func_val == 4.5
    assert (ar_y / ar_x)[0].func_val == 2

    assert (ar_x - ar_y)[1].partial_dict['x_1'] == 1
    assert (ar_x - ar_y)[1].partial_dict['y_1'] == -1

    assert (ar_x * ar_y)[1].partial_dict['x_1'] == 5
    assert (ar_x * ar_y)[1].partial_dict['y_1'] == 10

    assert (ar_y / ar_x)[1].partial_dict['x_1'] == -0.05
    assert (ar_y / ar_x)[1].partial_dict['y_1'] == 0.1

    assert (AD(1, 'x') + AD.from_array(np.array([1,2,3,4])))[1].func_val == 3
    assert (AD(1, 'x') - AD.from_array(np.array([1,2,3,4])))[1].func_val == -1
    assert (AD(1, 'x') * AD.from_array(np.array([1,2,3,4])))[1].func_val == 2
    assert (AD(1, 'x') / AD.from_array(np.array([1,2,3,4])))[1].func_val == 0.5
    assert (AD(10, 'x') ** AD.from_array(np.array([1,2,3,4])))[1].func_val == 100

def test_array_ops_numpy_ar_list(ar_x):
    ar = np.array([-1, 10])
    lst = [-1, 10]

    assert (ar_x + ar)[0].func_val == 0.5
    assert (ar_x + ar)[1].func_val == 20
    assert (ar_x + lst)[0].func_val == 0.5
    assert (ar_x + lst)[1].func_val == 20
    assert (ar_x + ar)[0].partial_dict['x_0'] == 1

    assert (ar_x - ar)[0].func_val == 2.5
    assert (ar_x - ar)[1].func_val == 0
    assert (ar_x - lst)[0].func_val == 2.5
    assert (ar_x - lst)[1].func_val == 0
    assert (ar_x - ar)[0].partial_dict['x_0'] == 1

    assert (ar_x * ar)[0].func_val == -1.5
    assert (ar_x * ar)[1].func_val == 100
    assert (ar_x * lst)[0].func_val == -1.5
    assert (ar_x * lst)[1].func_val == 100
    assert (ar_x * ar)[0].partial_dict['x_0'] == -1

    assert (ar_x / ar)[0].func_val == -1.5
    assert (ar_x / ar)[1].func_val == 1
    assert (ar_x / lst)[0].func_val == -1.5
    assert (ar_x / lst)[1].func_val == 1
    assert (ar_x / ar)[0].partial_dict['x_0'] == -1

def test_trig(ar_pi):
    assert  [AD.sin(ar_pi)[0].func_val, np.round(AD.sin(ar_pi)[1].func_val, 7)] == [1.0, np.round(0.7071067811865476, 7)]
    assert np.round(AD.sin(ar_pi)[0].partial_dict['p_0'], 7) ==  np.round(6.123233995736766e-17, 7)

    assert  [np.round(AD.cos(ar_pi)[0].func_val, 7), np.round(AD.cos(ar_pi)[1].func_val, 7)] == [np.round(6.123233995736766e-17, 7), np.round(0.7071067811865476, 7)]
    assert AD.cos(ar_pi)[0].partial_dict['p_0'] ==  -1.0

    assert  np.round(AD.tan(ar_pi)[1].func_val, 7) ==  np.round(0.9999999999999999, 7)
    assert np.round(AD.tan(ar_pi)[1].partial_dict['p_1'], 7) == np.round(1.9999999999999996, 7)

def test_invtrig():
    x = np.array([0.25, 0.5])
    inv_ar = AD.from_array(x,'p')

    assert  [np.round(AD.arcsin(inv_ar)[0].func_val, 7), np.round(AD.arcsin(inv_ar)[1].func_val, 7)] == [np.round(0.25268025514207865, 7), np.round(0.5235987755982989, 7)]
    assert np.round(AD.arcsin(inv_ar)[0].partial_dict['p_0'], 7) ==  np.round(1.0327955589886444, 7)

    assert  [np.round(AD.arccos(inv_ar)[0].func_val, 7), np.round(AD.arccos(inv_ar)[1].func_val, 7)] == [np.round(1.318116071652818, 7), np.round(1.0471975511965979, 7)]
    assert np.round(AD.arccos(inv_ar)[0].partial_dict['p_0'], 7) ==  np.round(-1.0327955589886444, 7)

    assert  np.round(AD.arctan(inv_ar)[1].func_val, 7) ==  np.round(0.4636476090008061, 7)
    assert AD.arctan(inv_ar)[1].partial_dict['p_1'] == 0.8

def test_misc_funcs():
    ar_f = AD.from_array([1, 4], 'f')

    assert AD.sqrt(ar_f)[1].func_val == 2
    assert AD.sqrt(ar_f)[1].partial_dict['f_1'] == 0.25

    assert AD.log(ar_f)[0].func_val == 0
    assert AD.log(ar_f)[1].partial_dict['f_1'] == 0.25

    assert np.round(AD.sinh(ar_f)[0].func_val, 7) == np.round(1.1752011936438014, 7)
    assert np.round(AD.sinh(ar_f)[1].partial_dict['f_1'], 7) == np.round(27.308232836016487, 7)


    assert np.round(AD.cosh(ar_f)[0].func_val, 7) == np.round(1.5430806348152437, 7)
    assert np.round(AD.cosh(ar_f)[1].partial_dict['f_1'], 7) == np.round(27.289917197127753, 7)
    assert np.round(AD.cosh(1), 7) == np.round(1.5430806348152437, 7)

    assert np.round(AD.tanh(ar_f)[0].func_val, 7) == np.round(0.7615941559557649, 7)
    assert np.round(AD.tanh(ar_f)[1].partial_dict['f_1'], 7) ==  np.round(0.001340950683025897, 7)
