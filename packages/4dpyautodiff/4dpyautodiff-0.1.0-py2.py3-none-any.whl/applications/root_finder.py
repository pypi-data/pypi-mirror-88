import numpy as np
from matplotlib import pyplot as plt

from pyautodiff import *


def Newton_Raphson_method(fn, xk, stepsize_thresh=1e-6, max_iters=1000, success_tolerance=1e-6, debug=False):
    """
        Newton's method to find root.
        Args:
            fn: funtion
            xk: initial guess
            stepsize_thresh: If ||x_{k+1} - x_{k}|| <= thresh, return
            max_iters: If #iters > max_iters, return
            success_tolerance: The absolute tolerance for fn(root)
            debug: Defaults to False. If True, print info for every iteration
        Returns:
            A dict
        """

    f = None
    is_scalar = (np.ndim(xk) == 0)

    checker = abs if is_scalar else np.linalg.norm
    solver = (lambda x, y: y / x) if is_scalar else np.linalg.solve

    offset = 1

    for k in range(max_iters):
        f = fn(Var(xk, "x"))  # This is a Var instance!! Access val and der by .val and .diff() respectively
        delta_x = solver(f.diff(), -f.val)

        if checker(delta_x) < stepsize_thresh:
            offset = 0
            break

        if debug:
            print(f"k={k}\tx={np.round(xk, 2)}\tf(x)={np.round(f.val)}\tf'(x)={np.round(f.diff())}")

        xk = xk + delta_x

    return {
        "succeed": np.allclose(f.val, 0, atol=success_tolerance),
        "iter": k + offset,
        "x": xk,
        "f(x)": f.val,
        "f\'(x)": f.diff()
    }


def cal_val_der(fn, xs):
    vals = []
    ders = []

    for x in xs:
        try:
            if not isinstance(x, (Var, VarAutoName)):
                y = fn(VarAutoName(x))
            else:
                y = fn(x)
        except:
            y = Var(0)
        finally:
            vals.append(y.val)
            ders.append(y.diff())

    return vals, ders


def draw_scalar(fn, roots, plt_range=[0, 10]):
    x = np.linspace(plt_range[0], plt_range[1], 1000).tolist()
    y, d = cal_val_der(fn, x)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='val')
    ax.plot(x, d, label='der')
    ax.scatter(roots, cal_val_der(fn, roots)[0], label="root")
    ax.grid(True, which='both')

    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    plt.title("Use 0 to fill in +-inf")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    print("====Scalar demo====")
    f = lambda x: x ** (-x) - log(x)

    rtn = Newton_Raphson_method(f, 1, debug=True)

    if rtn['succeed']:
        root = rtn["x"]
        print(f"Find a root={np.round(root, 4)}")
        draw_scalar(f, [root], plt_range=[0.1, root + 0.5])
    else:
        print(f"Failed. Try another x0 or larger max_iters!")
        print(rtn)
        draw_scalar(f, [], plt_range=[1, 5])

    print("====Vector demo====")
    A = Var(np.array([[1, 2], [3, 4]]))
    g = lambda x: A @ x - sin(exp(x))
    n_roots = 0
    for x0 in [[1, -1], [1, 1], [0, 0]]:
        x0 = np.array(x0).reshape(-1, 1)
        rtn = Newton_Raphson_method(g, x0, debug=False)
        if rtn["succeed"]:
            n_roots += 1
            root = rtn["x"]
            print(f"Find #{n_roots} root={np.round(root, 2).tolist()}")
        else:
            print(f"Failed. Try another x0 or larger max_iters!")
