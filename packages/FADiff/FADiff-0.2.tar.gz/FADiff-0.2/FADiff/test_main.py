import pytest
import coverage
from FADiff import FADiff
import Elems
import numpy as np
from FuncVect import FuncVect


class TestClass:
    FADiff.set_mode('forward')

    def test_neg(self):
        x = FADiff.new_scal(3)
        assert -x.val == -3
        assert -x.der == -1

    def test_add(self):
        x = FADiff.new_scal(3) + 5
        assert x.val == 8
        assert x.der == 1

        y = FADiff.new_scal(3) + FADiff.new_scal(5)
        assert y.val == 8

    def test_radd(self):
        x = 5 + FADiff.new_scal(3)
        assert x.val == 8
        assert x.der == 1

    def test_sub(self):
        x = FADiff.new_scal(3) - 5
        assert x.val == -2
        assert x.der == 1

        y = FADiff.new_scal(3) - FADiff.new_scal(2)
        assert y.val == 1
        assert x.der == 1

    def test_rsub(self):
        x = 3 - FADiff.new_scal(3)
        assert x.val == 0
        assert x.der == 2

    def test_mul(self):
        x = FADiff.new_scal(3) * 3
        assert x.val == 9
        assert x.der == 3

        y = FADiff.new_scal(3) * FADiff.new_scal(4)
        assert y.val == 12
        # assert y.der == 7

    def test_rmul(self):
        x = 3 * FADiff.new_scal(3)
        assert x.val == 9
        assert x.der == 3

    def test_div(self):
        x = FADiff.new_scal(3) / 3
        assert x.val == 1
        assert x.der == pytest.approx(0.3333333333333333)

        y = FADiff.new_scal(3) / FADiff.new_scal(4)
        assert y.val == pytest.approx(0.75)
        # assert y.der == pytest.approx(0.0625)

    def test_rdiv(self):
        x = 3 / FADiff.new_scal(3)
        assert x.val == 1
        assert x.der == pytest.approx(-0.3333333333333333)

    def test_pow(self):
        x = FADiff.new_scal(3) ** 2
        assert x.val == 9
        assert x.der == 6

        y = FADiff.new_scal(3) ** FADiff.new_scal(5)
        assert y.val == 243
        assert y.der[0] == 405

    def test_rpow(self):
        x = 2 ** FADiff.new_scal(3)
        assert x.val == 8
        assert x.der == pytest.approx(5.54517744)

    assert FADiff._mode == 'forward'
    FADiff.set_mode('reverse')
    assert FADiff._mode == 'reverse'

    def test_neg_reverse(self):
        x = FADiff.new_scal(3)
        assert -x.val == -3
        assert -x.der == -1

    def test_add_reverse(self):
        x = FADiff.new_scal(3) + 5
        assert x.val == 8
        assert x.der == 1

        y = FADiff.new_scal(3) + FADiff.new_scal(5)
        assert y.val == 8

    def test_radd_reverse(self):
        x = 5 + FADiff.new_scal(3)
        assert x.val == 8
        assert x.der == 1

    def test_sub_reverse(self):
        x = FADiff.new_scal(3) - 5
        assert x.val == -2
        assert x.der == 1

        y = FADiff.new_scal(3) - FADiff.new_scal(2)
        assert y.val == 1
        assert x.der == 1

    def test_rsub_reverse(self):
        x = 3 - FADiff.new_scal(3)
        assert x.val == 0
        assert x.der == 2

    def test_mul_reverse(self):
        x = FADiff.new_scal(3) * 3
        assert x.val == 9
        assert x.der == 3

        y = FADiff.new_scal(3) * FADiff.new_scal(4)
        assert y.val == 12
        # assert y.der == 7

    def test_rmul_reverse(self):
        x = 3 * FADiff.new_scal(3)
        assert x.val == 9
        assert x.der == 3

    def test_div_reverse(self):
        x = FADiff.new_scal(3) / 3
        assert x.val == 1
        assert x.der == pytest.approx(0.3333333333333333)

        y = FADiff.new_scal(3) / FADiff.new_scal(4)
        assert y.val == pytest.approx(0.75)
        # assert y.der == pytest.approx(0.0625)

    def test_rdiv_reverse(self):
        x = 3 / FADiff.new_scal(3)
        assert x.val == 1
        assert x.der == pytest.approx(-0.3333333333333333)

    def test_pow_reverse(self):
        x = FADiff.new_scal(3) ** 2
        assert x.val == 9
        assert x.der == 6

        y = FADiff.new_scal(3) ** FADiff.new_scal(5)
        assert y.val == 243
        assert y.der[0] == 405

    def test_rpow_reverse(self):
        x = 2 ** FADiff.new_scal(3)
        assert x.val == 8
        assert x.der == pytest.approx(5.54517744)

    assert FADiff._mode == 'reverse'
    FADiff.set_mode('forward')
    assert FADiff._mode == 'forward'
# Elems testing

    def test_exp(self):
        x = Elems.exp(FADiff.new_scal(3))
        assert x.val == pytest.approx(20.085536923187668)
        assert x.der == pytest.approx(20.085536923187668)

        y = 10
        assert Elems.exp(y) == np.exp(y)

    def test_exp_reverse(self):
        FADiff.set_mode('reverse')
        x = Elems.exp(FADiff.new_scal(3))
        assert x.val == pytest.approx(20.085536923187668)
        assert x.der == pytest.approx(20.085536923187668)

        y = 10
        assert Elems.exp(y) == np.exp(y)

    def test_cos(self):
        FADiff.set_mode('forward')
        x = Elems.cos(FADiff.new_scal(3))
        assert x.val == pytest.approx(-0.9899924966004454)
        assert x.der == pytest.approx(-0.1411200080598672)

        y = 2
        assert Elems.cos(y) == np.cos(y)

    def test_cos_reverse(self):
        FADiff.set_mode('reverse')
        x = Elems.cos(FADiff.new_scal(3))
        assert x.val == pytest.approx(-0.9899924966004454)
        assert x.der == pytest.approx(-0.1411200080598672)

        y = 2
        assert Elems.cos(y) == np.cos(y)

    def test_sin(self):
        x = FADiff()
        x.set_mode('forward')
        x = x.new_scal(3)

        a = Elems.sin(x)
        assert a.val == pytest.approx(0.1411200080598672)
        assert a.der == pytest.approx(-0.9899924966004454)

        y = 2
        assert Elems.sin(y) == np.sin(y)

    def test_sin_reverse(self):
        x = FADiff()
        x.set_mode('reverse')
        x = x.new_scal(3)

        a = Elems.sin(x)
        assert a.val == pytest.approx(0.1411200080598672)
        assert a.der == pytest.approx(-0.9899924966004454)

        y = 2
        assert Elems.sin(y) == np.sin(y)

    def test_tan(self):
        FADiff.set_mode('forward')
        x = Elems.tan(FADiff.new_scal(3))
        assert x.val == pytest.approx(-0.1425465430742778)
        assert x.der == pytest.approx(1.020319516942427)
        y = 2
        assert Elems.tan(y) == np.tan(y)

    def test_tan_reverse(self):
        FADiff.set_mode('reverse')
        x = Elems.tan(FADiff.new_scal(3))
        assert x.val == pytest.approx(-0.1425465430742778)
        assert x.der == pytest.approx(1.020319516942427)
        y = 2
        assert Elems.tan(y) == np.tan(y)

    def test_arcsin(self):
        FADiff.set_mode('forward')
        x = Elems.arcsin(FADiff.new_scal(0.3))
        assert x.val == pytest.approx(0.30469265)
        with pytest.warns(RuntimeWarning):
            Elems.arcsin(-19)

        y = -0.4
        assert Elems.arcsin(y) == np.arcsin(y)

    def test_arcsin_reverse(self):
        FADiff.set_mode('reverse')
        x = Elems.arcsin(FADiff.new_scal(0.3))
        assert x.val == pytest.approx(0.30469265)
        with pytest.warns(RuntimeWarning):
            Elems.arcsin(-19)

        y = -0.4
        assert Elems.arcsin(y) == np.arcsin(y)

    def test_arccos(self):
        FADiff.set_mode('forward')
        x = Elems.arccos(FADiff.new_scal(0.3))
        assert x.val == pytest.approx(1.2661036727794992)
        with pytest.warns(RuntimeWarning):
            Elems.arccos(19)

        y = -0.4
        assert Elems.arccos(y) == np.arccos(y)

    def test_arccos_reverse(self):
        FADiff.set_mode('reverse')
        x = Elems.arccos(FADiff.new_scal(0.3))
        assert x.val == pytest.approx(1.2661036727794992)
        with pytest.warns(RuntimeWarning):
            Elems.arccos(19)

        y = -0.4
        assert Elems.arccos(y) == np.arccos(y)

    def test_arctan(self):
        FADiff.set_mode('forward')
        x = Elems.arctan(FADiff.new_scal(0.5))
        assert x.val == pytest.approx(0.4636476090008061)

        y = -0.4
        assert Elems.arctan(y) == np.arctan(y)

    def test_arctan_reverse(self):
        FADiff.set_mode('reverse')
        x = Elems.arctan(FADiff.new_scal(0.5))
        assert x.val == pytest.approx(0.4636476090008061)

        y = -0.4
        assert Elems.arctan(y) == np.arctan(y)

    def test_sinh(self):
        FADiff.set_mode('forward')
        x = Elems.sinh(FADiff.new_scal(0.4))
        assert x.val == pytest.approx(0.4107523258028155)

        y = -0.4
        assert Elems.sinh(y) == np.sinh(y)

    def test_sinh_reverse(self):
        FADiff.set_mode('reverse')
        x = Elems.sinh(FADiff.new_scal(0.4))
        assert x.val == pytest.approx(0.4107523258028155)

        y = -0.4
        assert Elems.sinh(y) == np.sinh(y)

    def test_cosh(self):
        FADiff.set_mode('forward')

        x = Elems.cosh(FADiff.new_scal(0.3))
        assert x.val == pytest.approx(1.04533851)
        assert x.der == pytest.approx(0.30452029)

        y = 4
        assert Elems.cosh(y) == np.cosh(y)

    def test_cosh_reverse(self):
        FADiff.set_mode('reverse')

        x = Elems.cosh(FADiff.new_scal(0.3))
        assert x.val == pytest.approx(1.04533851)
        assert x.der == pytest.approx(0.30452029)

        y = 4
        assert Elems.cosh(y) == np.cosh(y)

    def test_tanh(self):
        FADiff.set_mode('forward')
        x = Elems.tanh(FADiff.new_scal(1))
        assert x.val == pytest.approx(0.7615941559557649)

        y = 2
        assert Elems.tanh(y) == np.tanh(y)

    def test_tanh_reverse(self):
        FADiff.set_mode('reverse')
        x = Elems.tanh(FADiff.new_scal(1))
        assert x.val == pytest.approx(0.7615941559557649)

        y = 2
        assert Elems.tanh(y) == np.tanh(y)

    def test_log(self):
        FADiff.set_mode('forward')
        x = Elems.log(FADiff.new_scal(0.3))
        assert x.val == pytest.approx(-1.2039728)

        y = 2
        assert Elems.log(y) == pytest.approx(np.log(y) / np.log(np.e))

    def test_log_reverse(self):
        FADiff.set_mode('reverse')
        x = Elems.log(FADiff.new_scal(0.3))
        assert x.val == pytest.approx(-1.2039728)

        y = 2
        assert Elems.log(y) == pytest.approx(np.log(y) / np.log(np.e))

    def test_logistic(self):
        FADiff.set_mode('forward')
        x = FADiff()
        x = x.new_scal(2)
        x = Elems.logistic(x)
        assert x.val == pytest.approx(0.8807970779778823)

        y = 4
        assert Elems.logistic(y) == pytest.approx(0.9820137900379085)

    def test_logistic_reverse(self):
        FADiff.set_mode('reverse')
        x = FADiff()
        x = x.new_scal(2)
        x = Elems.logistic(x)
        assert x.val == pytest.approx(0.8807970779778823)
        y = 4
        assert Elems.logistic(y) == pytest.approx(0.9820137900379085)

    def test_sqrt(self):
        FADiff.set_mode('forward')
        x = Elems.sqrt(FADiff.new_scal(3))
        assert x.val == pytest.approx(1.7320508075688772)

        y = 2
        assert Elems.sqrt(y) == np.sqrt(y)

        z = Elems.sqrt(FADiff.new_scal(-1))
        with pytest.raises(AssertionError):
            assert z.val == 1

    def test_sqrt_reverse(self):
        FADiff.set_mode('reverse')
        x = Elems.sqrt(FADiff.new_scal(3))
        assert x.val == pytest.approx(1.7320508075688772)

        y = 2
        assert Elems.sqrt(y) == np.sqrt(y)

        z = Elems.sqrt(FADiff.new_scal(-1))
        with pytest.raises(AssertionError):
            assert z.val == 1

    # FADiff class
    def test_mode(self):
        x = FADiff()
        x.set_mode('forward')
        assert x._mode == 'forward'
        x.new_scal(3)
        assert x._mode == 'forward'
        x.set_mode('reverse')
        assert x._mode == 'reverse'
        x.new_scal(4)
        x.set_mode('testing')
        assert x._mode != 'forward' or x._mode != 'reverse'

        y = FADiff()
        y.set_mode('forward')
        assert y._mode == 'forward'
        y = y.new_vect(np.array([2, 3, 4]))
        assert y.der is not None

        z = FADiff()
        z.set_mode('reverse')

        z = z.new_vect(np.array([1, 2, 3]))
        assert FADiff._mode == 'reverse'

    # FuncVect class

    def test_funcvect(self):

        # forward mode scalar tests
        x = FADiff()
        x.set_mode('forward')

        x = FADiff.new_scal(3)
        y = FADiff.new_scal(2)
        f1 = x * y + x
        assert f1.val == 9
        f2 = 8 * y
        assert f2.val == 16

        f = FADiff.new_funcvect([f1, f2])
        assert f.val.tolist() == [9, 16]
        assert f.der.tolist() == [[3, 3], [0, 8]]

        # forward mode vector tests
        x1 = FADiff.new_vect(np.array([2, 3, 4]))
        f3 = x1 * x1
        f4 = x1 * 8
        ff = FADiff.new_funcvect([f3, f4])

        assert ff.val.tolist() == [[4, 9, 16], [16, 24, 32]]
        assert ff.der.tolist() == [[4, 6, 8], [8, 8, 8]]

        # test fucntions of dif types
        with pytest.raises(Exception):
            ff = FADiff.new_funcvect([f3, 17])
        # reverse mode scalar tests
        xr = FADiff()
        xr.set_mode('reverse')

        xr = FADiff.new_scal(3)
        yr = FADiff.new_scal(2)
        f1r = xr * yr + xr
        assert f1r.val == 9
        f2r = 8 * yr
        assert f2r.val == 16

        fr = FADiff.new_funcvect([f1r, f2r])
        assert fr.val.tolist() == [9, 16]
        assert fr.der.tolist() == [[3, 3], [0, 8]]

        # reverse mode vector tests
        x1r = FADiff.new_vect(np.array([2, 3, 4]))
        f3r = x1r * x1r
        f4r = x1r * 8
        ffr = FADiff.new_funcvect([f3r, f4r])

        assert ffr.val.tolist() == [[4, 9, 16], [16, 24, 32]]
        assert ffr.der.tolist() == [[4, 6, 8], [8, 8, 8]]

        # test fucntions of dif types
        with pytest.raises(Exception):
            ffr = FADiff.new_funcvect([f3r, 17])

