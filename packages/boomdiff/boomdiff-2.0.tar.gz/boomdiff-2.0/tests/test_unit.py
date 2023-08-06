import boomdiff
from boomdiff import AD
import doctest
import pytest

## Test suite for boomdiff

# Test initalization of base class
def test_base():
    x = AD(1, {'x1':1})
    assert x.func_val == 1
    print(x.func_val)
    assert x.partial_dict['x1'] == 1
    assert len(x.partial_dict.keys()) == 1

def test_base_setstr():
    x = AD(1.0, 'x2')
    assert x == AD(1.0, {'x2': 1.})

def test_bast_nonstringname():
    with pytest.raises(ValueError):
        x = AD(3.0, 3)
    
def test_badbaseval():
    # Test initialize base class without float or integer type
    with pytest.raises(ValueError):
        x = AD('v')
        
def test_nonnum_dict_init():
    # Test values of passed dictionary are int or float
    with pytest.raises(ValueError):
        x = AD(3.6, {'x1': 'bad'})
        
def test_nondict_init():
    # Test that if der_dict passed, it is dictionary 
    with pytest.raises(ValueError):
        x = AD(1.5, 9.3)

def test_set_nonatt():
    # Test that set_params(att) must be one of 'func_val' or 'partial_dict'
    with pytest.raises(ValueError):
        x = AD(1.3)
        x.set_params('evaluation_point', 2)

def test_set_funcval():
    # If setting 'func_val', must be type float or int
    with pytest.raises(ValueError):
        x = AD(13.2)
        x.set_params('func_val', '2.3')

def test_set_dictionary():
    # If set 'partial_dict', must be dictionary
    with pytest.raises(ValueError):
        x = AD(13.2)
        x.set_params('partial_dict', 2)

def test_setparam_dictvals():
    # 'partial_dict' values must be integers or floats
    with pytest.raises(ValueError):
        x = AD(12)
        x.set_params('partial_dict', {'x1': '3'})
  
# Test equality/inequality operators
def test_equality():
    # Test equality of operations
    x = AD(12, 'x1')
    y = AD(12)
    assert x == y

def test_equality_fval():
    # Test equality of func_val
    x = AD(12, 'x1')
    z = AD(13)
    assert (x == z) == False

def test_equality_partial():
    # Test equality of partial dictionary
    x = AD(12, 'x1')
    y = AD(12, 'x2')
    assert (x == y) == False

def test_equality_obj():
    # test equality with non AD object
    x = AD(12, 'x1')
    assert (x == 12) == False
    
def test_inequality():
    # Test basic inequality
    x = AD(12, 'x1')
    y = AD(9)
    assert x != y

def test_inequality_rev():
    # Test reverse of inequality
    x = AD(12, 'x1')
    y = AD(12, 'x1')
    assert (x != y) == False    

def test_inequality_partial():
    # Testinequality of partial dictionary
    x = AD(12, 'x1')
    y = AD(12, 'x2')
    assert x != y

def test_inequality_obj():
    # test inequality compared to non-object
    x = AD(12, 'x1')
    assert x != 3
    
# Test evaluation methods
def test_name():
    x = AD(2.5, 'y')
    assert x.name() == ['y']

def test_funcval():
    x = AD(3.0)
    assert x.value() == 3.0

def test_ders():
    x = AD(3.0, 'x')
    y = AD(4.0, 'y')
    f = x + y
    assert f.ders() == {'x': 1.0, 'y': 1.0}

def test_evaluate():
    x = AD(4.0, 'x')
    y = AD(5., 'y')
    f = 2*x + 2*y
    assert f.evaluate() == (18.0, {'x': 2.0, 'y': 2.0})


#### MISC TESTS
def test_improper_logbase():
    x = AD(3)
    with pytest.raises(Exception):
        AD.log(x, base = AD(4))
        
def doctesting():
    doctest.testmod()

if __name__ == '__main__':
    test_evaluate()
