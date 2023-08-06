
import pytest

from NoetherAutoDiff import *

# Generate three NoetherAutoDiff class instances for testing
@pytest.fixture
def nad_obj1():
    '''Returns a NoetherAutoDiff instance, with jambo function'''
    return NoetherAutoDiff("sin(x)^cos(x-5/3+4^x*y/z)/tan(3*x)+exp(3*x-1)", 0,
                           {'x': 1.4, 'y': 2.4, 'z': 3.4},
                           {'x': 1, 'y': 1, 'z': 1})


@pytest.fixture
def nad_obj2():
    '''Returns a NoetherAutoDiff instance, same func as above but using reverse mode'''
    return NoetherAutoDiff("sin(x)^cos(x-5/3+4^x*y/z)/tan(3*x)+exp(3*x-1)", 1,
                           {'x': 1.4, 'y': 2.4, 'z': 3.4},
                           {'x': 1, 'y': 1, 'z': 1})


@pytest.fixture
def nad_obj3():
    '''Returns a NoetherAutoDiff instance, with two variables'''
    return NoetherAutoDiff("2*x + 3*y", 0, {'x': 2.3, 'y': 3.5}, {'x': 1.0, 'y': 1.0})


# Generate three NoetherAutoDiff_Vector class instances for testing 
@pytest.fixture
def nadv_obj1():
    '''Returns an instance of NoetherAutoDiff_Vector instance'''
    return NoetherAutoDiff_Vector("sin(x0)^cos(x0-5/3+4^x0*x1/x2)/tan(3*x0)+exp(3*x0-1)", 0,
                                   [1.4, 2.4, 3.4], [1, 1, 1])


@pytest.fixture
def nadv_obj2():
    '''Returns an instance of NoetherAutoDiff_Vector instance,same as above but with reverse more'''
    return NoetherAutoDiff_Vector("sin(x0)^cos(x0-5/3+4^x0*x1/x2)/tan(3*x0)+exp(3*x0-1)", 1,
                                   [1.4, 2.4, 3.4], [1, 1, 1])


@pytest.fixture
def nadv_obj3():
    '''Returns an another instance of NoetherAutoDiff_Vector instance'''
    return NoetherAutoDiff_Vector("2.5 * x0 - 3.5 * x1 + 1.25 * x2", 0, [2, 2, 2], [2, 2, 2])


# Generate three NoetherAD class instances for testing
@pytest.fixture
def noetherAD_obj1():
    '''Returns an instance of NoetherAD class with two functions'''
    return NoetherAD(["2.5 * x0 - 3.5 * x1 + 1.25 * x2",
                      "10*x0 + 5*x1 + 2*x2"], 0, [-2, 2, 2], [1, 1, 1])


@pytest.fixture
def noetherAD_obj2():
    '''Returns the same instance of NoetherAD class as above but evaluated with reverse mode'''
    return NoetherAD(["2.5 * x0 - 3.5 * x1 + 1.25 * x2",
                        "10*x0 + 5*x1 + 2*x2"], 1, [-2, 2, 2], [1, 1, 1])


@pytest.fixture
def noetherAD_obj3():
    '''Returns the same instance of NoetherAD class as above but evaluated at different 
    evaluation point and seed values, to help check comparison operators'''
    return NoetherAD(["2.5 * x0 + 3.5 * x1 + 1.25 * x2",
                        "10*x0 + 5*x1 + 2*x2"], 1, [2, 2, 2], [2, 2, 2])


class TestNoetherAutoDiff:
    def test_NoetherAutoDiff_val(self, nad_obj1, nad_obj2, nad_obj3):
        # check val
        assert nad_obj1.val == 25.095548918554428
        assert nad_obj2.val == 25.095548918554428
        assert nad_obj3.val == 15.1

    def test_NoetherAutoDiff_deriv1(self, nad_obj1, nad_obj2, nad_obj3):
        # check derivatives at x
        assert nad_obj1.deriv['x'] == 69.57424922848773
        assert nad_obj2.deriv['x'] == 69.57424922848773
        assert nad_obj3.deriv['x'] == 2.0

    def test_NoetherAutoDiff_deriv2(self, nad_obj1, nad_obj2, nad_obj3):
        # check derivatives at y
        assert nad_obj1.deriv['y'] == -0.016870006832635686
        assert nad_obj2.deriv['y'] == -0.016870006832635686
        assert nad_obj3.deriv['y'] == 3.0

    def test_NoetherAutoDiff_deriv3(self, nad_obj1, nad_obj2, nad_obj3):
        # check derivative at z
        assert nad_obj1.deriv['z'] == 0.0119082401171546
        assert nad_obj2.deriv['z'] == 0.0119082401171546

    def test_NoetherAutoDiff_equality(self, nad_obj1, nad_obj2, nad_obj3):
        # check overriding == (two object are equal if their val atrributes are equal)
        assert (nad_obj1 == nad_obj1) == True
        assert (nad_obj1 == nad_obj2) == True
        assert (nad_obj1 == nad_obj3) == False

    def test_NoetherAutoDiff_inequality(self, nad_obj1, nad_obj2, nad_obj3):
        # check overriding !=
        assert (nad_obj1 != nad_obj1) == False
        assert (nad_obj1 != nad_obj2) == False
        assert (nad_obj1 != nad_obj3) == True

    def test_NoetherAutoDiff_lt_(self, nad_obj1, nad_obj2, nad_obj3):
        # check overriding <
        assert (nad_obj1 < nad_obj1) == False
        assert (nad_obj1 < nad_obj2) == False
        assert (nad_obj1 < nad_obj3) == False

    def test_NoetherAutoDiff_le_(self, nad_obj1, nad_obj2, nad_obj3):
        # check overriding <=
        assert (nad_obj1 <= nad_obj1) == True
        assert (nad_obj1 <= nad_obj2) == True
        assert (nad_obj1 <= nad_obj3) == False

    def test_NoetherAutoDiff_gt_(self, nad_obj1, nad_obj2, nad_obj3):
        # check overriding >
        assert (nad_obj1 > nad_obj1) == False
        assert (nad_obj1 > nad_obj2) == False
        assert (nad_obj1 > nad_obj3) == True

    def test_NoetherAutoDiff_ge_(self, nad_obj1, nad_obj2, nad_obj3):
        # check overriding >=
        assert (nad_obj1 >= nad_obj1) == True
        assert (nad_obj1 >= nad_obj2) == True
        assert (nad_obj1 >= nad_obj3) == True


class TestNoetherAutoDiff_Vector:
    def test_NoetherAutoDiff_Vector_val(self, nadv_obj1, nadv_obj2, nadv_obj3):
        # check val
        assert nadv_obj1.val == 25.095548918554428
        assert nadv_obj2.val == 25.095548918554428
        assert nadv_obj3.val == 0.5

    def test_NoetherAutoDiff_Vector_deriv1(self, nadv_obj1, nadv_obj2, nadv_obj3):
        # check derivatives at x
        assert nadv_obj1.deriv[0] == 69.57424922848773
        assert nadv_obj2.deriv[0] == 69.57424922848773
        assert nadv_obj3.deriv[0] == 5.0
    
    def test_NoetherAutoDiff_Vector_deriv2(self, nadv_obj1, nadv_obj2, nadv_obj3):
        # check derivatives at y
        assert nadv_obj1.deriv[1] == -0.016870006832635686
        assert nadv_obj2.deriv[1] == -0.016870006832635686
        assert nadv_obj3.deriv[1] == -7.0

    def test_NoetherAutoDiff_Vector_deriv3(self, nadv_obj1, nadv_obj2, nadv_obj3):
        # check derivative at z
        assert nadv_obj1.deriv[2] == 0.0119082401171546
        assert nadv_obj2.deriv[2] == 0.0119082401171546
        assert nadv_obj3.deriv[2] == 2.5
    
    def test_NoetherAutoDiff_Vector_equality(self, nadv_obj1, nadv_obj2, nadv_obj3):
        # check overriding == (two object are equal if their val atrributes are equal)
        assert (nadv_obj1 == nadv_obj1) == True
        assert (nadv_obj1 == nadv_obj2) == True
        assert (nadv_obj1 == nadv_obj3) == False

    def test_NoetherAutoDiff_Vector_inequality(self, nadv_obj1, nadv_obj2, nadv_obj3):
        # check overriding !=
        assert (nadv_obj1 != nadv_obj1) == False
        assert (nadv_obj1 != nadv_obj2) == False
        assert (nadv_obj1 != nadv_obj3) == True

    def test_NoetherAutoDiff_Vector_lt_(self, nadv_obj1, nadv_obj2, nadv_obj3):
        # check overriding <
        assert (nadv_obj1 < nadv_obj1) == False
        assert (nadv_obj1 < nadv_obj2) == False
        assert (nadv_obj1 < nadv_obj3) == False

    def test_NoetherAutoDiff_Vector_le_(self, nadv_obj1, nadv_obj2, nadv_obj3):
        # check overriding <=
        assert (nadv_obj1 <= nadv_obj1) == True
        assert (nadv_obj1 <= nadv_obj2) == True
        assert (nadv_obj1 <= nadv_obj3) == False

    def test_NoetherAutoDiff_Vector_gt_(self, nadv_obj1, nadv_obj2, nadv_obj3):
        # check overriding >
        assert (nadv_obj1 > nadv_obj1) == False
        assert (nadv_obj1 > nadv_obj2) == False
        assert (nadv_obj1 > nadv_obj3) == True

    def test_NoetherAutoDiff_Vector_ge_(self, nadv_obj1, nadv_obj2, nadv_obj3):
        # check overriding >=
        assert (nadv_obj1 >= nadv_obj1) == True
        assert (nadv_obj1 >= nadv_obj2) == True
        assert (nadv_obj1 >= nadv_obj3) == True


class TestNoetherAD:
    def test_NoetherAD_val(self, noetherAD_obj1, noetherAD_obj2, noetherAD_obj3):
        # check val
        assert noetherAD_obj1.val == [-9.5, -6.0]
        assert noetherAD_obj2.val == [-9.5, -6.0]
        assert noetherAD_obj3.val == [14.5, 34.0]

    def test_NoetherAD_deriv(self, noetherAD_obj1, noetherAD_obj2, noetherAD_obj3):
        # check derivatives in the [x0, x1, x2]
        assert noetherAD_obj1.deriv == [[2.5, -3.5, 1.25], [10.0, 5.0, 2.0]]
        assert noetherAD_obj2.deriv == [[2.5, -3.5, 1.25], [10.0, 5.0, 2.0]]
        assert noetherAD_obj3.deriv == [[5.0, 7.0, 2.5], [20.0, 10.0, 4.0]]

    def test_NoetherAD_jacobian(self, noetherAD_obj1, noetherAD_obj2, noetherAD_obj3):
        # check derivatives in the [x0, x1, x2]
        assert noetherAD_obj1.get_jacobian() == [[2.5, -3.5, 1.25], [10.0, 5.0, 2.0]]
        assert noetherAD_obj2.get_jacobian() == [[2.5, -3.5, 1.25], [10.0, 5.0, 2.0]]
        assert noetherAD_obj3.get_jacobian() == [[2.5, 3.5, 1.25], [10.0, 5.0, 2.0]]

    def test_NoetherAD_equality(self, noetherAD_obj1, noetherAD_obj2, noetherAD_obj3):
        # check overriding == (two object are equal if their val atrributes are equal)
        assert (noetherAD_obj1 == noetherAD_obj1) == True
        assert (noetherAD_obj1 == noetherAD_obj2) == True
        assert (noetherAD_obj1 == noetherAD_obj3) == False

    def test_NoetherAD_inequality(self, noetherAD_obj1, noetherAD_obj2, noetherAD_obj3):
        # check overriding !=
        assert (noetherAD_obj1 != noetherAD_obj1) == False
        assert (noetherAD_obj1 != noetherAD_obj2) == False
        assert (noetherAD_obj1 != noetherAD_obj3) == True

    def test_NoetherAD_lt_(self, noetherAD_obj1, noetherAD_obj2, noetherAD_obj3):
        # check overriding <
        assert (noetherAD_obj1 < noetherAD_obj2) == False
        assert (noetherAD_obj1 < noetherAD_obj3) == True

    def test_NoetherAD_le_(self, noetherAD_obj1, noetherAD_obj2, noetherAD_obj3):
        # check overriding <=
        assert (noetherAD_obj1 <= noetherAD_obj3) == True

    def test_NoetherAD_gt_(self, noetherAD_obj1, noetherAD_obj2, noetherAD_obj3):
        # check overriding >
        assert (noetherAD_obj1 > noetherAD_obj2) == False
        assert (noetherAD_obj1 > noetherAD_obj3) == False

    def test_NoetherAD_ge_(self, noetherAD_obj1, noetherAD_obj2, noetherAD_obj3):
        # check overriding >=
        assert (noetherAD_obj1 >= noetherAD_obj3) == False
