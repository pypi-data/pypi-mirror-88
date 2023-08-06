from enum import Enum
from collections import deque, defaultdict, Counter
import time
from numbers import Number

import numpy as np

"""A global counter to count the total number of VarAutoName instances"""
G_VAR_AUTO_NAME_NUM = 0


class Mode(Enum):
    Forward = 0
    Reverse = 1
    Mix = 2
    NONE = -1


class Var(object):
    """
        A class that holds variables with AutoDiff method in both forward and reverse mode.
        Supports 20+ elementary functions (see ../ops.py) for scalar(Number) and 2D matrix (np.ndarray).

        Attributes:
            val (Number or np.ndarray): numerical value of this variable.
            name (str or Number, optional): name assigned to the variable, such as "x","longlongname" or 1.1, 2.
            derivative (dict): a dict that stores the derivative values w.r.t all involved variables. For example,
                {"x": numerical value of dfdx, "y": numerical value of dfdy}. A 4D matrix D is used to represent
                the single der such as dcdx: D_{ijkl} represents dc_{ij}/dx_{kl}.
            mode (Mode): for newly declared instance, specify Forward or Reverse mode. The Mix mode will come from
                the operation of a Forward mode and a non-Forward mode.
            _var_shapes (dict): a dict that stores the shape of the involved variables used for squeezing the 4D
                derivative matrix to 2D Jacobian matrix if necessary. For example, {"x": (1,1), "y": (2,1)}.
                LEAVE IT ALONE when declare a new Var instance.
            _context (list): [cls, operands] where "cls" represents the operation and operands is [a, b] if cls is
                a binary operation else [a] for unary operation. LEAVE IT ALONE when declare a new Var instance.

            _bpgrad (dict): a dict stores the temporary backpropagation gradiant, used for reverse mode only.
                For example, u.bp = {f: 1} means dfdu = 1. The key here is the hash value of f (output, a Var instance)
                while the key in u.derivative is the name of x (input, a Var instance). Similarly, a 4D matrix D is used
                to represent a single gradient dfdc: D_{ijkl} represents df_{ij}/dc_{kl}.
            _degree (int): "out degree" = number of usage in the computational graph, used for reverse mode only.
        """

    def __init__(self, val, name=None, derivative=None, mode=Mode.Forward, _var_shapes=None, _context=None):
        """
        ----------
        Args:
            val (Number or np.ndarray): numerical value of the variable.
            name (str or Number, optional): name of the variable. If None(default), the variable will be treated
                as a constant, which means no derivative wrt this instance.
            derivative (Number or np.ndarray, optional): a dict; Defaults to None. If name is None, derivative will be
                set as an empty dict; If name is not None, derivative will be initialized as {name: 4D_matrix};
                Number/np.ndarray can be passed in as the `seed` for this variable (name should not be None and the
                shape of seed should match its value).
            mode (Mode): Forward(default)/Reverse. The mode of const will be set as Mode.NONE.

            _var_shapes (dict or None): Leave it None when declare an instance. See explanations above.
            _context (list or None): Leave it None when declare an instance. See explanations above.

        TO use:
            >>> x = Var(1, 'x', mode=Mode.Forward)
            >>> y = Var(np.array([[1],[2]]), 'y', mode=Mode.Reverse)
        """

        self._val = val

        if name is None or isinstance(name, (str, Number)):
            self.name = name
        else:
            raise TypeError(f"name should be a str or Number, {type(name)} is not supported.")

        # Init derivative
        if isinstance(derivative, dict):
            self.derivative = derivative
        elif name is not None:
            self.derivative = {name: self._init_seed(val, derivative)}
        else:
            if derivative is not None:
                raise ValueError(f"Need a name!")
            # Use {} instead of None to skip the type check when self.derivative is used
            self.derivative = {}

        # Be careful, this dict is designed for sharing across multiple instances
        # which means for x = Var(1, 'x'), x.self._var_shapes can contain key="y" that is not x's "target wrt var"
        self._var_shapes = _var_shapes
        if name is not None:
            try:
                self._var_shapes[name] = np.shape(val)
            except:
                self._var_shapes = {name: np.shape(val)}

        self.mode = Mode.NONE if self.is_const else mode
        self._context = _context

        # Used only for reverse mode
        # Will be activated when ._reverse_diff() is called
        self._degrees = None
        self._bpgrad = None

    def _init_seed(self, val, seed=None):
        """
        Initialize the derivative for newly declared var instance. The shape of seed should match the shape of val.
        Or exception will be thrown out. If val is scalar, seed must be a scalar too; If val is matrix, seed could
        be a scalar or a matrix.
        Args:
            val: var's value, used for aligning the shape of val and derivative
            seed: a Number or np.ndarray, defaults to None.

        Returns:
            a 4D matrix as the initial derivative.

        For example (this function will be called in __init__):
        >>> Var(1, 'x', 100).derivative['x'].tolist()
        [[[[100.0]]]]
        >>> Var(np.array([[1],[2]]), 'x', 2).derivative['x'].tolist() # output is np.ndarray
        [[[[2.0], [0.0]]], [[[0.0], [2.0]]]]
        >>> Var(np.array([[1],[2]]), 'x', np.array([[100],[200]])).derivative['x'].tolist()
        [[[[100.0], [0.0]]], [[[0.0], [200.0]]]]
        """
        if seed is None:
            seed = 1
        elif not isinstance(seed, (Number, np.ndarray, list)):
            raise TypeError(f"Init derivative(seed) should be a ndarray or Number, {type(seed)} is not supported.")

        seed = np.array(seed)

        ndim = np.ndim(val)
        # Init seed should be a scalar or the shape of seed should be equal to the shape of  value
        assert np.ndim(seed) == 0 or np.size(seed) == np.size(val), (
            f"Initial derivative {np.shape(seed)} should match the shape of val {np.shape(val)}")

        if ndim == 2:
            k, l = val.shape
        elif ndim == 0:
            k = l = 1
        else:
            raise ValueError(f"Val only support scalar/2D-matrix. Input: {val.shape}")

        return np.einsum('ij,kl->ikjl', np.eye(k) * seed, np.eye(l))

    def __str__(self):
        return f"(val: {self.val}, der: {self.derivative})"

    def __repr__(self):
        return f"({self.__class__} name: {self.name} val: {self.val}, der: {self.derivative})"

    def __eq__(self, b):
        """Only compare the `val` and `derivative`. `name` is ignored."""
        if not isinstance(b, Var) or not np.allclose(self.val, b.val) or not (
                self.derivative.keys() == b.derivative.keys()):
            return False

        for wrt in self.derivative.keys():
            # TODO: Fan
            # Use np.array_equal instead to check the shape?
            if not np.allclose(self.derivative[wrt], b.derivative[wrt]):
                return False

        return True

    @property
    def val(self):
        """Return numerical value of variable"""
        return self._val

    @val.setter
    def val(self, v):
        """Set numerical value for variable"""
        self._val = v

    def _squeeze_der(self, name, v):
        """
        Squeeze the 4D derivative matrix to match the expectation of Jacobian matrix. The output shape is listed below:
        Input type --> output type: Jacobian matrix type
        Scalar --> scalar: scalar
        Scalar --> vector((n,1) or (1,n)): 2D matrix(n,1)
        Vector((n,1) or (1,n)) --> scalar: 2D matrix(1,n)
        Vector((n,1) or (1,n)) --> Vector((m,1) or (1,m)): 2D matrix(m,n)
        Matrix((m,n)) --> matrix((p,q)): 3D matrix if one of m,n,p,q is 1 else 4D matrix
        Args:
            name: name of target var instance
            v: 4D derivative matrix

        Returns:
            A scalar or matrix, the squeezed derivative.
        """
        shape = self._var_shapes[name]

        if len(shape) == 0:
            try:
                return v.item()
            except:
                return np.squeeze(np.squeeze(v, -1), -1)

        m, n, k, l = v.shape
        assert (k, l) == shape, f"var shape {shape} and der shape: {self.val.shape} mismatch!"

        if l == 1:
            v = np.squeeze(v, -1)
        elif k == 1:
            v = np.squeeze(v, -2)

        if n == 1:
            v = np.squeeze(v, 1)
        elif m == 1:
            v = np.squeeze(v, 0)

        return v

    def __hash__(self):
        return id(self)

    def _count_degrees(self):
        """
        Count "out degree" for every involved var instance for reverse mode.
        Returns: a dict where key = node, val = out degree
        """

        q = deque()
        q.append(self)

        degrees = Counter()
        visited = defaultdict(bool)

        while len(q) > 0:
            v = q.popleft()
            if v._context is None:
                continue
            _, operands = v._context
            for t in operands:
                degrees[t] += 1
                if not visited[t]:
                    visited[t] = True
                    q.append(t)

        return degrees

    def _backward(self):
        """
        Recursively trace back along the computational graph to propagate the derivative from output to input.
        See more explanations in code comments.
        """

        # Two cases to "merge" the .derivative from the forward propagation and ._bpgrad from the back propagation
        # if self.derivative is not None, two possible cases:
        # 1. For target vars like x,y whose .derivative is initialized when declared;
        # 2. For mix mode calculation, some node in forward mode in the trace has non-empty .derivative
        # Be careful, the merged derivative could be part of the total derivative so we need to accumulate all.
        if len(self.derivative) > 0:
            from pyautodiff import Ops
            # f: a var instance, dfdc: numerical derivative for dfdc (suppose current instance(self) is c)
            f, dfdc = self._bpgrad.popitem()
            # Merge two 4D matrix
            d = Ops.merge_fwd_backprop(self.derivative, dfdc)

            # Accumulate the derivatives
            f.derivative = Counter(f.derivative)
            f.derivative.update(d)
            f.derivative = dict(f.derivative)

        elif self._context is not None:
            cls, operands = self._context
            cls.backprop(operands[0],
                         operands[1] if len(operands) == 2 else None,
                         self.val,
                         self._bpgrad)
            # Clear it for next BP
            self._bpgrad.popitem()

            for t in operands:
                t._degree -= 1
                # When t.degree is 0, dfdt is complete and safe to trace back
                if t._degree == 0:
                    t._backward()

    def _reverse_diff(self):
        """
        Start AD of reverse mode.
        """
        degrees = self._count_degrees()
        for t in degrees:
            t._degree = degrees[t]
            t._bpgrad = Counter()

        self._bpgrad = {self: self._init_seed(self.val)}
        self._backward()

    def diff(self, wrts=None, return_raw=False):
        """
        Get derivative w.r.t. to each var in `wrts`.
        Args:
            wrts: single variable name or a list/tuple of variable names. Defaults to None, equals to `all`.

        Returns:
            a Number or np.ndarray if wrts is single variable name;
            or a list of Number or np.ndarray that corresponds to each variable name in wrts, if wrts is a list/tuple;
            or a dict with the variable name as a key and value as a Number or np.ndarray, if wrts is None.

        """

        # Reverse mode
        if len(self.derivative) == 0 and self._context is not None:
            self._reverse_diff()

        der = self.derivative
        keys = list(der.keys())

        if not return_raw:
            der = {x: self._squeeze_der(x, der[x]) for x in keys}

        if wrts is None:
            if len(keys) == 0:
                return 0

            if len(keys) == 1:
                return der[keys[0]]

            return der
        elif isinstance(wrts, (list, tuple)):
            return [der.get(w, 0) for w in wrts]
        else:
            try:
                return der[wrts]
            except:
                raise TypeError(f"wrts only supports None/list/tuple or a var name!")

    @property
    def T(self):
        """
        To support x.T
        Returns: Transposed matrix

        """
        return self.transpose()

    @property
    def is_const(self):
        """Const like: Var(1)"""
        return self._var_shapes is None


class VarAutoName(Var):
    """
    A wrapper class for class `Var`. Variable names are auto-generated by combining the current number of
    instances of `VarAutoName` and system process time to avoid duplicate names.
    """

    def __init__(self, val, derivative=None, mode=Mode.Forward):
        """

        Args:
            val (Number or np.ndarray): numerical value; same as `val` in `Var`.
            derivative: a dict or a Number/np.ndarray. Defaults to None. Same as `derivative` in `Var`.
        """
        # TODO: Fan
        # Add a Lock to protect G_VAR_AUTO_NAME_NUM
        global G_VAR_AUTO_NAME_NUM
        G_VAR_AUTO_NAME_NUM += 1
        name = f"{G_VAR_AUTO_NAME_NUM}_{time.process_time()}"

        super().__init__(val, name=name, derivative=derivative, mode=mode)

    @staticmethod
    def clear_var_counter():
        """
        Clears G_VAR_AUTO_NAME_NUM in case of overflow.

        Returns: None

        """
        global G_VAR_AUTO_NAME_NUM
        G_VAR_AUTO_NAME_NUM = 0
