#!/usr/bin/python
import os
import sys
from ctypes import *
from sys import platform

if platform == "darwin":
    thisdir = os.path.dirname(os.path.abspath(__file__))
    lib = cdll.LoadLibrary(thisdir + '/libNoetherAutoDiff.dylib')
elif platform == "win32":
    thisdir = os.path.dirname(os.path.abspath(__file__))
    lib = cdll.LoadLibrary(thisdir + '/NoetherAutoDiff.dll')
else:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    lib = cdll.LoadLibrary(thisdir + '/NoetherADPy.so')



def wrapper(lib, funcname, restype, argtypes):
    '''
        A wrapper that rest the restype and argtypes of a C
        function and returns the function.
        '''
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


class NoetherAutoDiff(Structure):

    def __init__(self, input, mode, inits={}, seeds={}):

        # inputs
        self.input = input
        self.mode = mode
        self.inits = inits
        self.seeds = seeds
        self.size = len(inits)

        # Get ctype arry of the input equation
        input_func = create_string_buffer(str.encode(input))

        # Get ctype array of the init keys and values
        init_keys_arr = (c_char * self.size)()
        init_keys_arr[:] = [bytes(i, 'utf-8') for i in list(inits.keys())]
        init_vals_arr = (c_double * self.size)()
        init_vals_arr[:] = list(inits.values())

        # Get ctype array of the seed keys and values
        seed_keys_arr = (c_char * self.size)()
        seed_keys_arr[:] = [bytes(i, 'utf-8') for i in list(seeds.keys())]
        seed_vals_arr = (c_double * self.size)()
        seed_vals_arr[:] = list(seeds.values())

        # Define the argtypes and restype of the C functions
        self.createNoetherAutoDiff = wrapper(lib, 'createNoetherAutoDiff', c_void_p,
                                             [POINTER(c_char), c_int, POINTER(c_char), POINTER(c_double),
                                              POINTER(c_char), POINTER(c_double), c_int])

        get_val = wrapper(lib, 'get_val', c_double, [c_void_p])
        get_deriv = wrapper(lib, 'get_deriv', c_double, [c_char_p, c_void_p])
        self.equal = wrapper(lib, 'equal', c_bool, [c_void_p, c_void_p])
        self.notEqual = wrapper(lib, 'notEqual', c_bool, [c_void_p, c_void_p])
        self.lessThan = wrapper(lib, 'lessThan', c_bool, [c_void_p, c_void_p])
        self.lessThanOrEqaul = wrapper(
            lib, 'lessThanOrEqaul', c_bool, [c_void_p, c_void_p])
        self.greaterThan = wrapper(lib, 'greaterThan', c_bool, [
                                   c_void_p, c_void_p])
        self.greaterThanOrEqual = wrapper(
            lib, 'greaterThanOrEqual', c_bool, [c_void_p, c_void_p])

        # Pass args to C and get C noether object
        self.noether = self.createNoetherAutoDiff(input_func, mode, init_keys_arr,
                                                  init_vals_arr, seed_keys_arr, seed_vals_arr, self.size)

        # Fetch value of the function from C
        self.val = get_val(self.noether)

        # Fetch derivative results from C
        self.deriv = {}
        for key in self.inits.keys():
            self.deriv[key] = get_deriv(key.encode('utf-8'), self.noether)

    # Comparison operators
    def __eq__(self, other):
        return self.equal(self.noether, other.noether)

    def __ne__(self, other):
        return self.notEqual(self.noether, other.noether)

    def __lt__(self, other):
        return self.lessThan(self.noether, other.noether)

    def __le__(self, other):
        return self.lessThanOrEqaul(self.noether, other.noether)

    def __gt__(self, other):
        return self.greaterThan(self.noether, other.noether)

    def __ge__(self, other):
        return self.greaterThanOrEqual(self.noether, other.noether)

    def print(self):
        print("Input function:")
        print("  f = {}".format(self.input))

        print("Evaluated at: ")
        for key, val in self.inits.items():
            print("  {}={}  ".format(key, val))

        print("\nNumeric Value: ")
        print("  f = {}".format(self.val))

        print("Derivates: ")
        for key, val in self.deriv.items():
            print("  df/d{} = {}  ".format(key, val))


class NoetherAutoDiff_Vector(Structure):

    def __init__(self, input, mode, inits=[], seeds=[]):

        # inputs
        self.input = input
        self.mode = mode
        self.inits = inits
        self.seeds = seeds
        self.size = len(inits)

        # Get ctype arry of the input equation
        input_func = create_string_buffer(str.encode(input))

        # Get ctype array of the init keys and values
        inits_arr = (c_double * self.size)()
        inits_arr[:] = inits

        # Get ctype array of the seed keys and values
        seeds_arr = (c_double * self.size)()
        seeds_arr[:] = seeds

        # Define the argtypes and restype of the C functions
        self.createNoetherAD_Vector = wrapper(lib, 'createNoetherAD_Vector', c_void_p, [POINTER(c_char),
                                                                                        c_int, POINTER(c_double), POINTER(c_double), c_int])
        # POINTER(c_double), POINTER(c_double * self.size)])
        self.get_val_vector = wrapper(lib, 'get_val_vector', c_double, [c_void_p])

        self.get_deriv_vector = wrapper(
            lib, 'get_deriv_vector', c_double, [c_void_p, c_int])

        self.get_jacobian_vector = wrapper(
            lib, 'get_jacobian_vector', c_double, [c_void_p, c_int])

        self.equal_Vector = wrapper(
            lib, 'equal_Vector', c_bool, [c_void_p, c_void_p])

        self.notEqual_Vector = wrapper(
            lib, 'notEqual_Vector', c_bool, [c_void_p, c_void_p])

        self.lessThan_Vector = wrapper(
            lib, 'lessThan_Vector', c_bool, [c_void_p, c_void_p])

        self.lessThanOrEqaul_Vector = wrapper(
            lib, 'lessThanOrEqaul_Vector', c_bool, [c_void_p, c_void_p])

        self.greaterThan_Vector = wrapper(
            lib, 'greaterThan_Vector', c_bool, [c_void_p, c_void_p])

        self.greaterThanOrEqual_Vector = wrapper(
            lib, 'greaterThanOrEqual_Vector', c_bool, [c_void_p, c_void_p])

        # Pass args to C and get C noether object
        self.noether = self.createNoetherAD_Vector(input_func, mode, inits_arr, seeds_arr,
                                                   self.size)  # self.temp, byref(self.temp2))

        # Get val and derivatives
        self.val = self.get_val_vector(self.noether)

        self.deriv = []
        for i in range(self.size):
            self.deriv.append(self.get_deriv_vector(self.noether, c_int(i)))

        self.jacobian = []
        for i in range(self.size):
            self.jacobian.append(self.get_jacobian_vector(self.noether, c_int(i)))

    def get_jacobian(self):
        return self.jacobian

    # Comparison operators
    def __eq__(self, other):
        return self.equal_Vector(self.noether, other.noether)

    def __ne__(self, other):
        return self.notEqual_Vector(self.noether, other.noether)

    def __lt__(self, other):
        return self.lessThan_Vector(self.noether, other.noether)

    def __le__(self, other):
        return self.lessThanOrEqaul_Vector(self.noether, other.noether)

    def __gt__(self, other):
        return self.greaterThan_Vector(self.noether, other.noether)

    def __ge__(self, other):
        return self.greaterThanOrEqual_Vector(self.noether, other.noether)

    def print(self):
        print("Input function:")
        print("  f = {}".format(self.input))

        print("Evaluated at: ")
        for i in range(self.size):
            print("  x{}={}".format(i, self.inits[i]))

        print("Numeric Value: ")
        print("  f = {}".format(self.val))

        print("Derivates: ")
        for i in range(self.size):
            print("  df/dx{} = {}  ".format(i, self.deriv[i]))


class NoetherAD(Structure):

    def __init__(self, inputs, mode, inits=[], seeds=[]):

        if (not inputs or not inits):
            # if inputs or inits are empty, exit
            print("No input equations or variable values provided.")
            sys.exit(-1)

        self.inputs = inputs
        self.mode = mode
        self.inits = inits 
        self.seeds = seeds
        self.py_objs = []
        self.deriv = []
        self.val = []
        self.jacobian = []


        for i in range(len(inputs)):
            py_noether = NoetherAutoDiff_Vector(inputs[i], mode, inits, seeds)
            self.py_objs.append(py_noether)
            self.deriv.append(py_noether.deriv)
            self.val.append(py_noether.val)

    def get_jacobian(self):
        self.jacobian = []
        for obj in self.py_objs:
            self.jacobian.append(obj.get_jacobian())

        return self.jacobian
        
    def print(self):
        if len(self.inputs) == 1:
            self.py_objs[0].print()
        else:
            for obj in self.py_objs:
                print("-----------------------------------")
                obj.print()

    # Comparison operators
    def __eq__(self, other):
        if (len(self.py_objs) != len(other.py_objs)):
            return False

        matched_set = set()
        for i in range(len(self.py_objs)):            
            for j in range(len(other.py_objs)):
                if (self.py_objs[i] == other.py_objs[j]):
                    matched_set.add(j)
                    break
                
        if (len(matched_set) == len(self.py_objs)):
            return True 
        else: 
            return False

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if (len(self.py_objs) != len(other.py_objs)):
            return False 

        for i in range(len(self.py_objs)):
            for j in range(len(self.py_objs)):
                if not (self.py_objs[i] < other.py_objs[j]):
                    return False

        return True

    def __le__(self, other):
        if (len(self.py_objs) != len(other.py_objs)):
            return False

        for i in range(len(self.py_objs)):
            for j in range(len(self.py_objs)):
                if not (self.py_objs[i] <= other.py_objs[j]):
                    return False

        return True

    def __gt__(self, other):
        if (len(self.py_objs) != len(other.py_objs)):
            return False

        for i in range(len(self.py_objs)):
            for j in range(len(self.py_objs)):
                if not (self.py_objs[i] > other.py_objs[j]):
                    return False

        return True

    def __ge__(self, other):
        if (len(self.py_objs) != len(other.py_objs)):
            return False

        for i in range(len(self.py_objs)):
            for j in range(len(self.py_objs)):
                if not (self.py_objs[i] >= other.py_objs[j]):
                    return False

        return True
        
