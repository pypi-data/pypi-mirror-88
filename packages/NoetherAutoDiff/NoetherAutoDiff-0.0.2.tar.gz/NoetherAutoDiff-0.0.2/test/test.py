
import pytest

from NoetherAutoDiff import *


class TestNoetherAD:
    def test_one(self):
        assert "h" in "this"

    def test_two(self):
        assert 1 == 1


    # # Example code on how to use NoetherAD
    # print("-------- Test NoetherAutoDiff ----------------------")
    # nad0 = NoetherAutoDiff("sin(x)^cos(x-5/3+4^x*y/z)/tan(3*x)+exp(3*x-1)", 0,
    #                        {'x': 1.4, 'y': 2.4, 'z': 3.4},
    #                        {'x': 1, 'y': 1, 'z': 1})
    # nad0.print()

    # nad1 = NoetherAutoDiff(
    #     "2*x + 3*y", 0, {'x': 2.3, 'y': 3.5}, {'x': 1.0, 'y': 1.0})
    # nad1.print()

    # nad2 = NoetherAutoDiff("2.5 * x - 3.5 * y + 1.25 * z", 0, {'x': 2, 'y': 2, 'z': 2},
    #                        {'x': 1, 'y': 1, 'z': 1})
    # nad2.print()

    # print(nad1 == nad0)
    # print(nad0 == nad0)
    # print(nad1 >= nad2)
    # print(nad1 <= nad2)

    # print("---------- Test NoetherAutoDiff_Vector ----------------------")
    # nadV0 = NoetherAutoDiff_Vector("sin(x0)^cos(x0-5/3+4^x0*x1/x2)/tan(3*x0)+exp(3*x0-1)", 0,
    #                                [1.4, 2.4, 3.4], [1, 1, 1])
    # nadV0.print()

    # nadV1 = NoetherAutoDiff_Vector(
    #     "2.5 * x0 - 3.5 * x1 + 1.25 * x2", 0, [2, 2, 2], [1, 1, 1])
    # nadV1.print()

    # nadV2 = NoetherAutoDiff_Vector("x0 + sin(3*x1)", 0, [10, 10], [1.0, 1.0])
    # nadV2.print()

    # print(nadV2 == nadV0)
    # print(nadV2 == nadV2)
    # print(nadV1 >= nadV2)
    # print(nadV1 <= nadV2)

    # print("------------ Test NoetherAD ----------------")
    # nad_v = NoetherAD(["2.5 * x0 - 3.5 * x1 + 1.25 * x2",
    #                    "10*x0 + 5*x1 + 2*x2"], 0, [2, 2, 2], [1, 1, 1])
    # nad_v.print()

    # print(nad_v == nad_v)

    # print("-- end --")
