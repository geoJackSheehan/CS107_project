# Test code for ad interface
import pytest
import numpy as np

from bad_package.elementary_functions import *
from bad_package.fad import DualNumber
from bad_package.interface import AutoDiff
from bad_package.interface import ReverseAD

class TestADInterface():

    def test_scalar_get_primal(self):
        # Scalar function
        def func(x):
            return 4*x + 3
        x = np.array([2])
        ad = AutoDiff(func, x)
        result = ad.get_primal()
        assert pytest.approx([11]) == result

        # Scalar function without putting into array
        def func(x):
            return 4*x + 3
        x = 2
        ad = AutoDiff(func, x)
        result = ad.get_primal()
        assert pytest.approx([11]) == result   

        # Vector function
        def func2(x):
            return logBase(x, 2) + exp(x) - e
        x = [2]
        ad = AutoDiff([func, func2], x)
        result = ad.get_primal()
        assert pytest.approx([11, 5.6707742704]) == result

    def test_scalar_get_jacobian(self):
        # Scalar function
        def func(x):
            return 4*x + 3
        x = np.array([2])
        ad = AutoDiff(func, x)
        result = ad.get_jacobian()
        assert pytest.approx([4]) == result

        # Vector function


    def test_vector_get_primal(self):
        def func(x):
            return x[0]**2 + 3*x[1] + 5
        x = np.array([1, 2])
        ad = AutoDiff(func, x)
        result = ad.get_primal()
        assert pytest.approx([12]) == result
        
    def test_vector_get_jacobian(self):
        # Scalar function
        def func(x):
            return x[0]**2 + 3*x[1] + 5
        x = np.array([1, 2])
        ad = AutoDiff(func, x)
        result = ad.get_jacobian()
        assert pytest.approx([2,3]) == result[0]

        # Vector function
        def func2(x):
            return sin(x[0]) + cos(x[1])

        f = [func, func2]
        ad = AutoDiff(f, x)
        result = ad.get_jacobian()
        assert pytest.approx([2,3]) == result[0]
        assert pytest.approx([np.cos(1), -np.sin(2)]) == result[1]

#     def test_scalar_get_jacobian_RM(self):
#         def func(x):
#             return 4*x
#         x = np.array([2])
#         rm = ReverseAD(func, x)
#         rm.compute()
#         result = rm.get_jacobian()
#         assert pytest.approx([4]) == result
        
        
    def test_scalar_get_jacobian_RM(self):
        def func(x):
            return (5*x + 50)/(2*x**2)
        f = np.array([func])
        x = np.array([5])
        rm = ReverseAD(f, x)
        result = rm.get_jacobian()
        assert pytest.approx([-0.5]) == result
        
    def test_vector_get_jacobian_RM(self):
        def func1(x):
            return (5*x[0] + 50)/(2*x[1]**2)
        def func2(x):
            return 10 + 2*x[1]
            # return sin(x)
        f = np.array([func1, func2])
        x = np.array([1, 2])
        rm = ReverseAD(f,x)
        result = rm.get_jacobian()
        assert pytest.approx([0.625, -6.875, 0, 2]) == result

# Testing Elementary Functions for ReverseMode as I fix them
        
    def test_vector_sin_jacobian_RM(self):
        def ef1(x):
            return sin(x)

        f = np.array([ef1])
        x = np.array([2.5])
        rm = ReverseAD(f, x)
        result = rm.get_jacobian()
        assert pytest.approx([np.cos(2.5)]) == result
        
    def test_vector_cos_jacobian_RM(self):
        def ef1(x):
            return cos(x)

        f = np.array([ef1])
        x = np.array([2.5])
        rm = ReverseAD(f, x)
        result = rm.get_jacobian()
        assert pytest.approx([-np.sin(2.5)]) == result
        
    def test_vector_tan_jacobian_RM(self):
        def ef1(x):
            return tan(x)

        f = np.array([ef1])
        x = np.array([2.5])
        rm = ReverseAD(f, x)
        result = rm.get_jacobian()
        assert pytest.approx([1/(np.cos(2.5)**2)]) == result
        
    def test_vector_csc_jacobian_RM(self):
        def ef1(x):
            return csc(x)

        f = np.array([ef1])
        x = np.array([2.5])
        rm = ReverseAD(f, x)
        result = rm.get_jacobian()
        assert pytest.approx([(-1/np.sin(2.5))*(1/np.tan(2.5))]) == result
        
    def test_vector_sec_jacobian_RM(self):
        def ef1(x):
            return sec(x)

        f = np.array([ef1])
        x = np.array([2.5])
        rm = ReverseAD(f, x)
        result = rm.get_jacobian()
        assert pytest.approx([(1/np.cos(2.5))*np.tan(2.5)]) == result
        
    def test_vector_cot_jacobian_RM(self):
        def ef1(x):
            return cot(x)

        f = np.array([ef1])
        x = np.array([2.5])
        rm = ReverseAD(f, x)
        result = rm.get_jacobian()
        assert pytest.approx([((-1/sin(2.5)))**2]) == result

    def test_vector_1arg_sinh_jacobian_RM(self):
        def ef1(x):
            return sinh(x)

        f = np.array([ef1])
        x = np.array([0.7])
        rm = ReverseAD(f, x)
        result = rm.get_jacobian()
        assert pytest.approx([np.cosh(0.7)]) == result

    def test_vector_1arg_cosh_jacobian_RM(self):
        def ef1(x):
            return cosh(x)

        f = np.array([ef1])
        x = np.array([0.25])
        rm = ReverseAD(f, x)
        result = rm.get_jacobian()
        assert pytest.approx([np.sinh(0.25)]) == result
    
    def test_vector_1arg_tanh_jacobian_RM(self):
        def ef1(x):
            return 3*tanh(x)
        
        f = np.array([ef1])
        x = np.array([1.25])
        rm = ReverseAD(f, x)
        result = rm.get_jacobian()
        assert pytest.approx([3/(np.cosh(1.25)**2)]) == result


    def test_vector_exp_jacobian_RM(self):
        def ef(x):
            return 5*exp(x[0]) + 2*exp(x[1]) + 3*exp(x[2])

        f = np.array([ef])
        x = np.array([0, 1, 2])
        rm = ReverseAD(f, x)
        result = rm.get_jacobian()
        assert pytest.approx([5, 2*np.exp(1), 3*np.exp(2)]) == result

    
    def test_vector_logs_jacobian_RM(self):
        def ef(x):
            return 3*x[0] + logBase(x[1], 3) + ln(x[2])
        
        f = np.array([ef])
        x = np.array([2, 4, 27])
        rm = ReverseAD(f, x)
        result = rm.get_jacobian()
        assert pytest.approx([3, 1/(np.log(3)*4), 1/27]) == result


    