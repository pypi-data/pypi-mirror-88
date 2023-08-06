import numpy as np


def small(x, n):
    a = np.sort(x)
    return a[n-1]


def large(x, n):
    a = np.sort(x)[::-1]
    return a[n-1]


def linest(ys, xs, const=True, stats=False):
    if const:
        return np.array(np.mean(ys / xs))  # This may not be correct?
    else:
        return np.polyfit(xs, ys, 1)


def geomean(x):
    a = np.log(x)
    return np.exp(a.sum()/len(a))


def match(x0, x, match_type):
    if match_type == 0:
        return np.where(x == x0)[0][0]
    elif match_type == -1:
        return np.searchsorted(x, x0, side="right")
    elif match_type == 1:
        return np.searchsorted(x, x0, side="left")


def p_max(params):
    p_all = []
    for param in params:
        if hasattr(param, "__len__"):
            if param.size == 1:
                param = [np.asscalar(param)]
            p_all += list(param)
        else:
            p_all += [param]
    return max(p_all)


def p_min(params):
    p_all = []
    for param in params:
        if hasattr(param, "__len__"):
            if param.size == 1:
                param = [np.asscalar(param)]
            p_all += list(param)
        else:
            p_all += [param]
    return min(p_all)


def p_sum(params):
    p_all = 0
    for param in params:
        if hasattr(param, "__len__"):
            p_all += sum(param)
        else:
            p_all += param
    return p_all


def vlookup(x, x0, y, approx=True):
    if isinstance(x[0], str):
        x0 = str(x0)
    if not approx:  # need exact match
        return y[np.where(x0 == x)[0][0]]
    else:
        inds = np.searchsorted(x, x0, side='right') - 1
        return y[inds]


def lookup(x0, x, y=None):
    if y is None:
        y = x
    inds = np.searchsorted(x, x0, side='right') - 1
    return y[inds]


def p_or(**args):
    return np.logical_or(**args)


def p_and(**args):
    return np.logical_and(**args)
