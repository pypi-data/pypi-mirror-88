import numpy as np
import itertools

class AD():

    def __init__(self, eval_pt, der_dict={'x1':1}):
        """Initializes class structure
        Parameters
        ----------
        eval_pt : float
            Value of the current function/variable
        der_dict : dict
            derivative value dictionary of all variables
        Returns
        -------
        None.
        Examples
        --------
        >>> x1 = AD(3.6, {'x1':1})
        >>> x1.func_val
        3.6
        >>> x1.partial_dict
        {'x1': 1}
        """
        # Set function value if int or float; else raise error
        if isinstance(eval_pt, (int, float, np.number)):
            self.func_val = eval_pt
        else:
            raise ValueError('All valuess should be real float or integer numbers!')

        # Set partial derivative dictionary
        # Will assume form of x_1, ..., x_n
        if not isinstance(der_dict, (dict, str)):
            raise ValueError('der_dict must be type dict or str!')
        try:
            for key, val in der_dict.items():
                assert isinstance(der_dict[key], (int, float, np.number))
            self.partial_dict = der_dict
        except(AttributeError):
            # If string, set name and default seed vector (non-str example
            # already handled above)
            self.partial_dict = {der_dict: 1.}
        except:
            raise ValueError('All derivatives must be type int or float, to make the expression real and valid!')

    @staticmethod
    def from_array(array, prefix='x'):
        """
        Convert all elements in a numpy array to AD instances, after that we got an numpy array whose elements are all AD instances

        Parameters
        ----------
        array: numpy array or list, only support 1D or 2D at these moment.
            But this can be easily reshaped afterwise
            All elements should be float or int value.
            Those value will be kept as func_val in new AD instances

        prefix: string
            Used for name in the AD instances' partial_dict.
            Elements on ith row, jth column will have the name prefix_i_j

        Examples
        --------
        >>> x_array = np.array([1.5,8.4])
        >>> AD_x_array = AD.from_array(x_array,'x')
        >>> print(AD_x_array)
        [1.5 ({'x_0': 1.0}) 8.4 ({'x_1': 1.0})]
        >>> w_array = np.array([[3.0,2.4],[1.5,3.3]])
        >>> AD_w_array = AD.from_array(w_array, 'w')
        >>> print(AD_w_array)
        [[3.0 ({'w_0_0': 1.0}) 2.4 ({'w_0_1': 1.0})]
         [1.5 ({'w_1_0': 1.0}) 3.3 ({'w_1_1': 1.0})]]
        >>> X = np.random.normal(size=[10,2])
        >>> print(np.dot(X, AD_w_array).shape)
        (10, 2)

        """
        assert isinstance(array, (list, np.ndarray)), "array should be a numpy array or list!"
        assert isinstance(prefix, str), "prefix should be a string!"
        array_arr = np.array(array)

        assert array_arr.ndim <= 2, "array should not be more than 2D!"


        AD_array = np.zeros(array_arr.shape, dtype=AD)

        if array_arr.ndim == 1:
            for i in range(array_arr.shape[0]):
                AD_array[i] = AD(array_arr[i], prefix+f"_{i}")

        if array_arr.ndim == 2:
            for i in range(array_arr.shape[0]):
                for j in range(array_arr.shape[1]):
                    AD_array[i,j] = AD(array_arr[i,j], prefix+f"_{i}_{j}")

        return AD_array

    @staticmethod
    def to_array(AD_array):
        """
        Convert all AD instance elementd in an AD numpy array into its function values

        Examples:
        >>> x_array = np.array([1.5,8.4])
        >>> AD_x_array = AD.from_array(x_array,'x')
        >>> print(AD_x_array)
        [1.5 ({'x_0': 1.0}) 8.4 ({'x_1': 1.0})]
        >>> print(AD.to_array(AD_x_array))
        [1.5 8.4]
        """
        assert isinstance(AD_array, (list, np.ndarray)), "array should be a numpy array or list!"
        AD_array_arr = np.array(AD_array)

        value_array = np.zeros(AD_array_arr.shape, dtype=float)
        try:
            for idx, x in np.ndenumerate(AD_array_arr):
                value_array[idx] = x.func_val
            return value_array
        except:
            raise AttributeError("All elements in AD_array should be AD instances!")

    def name(self):
        """Return the varaiable name string list of the instance
        Convinient for optimize use"""
        return list(self.partial_dict.keys())

    def value(self):
        """Return the function value of the AD object"""
        return self.func_val

    def ders(self):
        """Return the partial derivative dictionary; equivalent to
        x.partial_dict"""
        return self.partial_dict

    def evaluate(self):
        """Returns function value and partial derivative dictionary
        as separate objects. Returned in order func_val, partial_dict"""
        return self.func_val, self.partial_dict

    def round(self, decimal_number=2, decimal_number_optional=None):
        """Return a new AD instance with the func_val and value in partial_dict rounded to
        a given number of decimals. It will not overwrite the self instance
        Parameters
        ----------
        decimal_number: Int, non-negative, default to be 2
            Number of decimals you want to round to.
            If decimal_number_optional is not given,
            It will apply to both func_val and value in partial_dict;
            Or it will only apply to func_val

        decimal_number_optional: None, Non-negative int
            Number of decimals you want to round value in partial_dict to.
            If not given, decimal_number will apply to both
            func_val and value in partial_dict.

        Returns
        -------
        A new AD instance with rounded value

        Examples
        --------
        >>> a = AD(1.45789,{'a': 3.4564})
        >>> a.round()
        1.46 ({'a': 3.46})
        >>> a.round(3)
        1.458 ({'a': 3.456})
        >>> a.round(1,2)
        1.5 ({'a': 3.46})
        """
        assert isinstance(decimal_number, int) and (decimal_number >= 0), "decimal_number should be non-negative integer!"
        if decimal_number_optional is None:
            decimal_number_optional = decimal_number
        else:
            assert isinstance(decimal_number_optional, int) and (decimal_number_optional >= 0), "decimal_number_optional should be non-negative integer!"

        new_der_dict = {}
        for key, value in self.partial_dict.items():
            new_der_dict[key] = np.round(value, decimal_number_optional)
        return AD(np.round(self.func_val, decimal_number), new_der_dict)

    def set_params(self, att, val):
        """Set parameters for class; to be used in selective cases only
        Parameters
        ----------
        att: string
            Must be passed as a string. One of func_val or partial_dict.
        val: float, int, dictionary
            If att == 'func_val', must be int or float. Else must be dictionary.
        Returns
        -------
        None

        Examples
        --------
        >>> x = AD(1)
        >>> x.set_params('func_val', 3.4)
        >>> x.set_params('partial_dict', {'x1': 2})
        >>> print(x.func_val, x.partial_dict)
        3.4 {'x1': 2}
        """
        if att == 'func_val':
            # Implement same check as constructor
            if not isinstance(val, (float, int, np.number)):
                raise ValueError("val must be type float or int")
            self.func_val = val
        elif att == 'partial_dict':
            if not isinstance(val, dict):
                raise ValueError("If att='partial_dict', val must be type dictionary")
            # Check that all values of passed dictionary are integers or floats
            try:
                for k, v in val.items():
                    assert isinstance(val[k], (int, float, np.number))
                self.partial_dict = val
            except:
                raise ValueError('All values of partial_dict must be int or float')
        else:
            raise ValueError("att must be either 'func_val' or 'partial_dict'")

    def __repr__(self):
        return f'{self.func_val} ({self.partial_dict})'

    # Define equality and inequality messages
    def __eq__(self, other):
        """AD objects must have same function value and partial derivative
        dictionary to be considered equal
        """
        if isinstance(other, AD):
            return (self.func_val == other.func_val) and (self.partial_dict == other.partial_dict)
        else:
            return False

    def __ne__(self, other):
        """AD objects are never equal to non-AD objects; if other AD object,
        will not be equal if either function value or partial derivatives are not equal
        """
        if isinstance(other, AD):
            return (self.func_val != other.func_val) or (self.partial_dict != other.partial_dict)
        else:
            return True

    def __add__(self, other):
        """Overload addition operation '+'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be added from self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(3.6, {'x1': 1})
        >>> x2 = AD(5.2, {'x2': 1.5})
        >>> f1 = x1 + x2
        >>> print(f1.func_val, f1.partial_dict)
        8.8 {'x1': 1, 'x2': 1.5}
        >>> f2 = f1 + x1
        >>> print(f2.func_val, f2.partial_dict)
        12.4 {'x1': 2, 'x2': 1.5}
        """
        if isinstance(other, (np.ndarray,list)):
            return np.array(self) + np.array(other)

        try:
            # First try as other is an AD class instance
            # Combine the partial_dict of self and other, for common keys, add the value; else, append the dictionary
            new_der_dict = {}
            for k in itertools.chain(self.partial_dict.keys(), other.partial_dict.keys()):
                new_der_dict[k] = self.partial_dict.get(k,0) + other.partial_dict.get(k,0)
            return AD(self.func_val+other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            return AD(self.func_val+other, self.partial_dict)

    def __radd__(self, other):
        """Overload to make sure commutativity of addition '+'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be subtracted on the left, from self.
            Can be a AD class instance, which will update function value
            and partial derivative dictionary; Or a constant,
            which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(3.6, {'x1': 1})
        >>> f1 = 10 + x1
        >>> print(f1.func_val, f1.partial_dict)
        13.6 {'x1': 1}
        >>> f0 = AD(3.6, {'x1': 1, 'x2': 4})
        >>> f1 = 10 + f0
        >>> print(f1.func_val, f1.partial_dict)
        13.6 {'x1': 1, 'x2': 4}
        """
        assert isinstance(other,(int, float, np.number)), "All values should be real float or int values!"
        # treat as a constant
        # just return the partial dictionary of the self instance
        new_der_dict = dict(self.partial_dict)
        return AD(other+self.func_val, new_der_dict)

    def __sub__(self, other):
        """Overload subtraction operation '-'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be subtracted from self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(3.6, {'x1': 1})
        >>> f1 = x1 - 10
        >>> print(f1.func_val, f1.partial_dict)
        -6.4 {'x1': 1}
        >>> x2 = AD(2.0, {'x2': 3.4})
        >>> f2 = x1 - x2
        >>> print(f2.func_val, f2.partial_dict)
        1.6 {'x1': 1, 'x2': -3.4}
        """
        if isinstance(other, (np.ndarray,list)):
            return np.array(self) - np.array(other)
        try:
            # First try as other is an AD class instance
            # Combine the partial_dict of self and other, for common keys, subtract the value; else, append the dictionary
            new_der_dict = {}
            for k in itertools.chain(self.partial_dict.keys(), other.partial_dict.keys()):
                new_der_dict[k] = self.partial_dict.get(k,0) - other.partial_dict.get(k,0)
            return AD(self.func_val-other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            return AD(self.func_val-other, self.partial_dict)

    def __rsub__(self, other):
        """Overload to make sure commutativity of subtraction '-'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be subtracted on the left, from self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(3.6, {'x1': 1})
        >>> f1 = 10 - x1
        >>> print(f1.func_val, f1.partial_dict)
        6.4 {'x1': -1}
        >>> f0 = AD(3.6, {'x1': 1, 'x2': 3})
        >>> f1 = 10 - f0
        >>> print(f1.func_val, f1.partial_dict)
        6.4 {'x1': -1, 'x2': -3}
        """
        assert isinstance(other,(int, float, np.number)), "All values should be real float or int values!"
        # If other is not an AD class instance, treat as a constant
        new_der_dict = {}
        for key, value in self.partial_dict.items():
            new_der_dict[key] = -value
        return AD(other-self.func_val, new_der_dict)

    def __mul__(self, other):
        """Overload multiplication operation '*'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be multiplied to self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(1, {'x1': 1})
        >>> f1 = x1*10.0
        >>> print(f1.func_val, f1.partial_dict)
        10.0 {'x1': 10.0}
        >>> x2 = x1*3.4 - 1.4
        >>> print(x2.func_val, x2.partial_dict)
        2.0 {'x1': 3.4}
        >>> f2 = f1 * x2
        >>> print(f2.func_val, f2.partial_dict)
        20.0 {'x1': 54.0}
        >>> a = AD(2, {'a': 1})
        >>> b = AD(4, {'b': 1})
        >>> f3 = a*b
        >>> print(f3.func_val, f3.partial_dict)
        8 {'a': 4, 'b': 2}
        >>> f4 = f3*b
        >>> print(f4.func_val, f4.partial_dict)
        32 {'a': 16, 'b': 16}
        """
        if isinstance(other, (np.ndarray, list)):
            return np.array(self) * np.array(other)

        try:
            # First try as other is an AD class instance
            new_der_dict = {}
            for k in itertools.chain(self.partial_dict.keys(), other.partial_dict.keys()):
                new_der_dict[k] = self.partial_dict.get(k,0)*other.func_val + other.partial_dict.get(k,0)*self.func_val
            #print(new_der_dict)
            #print(self.partial_dict)
            return AD(self.func_val*other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            new_der_dict = {}
            for key, value in self.partial_dict.items():
                new_der_dict[key] = value*other
            return AD(self.func_val*other, new_der_dict)

    def __rmul__(self, other):
        """Overload to make sure commutativity of operation '*'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be multiplied to self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(1, {'x1': 1})
        >>> f1 = 10.0*x1
        >>> print(f1.func_val, f1.partial_dict)
        10.0 {'x1': 10.0}
        >>> x2 = 3.4*x1 - 1.4
        >>> print(x2.func_val, x2.partial_dict)
        2.0 {'x1': 3.4}
        >>> f2 = f1 * x2
        >>> print(f2.func_val, f2.partial_dict)
        20.0 {'x1': 54.0}
        >>> a = AD(2, {'a': 1})
        >>> b = AD(4, {'b': 1})
        >>> f3 = (4*a + 6*b)*a
        >>> print(f3.func_val, f3.partial_dict)
        64 {'a': 40, 'b': 12}
        """
        assert isinstance(other,(int, float, np.number)), "All values should be real float or int values!"
        # if other is not an AD class instance, treat as a constant
        new_der_dict = {}
        for key, value in self.partial_dict.items():
            new_der_dict[key] = value*other
        return AD(other*self.func_val, new_der_dict)

    def __truediv__(self, other):
        """Overload division operation '/'
        Parameters
        ----------
        other: AD class instance or float
            Elements to be divided from self. Can be an AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(1., {'x1':1})
        >>> f1 = x1/10.
        >>> print(f1.func_val, f1.partial_dict)
        0.1 {'x1': 0.1}
        >>> x2 = 3.4*x1
        >>> f2 = x2/x1
        >>> print(f2.func_val, f2.partial_dict)
        3.4 {'x1': 0.0}
        >>> a = AD(2, {'a': 1})
        >>> b = AD(4, {'b': 1})
        >>> f3 = a/b
        >>> print(f3.func_val, f3.partial_dict)
        0.5 {'a': 0.25, 'b': -0.125}
        """
        if isinstance(other, (np.ndarray,list)):
            return np.array(self)/np.array(other)
        try:
            # first try as other is an ad class instance
            new_der_dict = {}
            for k in itertools.chain(self.partial_dict.keys(), other.partial_dict.keys()):
                new_der_dict[k] = (self.partial_dict.get(k,0)*other.func_val - other.partial_dict.get(k,0)*self.func_val)/(other.func_val**2)
            return AD(self.func_val/other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            new_der_dict = {}
            for key, value in self.partial_dict.items():
                new_der_dict[key] = value/other
            return AD(self.func_val/other, new_der_dict)

    def __rtruediv__(self, other):
        """Overload to make right version of operation '/' works
        Parameters
        ----------
        other : AD class instance or float
            Elements to be multiplied to self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x1 = AD(1., {'x1':1})
        >>> f1 = 10.0/x1
        >>> print(f1.func_val, f1.partial_dict)
        10.0 {'x1': -10.0}
        >>> x2 = 3.4*x1 - 1.4
        >>> f2 = x2/x1
        >>> print(f2.func_val, f2.partial_dict)
        2.0 {'x1': 1.4}
        >>> a = AD(2, {'a': 1})
        >>> b = AD(4, {'b': 1})
        >>> f3 = 16./(a*b)
        >>> print(f3.func_val, f3.partial_dict)
        2.0 {'a': -1.0, 'b': -0.5}
        """
        assert isinstance(other,(int, float, np.number)), "All values should be real float or int values!"
        # if other is not an AD class instance, treat as a constant
        new_der_dict = {}
        for key, value in self.partial_dict.items():
            new_der_dict[key] = -other*value/(self.func_val**2)
        return AD(other/self.func_val, new_der_dict)

    def __pow__(self, other):
        """Overload power operation '**'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be powered to self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x = AD(2, {'x1': 1})
        >>> print(x**3)
        8 ({'x1': 12})
        >>> x = AD(2, {'x1': 1.})
        >>> f1 = AD.sin(x**3)
        >>> print(f1**3)
        0.9684132754691923 ({'x1': -5.127111370310495})
        >>> x = AD(2, {'x': 1})
        >>> f2 = x**x
        >>> print(f2.func_val, f2.partial_dict)
        4 {'x': 6.772588722239782}
        >>> a = AD(2, {'a': 1})
        >>> b = AD(4, {'b': 1})
        >>> f3 = a**b
        >>> print(f3.func_val, f3.partial_dict)
        16 {'a': 32.0, 'b': 11.090354888959125}
        """
        if isinstance(other, (np.ndarray,list)):
            return np.array(self) ** np.array(other)

        try:
            # First try as other is an AD class instance
            new_der_dict = {}
            for k in itertools.chain(self.partial_dict.keys(), other.partial_dict.keys()):
                new_der_dict[k] = self.func_val**other.func_val *\
                                    (self.partial_dict.get(k,0)*other.func_val/self.func_val +\
                                     other.partial_dict.get(k,0)*np.log(self.func_val))
            return AD(self.func_val**other.func_val, new_der_dict)
        except AttributeError:
            # If other is not an AD class instance, treat as a constant
            new_der_dict = {}
            for key, value in self.partial_dict.items():
                new_der_dict[key] = other * self.func_val**(other-1) * value
            return AD(self.func_val**other, new_der_dict)


    def __rpow__(self, other):
        """Overload right power operation '**'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be powered to self. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information
        Examples
        --------
        >>> x = AD(2, {'x1': 1})
        >>> print(3**x)
        9 ({'x1': 9.887510598012987})
        >>> x = AD(2, {'x1': 1.})
        >>> f1 = AD.sin(3**x)
        >>> print(f1**3)
        0.06999488183019169 ({'x1': -4.5902134148312985})
        >>> a = AD(2, {'a': 1})
        >>> b = AD(3, {'b': 1})
        >>> f2 = 2**(a+b)
        >>> print(f2.func_val, f2.partial_dict)
        32 {'a': 22.18070977791825, 'b': 22.18070977791825}
        """
        assert isinstance(other,(int, float, np.number)), "All values should be real float or int values!"
        # if other is not an AD class instance, treat as a constant
        new_der_dict = {}
        for key, value in self.partial_dict.items():
            new_der_dict[key] = other**self.func_val * np.log(other) * value
        return AD(other**self.func_val, new_der_dict)

    def __neg__(self):
        """Overload '-' to return the negative of an object

        Parameters
        ----------
        self: AD class instance or float
             Current AD instance
        Returns
        -------
        A new AD class instance with opposite function value and derivative

        Examples
        --------
        >>> x1 = AD(1., {'x1':1})
        >>> f_x1 = -x1
        >>> print(f_x1.func_val, f_x1.partial_dict)
        -1.0 {'x1': -1}
        >>> x2 = 3*x1
        >>> f_x2_x1 = -x2 + x1
        >>> print(f_x2_x1.func_val, f_x2_x1.partial_dict)
        -2.0 {'x1': -2}
        >>> f2 = AD(2, {'a': 1}) + AD(4, {'b': 1})
        >>> print(-f2)
        -6 ({'a': -1, 'b': -1})
        """
        # Pass to __rmul__ via multiply by float
        return self.__rmul__(-1)


    @staticmethod
    def sin(x):
        """A static method to calculate the sine function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a sin operator. Can be an AD class instance, whichi
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(np.pi/2, {'x1': 1.})
        >>> f1 = AD.sin(x1)
        >>> print(f1.func_val, f1.partial_dict)
        1.0 {'x1': 6.123233995736766e-17}
        >>> x2 = AD.sin(np.pi)
        >>> print(x2)
        1.2246467991473532e-16
        """
        if isinstance(x,(np.ndarray,list)):
            new_x = np.zeros(np.array(x).shape, dtype=AD)
            for idx, ele in np.ndenumerate(np.array(x)):
                new_x[idx] = AD.sin(ele)
            return new_x
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = np.cos(x.func_val)*new_der_dict[var]
            return AD(np.sin(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.sin(x)


    @staticmethod
    def cos(x):
        """A static method to calculate the cosine function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a cosine operator. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(np.pi/2, {'x1': 1.})
        >>> f1 = AD.cos(x1)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        0.0 {'x1': -1.0}
        >>> x2 = AD.cos(np.pi)
        >>> print(x2)
        -1.0
        """
        if isinstance(x,(np.ndarray,list)):
            new_x = np.zeros(np.array(x).shape, dtype=AD)
            for idx, ele in np.ndenumerate(np.array(x)):
                new_x[idx] = AD.cos(ele)
            return new_x
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = -np.sin(x.func_val)*new_der_dict[var]
            return AD(np.cos(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.cos(x)

    @staticmethod
    def tan(x):
        """A static method to calculate the tangent function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a tangent operator. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(np.pi, {'x1': 1.})
        >>> f1 = AD.tan(x1)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        -0.0 {'x1': 1.0}
        >>> x2 = AD.tan(np.pi)
        >>> print(x2.round(1))
        -0.0
        """
        if isinstance(x,(np.ndarray,list)):
            new_x = np.zeros(np.array(x).shape, dtype=AD)
            for idx, ele in np.ndenumerate(np.array(x)):
                new_x[idx] = AD.tan(ele)
            return new_x
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = new_der_dict[var]/(np.cos(x.func_val)**2)
            return AD(np.tan(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.tan(x)

    @staticmethod
    def arcsin(x):
        """A static method to calculate the arcsine function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated an arcsin operator. Can be an AD class instance, whichi
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x = AD(0.25, {'x1': 1.})
        >>> print(AD.arcsin(x))
        0.25268025514207865 ({'x1': 1.0327955589886444})
        >>> print(AD.arcsin(0.25))
        0.25268025514207865
        """
        if isinstance(x,(np.ndarray,list)):
            new_x = np.zeros(np.array(x).shape, dtype=AD)
            for idx, ele in np.ndenumerate(np.array(x)):
                new_x[idx] = AD.arcsin(ele)
            return new_x
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = 1 / np.sqrt(1 - x.func_val**2)*new_der_dict[var]
            return AD(np.arcsin(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.arcsin(x)

    @staticmethod
    def arccos(x):
        """A static method to calculate the arccos function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated an arccos operator. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x = AD(0.25, {'x1': 1.})
        >>> print(AD.arccos(x))
        1.318116071652818 ({'x1': -1.0327955589886444})
        >>> print(AD.arccos(0.25))
        1.318116071652818
        """
        if isinstance(x,(np.ndarray,list)):
            new_x = np.zeros(np.array(x).shape, dtype=AD)
            for idx, ele in np.ndenumerate(np.array(x)):
                new_x[idx] = AD.arccos(ele)
            return new_x
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = - 1 / np.sqrt(1 - x.func_val**2)*new_der_dict[var]
            return AD(np.arccos(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.arccos(x)

    @staticmethod
    def arctan(x):
        """A static method to calculate the arctan function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated an arctan operator. Can be an AD class instance, whichi
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x = AD(0.25, {'x1': 1.})
        >>> print(AD.arctan(x))
        0.24497866312686414 ({'x1': 0.9411764705882353})
        >>> print(AD.arctan(0.25))
        0.24497866312686414
        """
        if isinstance(x,(np.ndarray,list)):
            new_x = np.zeros(np.array(x).shape, dtype=AD)
            for idx, ele in np.ndenumerate(np.array(x)):
                new_x[idx] = AD.arctan(ele)
            return new_x
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = 1 / (1 + x.func_val**2)*new_der_dict[var]
            return AD(np.arctan(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.arctan(x)

    @staticmethod
    def sqrt(x):
        """Overload power operation 'sqrt'
        Parameters
        ----------
        other : AD class instance or float
            Elements to be put to 1/2 power. Can be a AD class instance, which
            will update function value and partial derivative dictionary; Or a con-
            -stant, which will only update function value.
        Returns
        -------
        A new AD class instance with updated information

        Examples
        --------
        >>> x1 = AD(1.0, {'x1': 1.0})
        >>> f1 = AD.sqrt(x1)
        >>> print(f1.func_val, f1.partial_dict)
        1.0 {'x1': 0.5}
        >>> f2 = AD.sqrt(1.0)
        >>> print(f2)
        1.0
        >>> x2 = AD(0, {'x2': 1})
        >>> f3 = AD.sqrt(AD.cos(x2))
        >>> print(f3.func_val, f3.partial_dict)
        1.0 {'x2': -0.0}
        """
        if isinstance(x,(np.ndarray,list)):
            new_x = np.zeros(np.array(x).shape, dtype=AD)
            for idx, ele in np.ndenumerate(np.array(x)):
                new_x[idx] = AD.sqrt(ele)
            return new_x
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = new_der_dict[var]/(2 * (x.func_val**(1/2)))
            return AD(np.sqrt(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.sqrt(x)

    @staticmethod
    def log(x,base = np.e):
        """A static method to calculate the logrithmic function of a AD instance,
            or a float for multiple bases, with the default being e.
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated on a logrithm. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output.
        Base : Constant integer or float to be used as base in logarithm.
            Base is a default of e, but can be changed by entering in after x in log
            method.
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(np.e**2, {'x1': 1.})
        >>> f0 = AD.log(x1)
        >>> print(f0.func_val.round(1), f0.partial_dict)
        2.0 {'x1': 0.1353352832366127}
        >>> f1 = AD.log(x1, np.e**2)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        2.0 {'x1': 0.06766764161830635}
        >>> x2 = AD.log(np.e)
        >>> print(x2)
        1.0
        >>> x3 = AD.log(4, 2)
        >>> print(x3)
        2.0
        >>> x4 = AD.log(2, 32)
        >>> print(x4.round(1))
        0.2
        """
        if base == 0 or not (isinstance(base, (int, float, np.number))):
            raise Exception("Base Must be a constant integer or a float not equal to 0")

        if isinstance(x,(np.ndarray,list)):
            new_x = np.zeros(np.array(x).shape, dtype=AD)
            for idx, ele in np.ndenumerate(np.array(x)):
                new_x[idx] = AD.log(ele, base)
            return new_x

        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = new_der_dict[var]/(x.func_val * np.log(base))
            return AD(np.log(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.log(x) / np.log(base)

    @staticmethod
    def sinh(x):
        """A static method to calculate the hyperbolic sine function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a sinh operator. Can be an AD class instance, whichi
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(0.0, {'x1': 1.0})
        >>> f1 = AD.sinh(x1)
        >>> print(f1.func_val, f1.partial_dict)
        0.0 {'x1': 1.0}
        >>> x2 = AD.sinh(0)
        >>> print(x2)
        0.0
        """
        if isinstance(x,(np.ndarray,list)):
            new_x = np.zeros(np.array(x).shape, dtype=AD)
            for idx, ele in np.ndenumerate(np.array(x)):
                new_x[idx] = AD.sinh(ele)
            return new_x
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = np.cosh(x.func_val)*new_der_dict[var]
            return AD(np.sinh(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.sinh(x)

    @staticmethod
    def cosh(x):
        """A static method to calculate the hyperbolic cosine function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a cosine operator. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(0.0, {'x1': 1.0})
        >>> f1 = AD.cosh(x1)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        1.0 {'x1': 0.0}
        >>> x2 = AD.cosh(0)
        >>> print(x2)
        1.0
        """
        if isinstance(x,(np.ndarray,list)):
            new_x = np.zeros(np.array(x).shape, dtype=AD)
            for idx, ele in np.ndenumerate(np.array(x)):
                new_x[idx] = AD.cosh(ele)
            return new_x
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = np.sinh(x.func_val)*new_der_dict[var]
            return AD(np.cosh(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.cosh(x)

    @staticmethod
    def tanh(x):
        """A static method to calculate the hyperbolic tangent function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated a hyperbolic tangent operator. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x1 = AD(0.0, {'x1': 1.0})
        >>> f1 = AD.tanh(x1)
        >>> print(f1.func_val.round(1), f1.partial_dict)
        0.0 {'x1': 1.0}
        >>> x2 = AD.tanh(np.pi)
        >>> print(x2.round(1))
        1.0
        """
        if isinstance(x,(np.ndarray,list)):
            new_x = np.zeros(np.array(x).shape, dtype=AD)
            for idx, ele in np.ndenumerate(np.array(x)):
                new_x[idx] = AD.tanh(ele)
            return new_x
        try:
            # First try as x is an AD instance
            new_der_dict = x.partial_dict.copy()
            for var in new_der_dict.keys():
                new_der_dict[var] = new_der_dict[var]/(np.cosh(x.func_val)**2)
            return AD(np.tanh(x.func_val), new_der_dict)
        except AttributeError:
            # if x is not an AD class instance, treat as a constant
            return np.tanh(x)

    @staticmethod
    def exp(x):
        """A static method to calculate the natrual an exponent function of a AD instance, or a float
        Parameters
        ----------
        x: AD class instance or float, in radians
           Elements to be operated an exponent. Can be an AD class instance, which
           will update function value and partial derivative dictionary; or a constant, whi-
           -ch will give a constant output
        Returns
        -------
        A new AD class with updated information
        Examples
        --------
        >>> x = AD(2, {'x1': 1.})
        >>> print(AD.exp(x))
        7.3890560989306495 ({'x1': 7.3890560989306495})
        >>> x2 = 2
        >>> print(AD.exp(x2))
        7.3890560989306495
        """
        return np.e**x


    @staticmethod
    def logistic(x, x_0=0, k=1, L=1):
        """A static method to calculate the logistic function of an AD instance or
        float. Logistic function L/(1+e^(-k(x-x_0))). More commonly used as 1/(1+e^(-x))
        Parameters
        ----------
        x: AD class instance of float
            Elements to be used as base of logistic function.
        x_0: int or float
            This represents the center of logistic function; default set to zero.
        k: int or float
            Logistic growth rate of function; default set to 1.
        L: int or float
            Maximum value of logistic function; default set to 1.
        Returns
        -------
        A new AD class with updated information; otherwise a float value.

        Examples
        --------
        >>> x = AD(1.5)
        >>> print(AD.logistic(x))
        0.8175744761936437 ({'x1': 0.14914645207033284})
        >>> f = x + AD(-0.5, {'x2': 1})
        >>> print(AD.logistic(f))
        0.7310585786300049 ({'x1': 0.19661193324148188, 'x2': 0.19661193324148188})
        """
        return L/(1 + AD.exp(-k * (x - x_0)))

    @staticmethod
    def sum(a, axis=None):
        """
        A summation operation for AD instances array, it is the same as numpy.sum
        """
        return np.sum(np.array(a),axis=axis)

    @staticmethod
    def mean(a, axis=None):
        """
        An average operation for AD instances array, it is the same as numpy.mean
        """
        return np.mean(np.array(a), axis=axis)

    @staticmethod
    def dot(a, b):
        """
        An array(matrix) multiplication operation for AD instances array, it is the same as numpy.dot
        """
        return np.dot(np.array(a), np.array(b))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
