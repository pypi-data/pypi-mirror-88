import numpy as np

from pyautodiff import Var, Ops
from pyautodiff.ops import _dunder_wrapper


class VarSin(Ops):
    """
        A class for trigonometric sine operation. Gives the value and local derivative.

        This class inherits from the Ops Class.

    >>> sin(Var(0, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 0.0, der: {'x': array([[[[1.]]]])})
    """

    @classmethod
    def op(cls, va, vb):
        return np.sin(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        return np.cos(va)


class VarCos(Ops):
    """
        A class for trigonometric cosine operation. Gives the value and local derivative.
        
        This class inherits from the Ops Class.

    >>> cos(Var(0, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 1.0, der: {'x': array([[[[0.]]]])})
    """

    @classmethod
    def op(cls, va, vb):
        return np.cos(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        return -np.sin(va)


class VarTan(Ops):
    """
        A class for trigonometric tangent operation. Gives the value and local derivative.
        
        This class inherits from the Ops Class.

    >>> tan(Var(0, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 0.0, der: {'x': array([[[[1.]]]])})

    """

    @classmethod
    def op(cls, va, vb):
        return np.tan(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        return (1 / np.cos(va)) ** 2


class VarArcSin(Ops):
    """
        A class for trigonometric arcsine operation. Gives the value and local derivative.
        
        This class inherits from the Ops Class.

    >>> arcsin(Var(0, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 0.0, der: {'x': array([[[[1.]]]])})

    """

    @classmethod
    def op(cls, va, vb):
        return np.arcsin(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        return 1 / np.sqrt(1 - va ** 2)


class VarArcCos(Ops):
    """
        A class for trigonometric arccosine operation. Gives the value and local derivative.
        
        This class inherits from the Ops Class.

    >>> arccos(Var(0, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 1.5707963267948966, der: {'x': array([[[[-1.]]]])})
    """

    @classmethod
    def op(cls, va, vb):
        return np.arccos(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        return -1 / np.sqrt(1 - va ** 2)


class VarArcTan(Ops):
    """
        A class for trigonometric arctangent operation. Gives the value and local derivative.
        
        This class inherits from the Ops Class.

    >>> arctan(Var(0, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 0.0, der: {'x': array([[[[1.]]]])})
    """

    @classmethod
    def op(cls, va, vb):
        return np.arctan(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        return 1 / (1 + va ** 2)


class VarSinH(Ops):
    """
        A class for trigonometric hyperbolic sine operation. Gives the value and local derivative.
        
        This class inherits from the Ops Class.

    >>> arcsinh(Var(0, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 0.0, der: {'x': array([[[[1.]]]])})
    """

    @classmethod
    def op(cls, va, vb):
        return np.sinh(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        """ derivative of sinh(x) = cosh(x)"""
        return np.cosh(va)


class VarCosH(Ops):
    """
        A class for trigonometric hyperbolic cosine operation. Gives the value and local derivative.
        
        This class inherits from the Ops Class.

    >>> arccosh(Var(2, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 1.3169578969248166, der: {'x': array([[[[0.57735027]]]])})
    """

    @classmethod
    def op(cls, va, vb):
        return np.cosh(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        """ derivative of cosh(x) = sinh(x)"""
        return np.sinh(va)


class VarTanH(Ops):
    """
        A class for trigonometric hyperbolic tangent operation. Gives the value and local derivative.
        
        This class inherits from the Ops Class.

    >>> tanh(Var(1, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 0.7615941559557649, der: {'x': array([[[[0.41997434]]]])})
    """

    @classmethod
    def op(cls, va, vb):
        return np.tanh(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        """ derivative of tanh(x) = 1 - tanh(x)^2

        Args:
            **kwargs:
        """
        return 1 - np.tanh(va) ** 2


class VarArcSinH(Ops):
    """
        A class for trigonometric hyperbolic arcsine operation. Gives the value and local derivative.
        
        This class inherits from the Ops Class.

    >>> arcsinh(Var(0, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 0.0, der: {'x': array([[[[1.]]]])})

    """

    @classmethod
    def op(cls, va, vb):
        return np.arcsinh(va)

    @classmethod
    def local_derivative(cls, va, vb, vc):
        """ for all real va """
        return 1 / np.sqrt((va ** 2) + 1)


class VarArcCosH(Ops):
    """
        A class for trigonometric hyperbolic arccosine operation. Gives the value and local derivative.
        
        This class inherits from the Ops Class.

    >>> arccosh(Var(2, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 1.3169578969248166, der: {'x': array([[[[0.57735027]]]])})

    """

    @classmethod
    def op(cls, va, vb):
        return np.arccosh(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        """ for all real va>1

        Args:
            **kwargs:
        """
        assert (va > 1), "va should be greater than 1."
        return 1 / np.sqrt((va ** 2) - 1)


class VarArcTanH(Ops):
    """
        A class for trigonometric hyperbolic arctan operation. Gives the value and local derivative.
        
        This class inherits from the Ops Class.

    >>> arctanh(Var(0, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 0.0, der: {'x': array([[[[1.]]]])})

    """

    @classmethod
    def op(cls, va, vb):
        """ the domain of arctanh is (-1, 1) """
        assert (np.abs(va) < 1), "The value inside arctanh should be between (-1, 1)."

        return np.arctanh(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        """ derivative of arctanh(x) = 1 / (1-x^2)

        Args:
            **kwargs:
        """
        return 1 / (1 - va ** 2)


sin = VarSin.unary_operation  # enable sin(x)
Var.sin = _dunder_wrapper(sin, True)  # enable x.sin()

arcsin = VarArcSin.unary_operation
Var.arcsin = _dunder_wrapper(arcsin, True)

cos = VarCos.unary_operation
Var.cos = _dunder_wrapper(cos, True)

arccos = VarArcCos.unary_operation
Var.arccos = _dunder_wrapper(arccos, True)

tan = VarTan.unary_operation
Var.tan = _dunder_wrapper(tan, True)

arctan = VarArcTan.unary_operation
Var.arctan = _dunder_wrapper(arctan, True)

sinh = VarSinH.unary_operation
Var.sinh = _dunder_wrapper(sinh, True)

arcsinh = VarArcSinH.unary_operation
Var.arcsinh = _dunder_wrapper(arcsinh, True)

cosh = VarCosH.unary_operation
Var.cosh = _dunder_wrapper(cosh, True)

arccosh = VarArcCosH.unary_operation
Var.arccosh = _dunder_wrapper(arccosh, True)

tanh = VarTanH.unary_operation
Var.tanh = _dunder_wrapper(tanh, True)

arctanh = VarArcTanH.unary_operation
Var.arctanh = _dunder_wrapper(arctanh, True)
