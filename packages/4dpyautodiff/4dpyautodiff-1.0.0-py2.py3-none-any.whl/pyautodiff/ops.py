import math
from collections import defaultdict
from functools import wraps

import numpy as np

from pyautodiff import Var, Mode


def _dunder_wrapper(fn, is_unary=False):
    """
    A wrapper function to bridge dunder method and classmethod (operation).
    For example, Var.__add__ = dunder_wrapper(VarAdd.binary_operation).
    Or Var.__add__ = lambda a, b: VarAdd.binary_operation(a, b)
    Args:
        fn: operation function
        is_unary: Defaults to False for binary operations like Add, Substract; True for unary operations like abs, exp.

    Returns:
        The wrapped function.
    """

    @wraps(fn)
    def wrapper(*args):
        a = args[0]
        if is_unary:
            return fn(a)

        b = args[1]
        return fn(a, b)

    return wrapper


class Ops:
    """
    A template class for all operations for class `Var` (i.e. unary and binary operations).
    For each operation, users MUST implement (at least) two functions: `op()` and `local_derivative()`.
    Non-element-wise operations should re-write some more methods. See 'VarTranspose' and 'VarMatMul' as reference.
    Then the propagation for forward/reverse/mix mode will be auto handled by the pipeline, which locate in
    `binary_operation()` and `unary_operation()`.
    """

    # Unary operation: 1 (by default)
    # Binary operaton: 2 (customized)
    n_operands = 1

    # A string to be displayed in computational graph.
    # If None, suffix of class name will be used.
    # For example, exp (operation) will show `Exp` since its class name is `VarExp` in the plot.
    # See ../visualization.py for its usage.
    symbol = None

    @classmethod
    def op(cls, va, vb):
        """
        Implement the numerical value operation in this function.
        For unary operation: vc = f(va), return vc;
        For binary operation: vc = va op vb, return vc;
        To be implemented by each operation.
        Args:
            va: numerical value of operand a (a.val, a is a Var instance);
            vb: numerical value of operand b (b.val, b is a Var instance);

        Returns:
            A Number or np.ndarray, the numerical value of this operation
        """

        raise NotImplementedError

    @classmethod
    def local_derivative(cls, va, vb, vc, skip_lda=False, skip_ldb=False):
        """
        Calculate the derivative for every elementary operations.
        For unary operation: c = f(a), return the local partial derivative: df/da;
        For binary operation: c = a op b, return the local partial derivatives df/da, df/db;
        (a,b could be results of some operations)
        For example,

            x = Var(1, 'x')
            a = x + 1
            b = 2 - x
            c = a * b

        The local derivative dc/da = 1, dc/db = 2;
        The target derivative dc/dx = dc/da*da/dx + dc/db*db/dx = 1*1 + 2*(-1) = -1

        Args:
            va: numerical value of operand (a Var instance) a (=a.val);
            vb: numerical value of operand (a Var instance) b (=b.val);
            vc: numerical value of operation result (a Var instance) c (=c.val);
            skip_lda: If a is a constant, no need to calculate dc/da
            skip_ldb: If b is a constant, no need to calculate dc/db
        Returns:
            A Number or np.ndarray for unary operation;
            A list of two Numbers or np.ndarrays for binary operation;

        """
        raise NotImplementedError

    @classmethod
    def chain_rule(cls, lda, da, ldb, db, forward_mode=True):
        """
        Apply chain rule in forward mode.
        For composite function: c = g(f(a, b)), dg/dx = dg/df*df/dx; dg/dy = dg/df*df/dy;
        Args:
            lda: A Number or np.ndarray, represents the local derivative: dc/da
            da: a dict stores the derivative of a.
                For example, {'x': da/dx, 'y': da/dy}, where `x`,'y' is the involved variables.
            ldb: A Number or np.ndarray, represents the local derivative: dc/db
            db: a dict stores the derivative of b.
                For example, {'x': db/dx, 'y': db/dy}, where `x`,'y' is the involved variables.
            forward_mode: defaults to True; False for reverse or mix mode.
        Returns:
            A dict stores the derivative of c by applying the chain rule. For example,
            {'x': dc/dx, 'y': dc/dy} where `x`,'y' are the target variables.

        """

        einsum_dispatcher = "ijkl,ij->ijkl" if forward_mode else "ijkl,kl->ijkl"

        def _apply(d, ld):
            if d is None:
                return

            ndim = np.ndim(ld)
            if ndim == 0:
                fn = lambda tot, loc: tot * loc
            elif ndim == 2:
                fn = lambda tot, loc: np.einsum(einsum_dispatcher, tot, loc)
            else:
                raise TypeError(f"Local derivative only supports scalar or 2D matrix but not {np.shape(ld)}")

            for wrt in d:
                dc[wrt] += fn(d[wrt], ld)

        dc = defaultdict(int)
        _apply(da, lda)
        _apply(db, ldb)

        return dict(dc)

    @classmethod
    def merge_var_shapes(cls, sa, sb=None):
        """
        Propagate the _var_shapes to the operation result by synthesizing the _var_shapes of a and b.
        BE CAREFUL, a _var_shapes (dict) instance can be shared across multiple var instances.
        Don't use _var_shapes for any instance specific calculation.
        Args:
            sa: _var_shapes of the first operand
            sb: _var_shapes of the second operand, could be None

        Returns:
            a dict, the merged _var_shapes
        """
        if sb is None:
            return sa

        if sa is None:
            return sb

        sa.update(sb)
        return sa

    @classmethod
    def merge_modes(cls, ma, mb=None):
        """
        Merge mode by such rules:
        1. Forward op reverse/mix --> mix
        2. Forward op forward/NONE --> forward
        3. Reverse op reverse/NONE --> reverse
        4. Reverse/mix/NONE op mix --> mix
        5. NONE op NONE --> NONE
        Args:
            ma: a.mode
            mb: b.mode

        Returns:
            A mode value

        """
        if mb is None or mb == Mode.NONE:
            return ma

        if ma == Mode.NONE:
            return mb

        if ma != mb:
            return Mode.Mix

        return ma

    @classmethod
    def fwdprop(cls, a, b, val):
        """
        Propagation for forward mode. Suppose current operation : c = a op b is one step of f(x), by chain rule,
        we have: dc/dx = dc/da * da/dx + dc/db * db/dx, return dc/dx.
        Args:
            a: the first operand, a Var instance
            b: the second operand, a Var instance, could be None
            val: the numerical operation result

        Returns:
            a dict, the derivative of operation result instance
        """
        if cls.n_operands == 2:
            lda, ldb = cls.local_derivative(a.val, b.val, val,
                                            skip_lda=a.is_const,
                                            skip_ldb=b.is_const)

            return cls.chain_rule(lda, a.derivative, ldb, b.derivative)

        lda = cls.local_derivative(a.val, None, val)
        return cls.chain_rule(lda, a.derivative, None, None)

    @classmethod
    def backprop(cls, a, b, val, dfdc):
        """
        Propagation for reverse/mix mode. Suppose current operation : c = a op b is one step of f(x), by chain rule,
        we have: df/da = df/dc * dc/da, df/db = df/dc * dc/db.
        Args:
            a: the first operand, a Var instance
            b: the second operand, a Var instance, could be None
            val: the numerical operation result
            dfdc: the backprop gradient.

        Returns:
            None
        """
        if cls.n_operands == 2:
            lda, ldb = cls.local_derivative(a.val, b.val, val,
                                            skip_lda=a.is_const,
                                            skip_ldb=b.is_const)
            a._bpgrad.update(cls.chain_rule(lda, dfdc, None, None, False))
            b._bpgrad.update(cls.chain_rule(None, None, ldb, dfdc, False))

        else:
            lda = cls.local_derivative(a.val, None, val)
            a._bpgrad.update(cls.chain_rule(lda, dfdc, None, None, False))

    @classmethod
    def merge_fwd_backprop(cls, dcdxs, dfdc):
        """
        Merge derivatives from forward mode and reverse mode. Suppose current node is c, in mix mode. W.r.t x, we have
        dc/dx and df/dc, then PART of df/dx is df/dc * dc/dx.
        Args:
            dcdxs: a dict like {'x': dcdx, 'y': dcdy}
            dfdc: a dict like {f: dfdc}

        Returns:
            a dict like {'x': dfdc (part), 'y': dfdy (part)}
        """
        dfdxs = {}
        for wrt in dcdxs:
            dfdxs[wrt] = np.einsum("ijpq, klij->klpq", dcdxs[wrt], dfdc)

        return dfdxs

    @classmethod
    def binary_operation(cls, a, b):
        """
        A universal binary operation process. Newly defined operations (class) do not need to re-write it.
        Args:
            a: a Number of np.ndarray or `Var` instance, the first operand of the calculation
            b: a Number of np.ndarray or `Var` instance , the second operand of the calculation

        Returns:
            A `Var` instance whose `.val` is the numerical value of the operation and `.derivative` containing
            the derivative w.r.t. the involved variables.

        """

        if not isinstance(a, Var):
            a = Var(a)

        if not isinstance(b, Var):
            b = Var(b)

        # Stop numpy auto broadcasting but allow the operation between scalar and vector,
        # or the differentiation would be too complicated to deal with
        if np.ndim(a.val) > 0 and np.ndim(b.val) > 0 and cls.__name__ != "VarMatMul":
            assert a.val.shape == b.val.shape, f"Shapes mismatch: {a.val.shape} != {b.val.shape}"

        # S1: calculate numerical result
        val = cls.op(a.val, b.val)

        # S2: get mode of the result
        mode = cls.merge_modes(a.mode, b.mode)

        # Prepare params for constructing a Var instance to contain the operation result
        params = dict(derivative={},
                      _var_shapes=cls.merge_var_shapes(a._var_shapes, b._var_shapes),
                      mode=mode,
                      _context=[cls, [a, b]])

        # Reverse/mix mode vars will calculate derivative later (when .diff() is called)
        if mode not in (Mode.Forward, Mode.NONE):
            return Var(val, **params)

        params["derivative"] = cls.fwdprop(a, b, val)
        return Var(val, **params)

    @classmethod
    def unary_operation(cls, a):
        """
        A universal unary operation process. Newly defined operations (class) do not need to re-write it.

        Args:
            a: a Number of np.ndarray or `Var` instance, the first operand of the calculation

        Returns:
            A `Var` instance whose `.val` is the numerical value of the operation and `.derivative` containing
            the derivative w.r.t. the involved variables.
        """
        if not isinstance(a, Var):
            a = Var(a)

        # S1: calculate numerical result
        val = cls.op(a.val, None)
        # S2: inherit the mode for the result
        mode = a.mode
        # Prepare params for constructing a Var instance to contain the operation result
        params = dict(derivative={},
                      _var_shapes=cls.merge_var_shapes(a._var_shapes),
                      mode=mode,
                      _context=[cls, [a]])

        if mode not in (Mode.Forward, Mode.NONE):
            return Var(val, **params)

        params["derivative"] = cls.fwdprop(a, None, val)
        return Var(val, **params)


class VarNeg(Ops):
    """
    A class for negative constants. Gives the value and local derivative.
    This class inherits from the Ops Class.
    To use:
    >>> -Var(1, 'x')
    (<class 'pyautodiff.var.Var'> name: None val: -1, der: {'x': array([[[[-1.]]]])})
    """

    symbol = "-"

    @classmethod
    def op(cls, va, vb):
        return -va

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        return -1


class VarPos(Ops):
    """
    A class for positive constants. Gives the value and local derivative.        
    This class inherits from the Ops Class.
    >>> +Var(1, 'x')
    (<class 'pyautodiff.var.Var'> name: None val: 1, der: {'x': array([[[[1.]]]])})
    """

    symbol = "+"

    @classmethod
    def op(cls, va, vb):
        return va

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        return 1


class VarAbs(Ops):
    """
    A class for absolute values. Gives the value and local derivative. 
    This class inherits from the Ops Class.
    >>> abs(Var(1, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 1, der: {'x': array([[[[1.]]]])})
    """

    @classmethod
    def op(cls, va, vb):
        return abs(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        d = np.ones_like(va)
        d[va < 0] = -1

        try:
            # scalar
            return d.item()
        except:
            return d


class VarAdd(Ops):
    """
    A class for addition. Gives the value and local derivative.
    This class inherits from the Ops Class.
    >>> Var(1, 'x') + 1
    (<class 'pyautodiff.var.Var'> name: None val: 2, der: {'x': array([[[[1.]]]])})
    >>> Var(1, 'x') + Var(2, 'y')
    (<class 'pyautodiff.var.Var'> name: None val: 3, der: {'x': array([[[[1.]]]]), 'y': array([[[[1.]]]])})
    """

    n_operands = 2
    symbol = "+"

    @classmethod
    def op(cls, va, vb):
        return va + vb

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        return 1, 1


class VarSub(Ops):
    """
    A class for addition. Gives the value and local derivative.
    This class inherits from the Ops Class.
    >>> Var(1, 'x') - 1
    (<class 'pyautodiff.var.Var'> name: None val: 0, der: {'x': array([[[[1.]]]])})
    >>> Var(1, 'x') - Var(2, 'y')
    (<class 'pyautodiff.var.Var'> name: None val: -1, der: {'x': array([[[[1.]]]]), 'y': array([[[[-1.]]]])})
    """

    n_operands = 2
    symbol = "-"

    @classmethod
    def op(cls, va, vb):
        return va - vb

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        return 1, -1


class VarMul(Ops):
    """
    A class for multiplication. Gives the value and local derivative.
    This class inherits from the Ops Class.
    >>> Var(1, 'x') * 2
    (<class 'pyautodiff.var.Var'> name: None val: 2, der: {'x': array([[[[2.]]]])})
    >>> Var(1, 'x') * Var(2, 'y')
    (<class 'pyautodiff.var.Var'> name: None val: 2, der: {'x': array([[[[2.]]]]), 'y': array([[[[1.]]]])})
    """

    n_operands = 2
    symbol = "*"

    @classmethod
    def op(cls, va, vb):
        return va * vb

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        return vb, va


class VarTrueDiv(Ops):
    """
    A class for division. Gives the value and local derivative.     
    This class inherits from the Ops Class.
    >>> Var(4, 'x') / 2
    (<class 'pyautodiff.var.Var'> name: None val: 2.0, der: {'x': array([[[[0.5]]]])})
    >>> Var(4, 'x') / Var(2, 'y')
    (<class 'pyautodiff.var.Var'> name: None val: 2.0, der: {'x': array([[[[0.5]]]]), 'y': array([[[[-1.]]]])})
    """

    n_operands = 2
    symbol = "/"

    @classmethod
    def op(cls, va, vb):
        return va / vb

    @classmethod
    def local_derivative(cls, va, vb, vc, skip_lda=False, skip_ldb=False):
        if skip_ldb:
            return 1 / vb, 0

        if skip_lda:
            return 0, -vc / vb

        return 1 / vb, -vc / vb


class VarPow(Ops):
    """
    A class for power operation. Gives the value and local derivative.    
    This class inherits from the Ops Class.
    >>> Var(2, 'x') ** 2
    (<class 'pyautodiff.var.Var'> name: None val: 4, der: {'x': array([[[[4.]]]])})
    >>> Var(4, 'x') ** Var(2, 'y')
    (<class 'pyautodiff.var.Var'> name: None val: 16, der: {'x': array([[[[8.]]]]), 'y': array([[[[22.18070978]]]])})
    """

    n_operands = 2
    symbol = "power"

    @classmethod
    def op(cls, va, vb):
        return va ** vb

    @classmethod
    def local_derivative(cls, va, vb, vc, skip_lda=False, skip_ldb=False):
        """ derivative of w.r.t vb and vb: b * a^(b-1)*a', a^b*ln(a)*b' """

        if skip_ldb:
            return vb * (va ** (vb - 1)), 0

        if skip_lda:
            return 0, np.log(va) * vc

        return vb * (va ** (vb - 1)), np.log(va) * vc


class VarExp(Ops):
    """
    A class for exponential operation. Gives the value and local derivative.
    This class inherits from the Ops Class.
    >>> exp(Var(0, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 1.0, der: {'x': array([[[[1.]]]])})
    """

    @classmethod
    def op(cls, va, vb):
        return np.exp(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, **kwargs):
        """ c = e^a --> c' = e^a"""
        return vc


class VarLog(Ops):
    """
    A class for logarithm. Gives the value and local derivative.
    This class inherits from the Ops Class.
    >>> log(Var(1, 'x'))
    (<class 'pyautodiff.var.Var'> name: None val: 0.0, der: {'x': array([[[[1.]]]])})
    """

    n_operands = 2

    @classmethod
    def op(cls, va, vb):
        """ log_vb(va) """
        return np.log(va) / np.log(vb)
        # return np.log(va)

    @classmethod
    def local_derivative(cls, va, vb, vc, skip_lda=False, skip_ldb=False):
        """ c'=a'/(a*ln(b)), c' = -(b'*log(a))/(b*log^2(b))) """
        inv_log_vb = 1 / np.log(vb)

        if skip_ldb:
            return 1 / va * inv_log_vb, 0

        if skip_lda:
            return 0, -vc * inv_log_vb / vb

        return 1 / va * inv_log_vb, -vc * inv_log_vb / vb

    @classmethod
    def binary_operation_with_base(clf, a, base=math.e):
        """ Wrap function to explicitly specify base """
        return clf.binary_operation(a, base)


class VarLogistic(Ops):
    """
    Logistic function: f(x) = 1 / (1 + exp(x))
    >>> sigmoid((Var(0, 'x')))
    (<class 'pyautodiff.var.Var'> name: None val: 0.5, der: {'x': array([[[[0.25]]]])})
    """

    @classmethod
    def op(cls, va, vb):
        return 1 / (1 + np.exp(-va))

    @classmethod
    def local_derivative(cls, va, vb, vc, skip_lda=False, skip_ldb=False):
        return vc * (1 - vc)


class VarMatMul(Ops):
    """
    Matrix multiplication.
    >>> (Var(np.array([[1],[2]]), 'x') @ Var(np.array([[0,1]]), 'y')).val.tolist()
    [[0, 1], [0, 2]]
    """
    n_operands = 2
    symbol = "@"

    @classmethod
    def op(cls, va, vb):
        return va @ vb

    @classmethod
    def local_derivative(cls, va, vb, vc, skip_lda=False, skip_ldb=False):
        return vb, va

    @classmethod
    def chain_rule(cls, lda, da, ldb, db, forward_mode=True):
        """
        Apply chain rule in forward mode for Matmul: c = a@b
        Args:
            lda: A Number or np.ndarray, represents the local derivative: dc/da (b.val in this case)
            da: a dict stores the derivative of a.
                For example, {'x': da/dx, 'y': da/dy}, where `x`,'y' is the involved variables.
            ldb: A Number or np.ndarray, represents the local derivative: dc/db (a.val in this case)
            db: a dict stores the derivative of b.
                For example, {'x': db/dx, 'y': db/dy}, where `x`,'y' is the involved variables.

        Returns:
            A dict stores the derivative of c by applying the chain rule. For example,
            {'x': dc/dx, 'y': dc/dy} where `x`,'y' is the involved variables.

        """

        def _apply(d, ld, s):
            if d is None:
                return

            for wrt in d:
                dc[wrt] += np.einsum(s, d[wrt], ld)

        dc = defaultdict(int)
        _apply(da, lda, "pqkl,qr->prkl" if forward_mode else "mnpr,qr->mnpq")
        _apply(db, ldb, "qrkl,pq->prkl" if forward_mode else "mnpr,pq->mnqr")

        return dict(dc)


class VarTranspose(Ops):
    """
    Transpose matrix.
    >>> (Var(np.array([[1,2]]), 'x').T).val.tolist()
    [[1], [2]]
    """
    symbol = ".T"

    @classmethod
    def op(cls, va, vb):
        return np.transpose(va)

    @classmethod
    def fwdprop(cls, a, b, val):
        der = {}
        for wrt in a.derivative:
            der[wrt] = np.einsum('ijkl->jikl', a.derivative[wrt])

        return der

    @classmethod
    def backprop(cls, a, b, val, dfdc):
        bp = {}
        for wrt in dfdc:
            bp[wrt] = np.einsum('ijkl->ijlk', dfdc[wrt])

        a._bpgrad.update(bp)

    @classmethod
    def unary_operation(cls, a):
        """
        A universal unary operation process. Newly defined operations (class) do not need to re-write it.

        Args:
            a: a Number of np.ndarray or `Var` instance, the first operand of the calculation

        Returns:
            A `Var` instance whose `.val` is the numerical value of the operation and `.derivative` containing
            the derivative w.r.t. the involved variables.
        """
        if not isinstance(a, Var):
            a = Var(a)

        val = cls.op(a.val, None)

        mode = a.mode
        params = dict(derivative={},
                      _var_shapes=cls.merge_var_shapes(a._var_shapes),
                      mode=mode,
                      _context=[cls, [a]])

        if mode not in (Mode.Forward, Mode.NONE):
            return Var(val, **params)

        params["derivative"] = cls.fwdprop(a, None, val)
        return Var(val, **params)


Var.__neg__ = _dunder_wrapper(VarNeg.unary_operation, True)
Var.__pos__ = _dunder_wrapper(VarPos.unary_operation, True)
Var.__abs__ = _dunder_wrapper(VarAbs.unary_operation, True)

# +=, -=, *=, /= are auto enabled.

Var.__radd__ = Var.__add__ = _dunder_wrapper(VarAdd.binary_operation)
Var.__sub__ = _dunder_wrapper(VarSub.binary_operation)
Var.__rsub__ = lambda a, b: VarSub.binary_operation(b, a)
Var.__rmul__ = Var.__mul__ = _dunder_wrapper(VarMul.binary_operation)
Var.__truediv__ = _dunder_wrapper(VarTrueDiv.binary_operation)
Var.__rtruediv__ = lambda a, b: VarTrueDiv.binary_operation(b, a)

Var.__pow__ = _dunder_wrapper(VarPow.binary_operation)
Var.__rpow__ = lambda a, b: VarPow.binary_operation(b, a)
pow = VarPow.binary_operation

# TODO: Fan
Var.__matmul__ = _dunder_wrapper(VarMatMul.binary_operation)
Var.transpose = transpose = _dunder_wrapper(VarTranspose.unary_operation, True)

exp = VarExp.unary_operation  # enable exp(x)
Var.exp = _dunder_wrapper(exp, True)  # enable x.exp()

log = VarLog.binary_operation_with_base
Var.log = _dunder_wrapper(log)

logistic = sigmoid = VarLogistic.unary_operation
Var.sigmoid = _dunder_wrapper(sigmoid, True)

sqrt = lambda x: x ** 0.5
Var.sqrt = sqrt
