import numpy as np
import numpy.random as rd
import numpy.linalg as LA
from .compact_func import Classo, pathlasso


def train_test_CV(n, k):
    idx = rd.permutation(n)
    SUBLIST = []
    sublist_len = n // k
    rest = n % k
    for i in range(k):
        if i == k-1:
            SUBLIST.append(idx[i * sublist_len:(i+1) * sublist_len + rest])
        else:
            SUBLIST.append(idx[i * sublist_len:(i+1) * sublist_len])

    return SUBLIST


def train_test_i(SUBLIST, i):
    # create training and test sets 
    training_set, test_set = np.array([], dtype=int), SUBLIST[i]
    for j in range(len(SUBLIST)):
        if j != i:
            training_set = np.concatenate((training_set, SUBLIST[j]))
    return (training_set, test_set)


def training(
    matrices,
    typ,
    num_meth,
    training_set,
    rho,
    rho_classification,
    e,
    lambdas,
    w,
    intercept,
):
    (A, C, y) = matrices
    mat = (A[training_set], C, y[training_set])
    sol = pathlasso(
        mat,
        lambdas = lambdas,
        typ = typ,
        meth = num_meth,
        rho = rho,
        e = e,
        rho_classification = rho_classification,
        w = w,
        intercept = intercept,
    )[0]
    return sol

def cv_test_i(
    matrices,
    typ,
    num_meth,
    SUBLIST,
    i,
    rho,
    rho_classification,
    e,
    lambdas,
    w,
    intercept,
):
    training_set, test_set = train_test_i(SUBLIST, i)
    BETA = training(
        matrices,
        typ,
        num_meth,
        training_set,
        rho,
        rho_classification,
        e,
        lambdas,
        w,
        intercept,
    )
    n_lam = len(lambdas)
    residual = np.zeros(n_lam)
    for j in range(n_lam):
        residual[j] = accuracy_func(
            matrices[0][test_set],
            matrices[2][test_set],
            BETA[j],
            typ,
            rho = rho,
            rho_classification = rho_classification,
            intercept = intercept,
        )

    return residual

def average_test(
    matrices,
    typ,
    num_meth,
    SUBLIST,
    rho,
    rho_classification,
    e,
    lambdas,
    w,
    intercept,
):
    k = len(SUBLIST)
    n_lam = len(lambdas)
    RESIDUAL = np.zeros((k, n_lam))
    for i in range(k):
        RESIDUAL[i, :] = cv_test_i(
            matrices,
            typ,
            num_meth,
            SUBLIST,
            i,
            rho,
            rho_classification,
            e,
            lambdas,
            w,
            intercept,
        )
    MSE = np.mean(RESIDUAL, axis = 0)
    SE = np.std(RESIDUAL, axis = 0) / np.sqrt(k)
    return (MSE, SE)


def CV(
    matrices,
    k,
    typ="R1",
    num_meth="Path-Alg",
    seed = 1,
    rho = 1.345,
    rho_classification = -1.0,
    e = 1.0,
    lambdas = None,
    Nlam = 100,
    oneSE = True,
    w = None,
    intercept = False,
):

    if lambdas is None:
        lambdas = np.linspace(1.0, 1e-3, Nlam)

    rd.seed(seed)
    n = len(matrices[0])

    SUBLIST = train_test_CV(n, k)
    MSE, SE = average_test(
        matrices,
        typ,
        num_meth,
        SUBLIST,
        rho,
        rho_classification,
        e,
        lambdas,
        w,
        intercept,
    )
    i = np.argmin(MSE)
    i_1SE = np.min(np.where(MSE < MSE[i] + SE[i]))

    if oneSE:
        lam = lambdas[i_1SE]
    else:
        lam = lambdas[i]
    out = Classo(
        matrices,
        lam,
        typ = typ,
        meth = num_meth,
        rho = rho,
        e = e,
        rho_classification = rho_classification,
        w = w,
        intercept = intercept,
    )
    return (out, MSE, SE, i, i_1SE)


# Computation of the residual, for huber, LS, huber_classification and classification
def hub(r, rho):
    h = 0
    for j in range(len(r)):
        if abs(r[j]) < rho:
            h += r[j] ** 2
        elif r[j] > 0:
            h += (2 * r[j] - rho) * rho
        else:
            h += (-2 * r[j] - rho) * rho
    return h


def hinge(A, y, beta):
    return sum(np.maximum(0, 1 - y * A.dot(beta)) ** 2)


def misclassification_rate(X, y, beta):
    yhat = np.sign(X.dot(beta))
    return np.sum(y != yhat) / len(y)


def accuracy_func(
    A, y, beta, typ="R1", rho=1.345, rho_classification=-1.0, intercept=False
):

    if intercept:
        Aprime = np.concatenate([np.ones((len(A), 1)), A], axis = 1)
    else:
        Aprime = A[:, :]

    n = len(y)

    if typ == "R2":
        return hub(Aprime.dot(beta) - y, rho) / n
    elif typ in ["C1","C2"]:
        return misclassification_rate(Aprime, y, beta)
    else:
        return LA.norm(Aprime.dot(beta) - y, 2) ** 2 / n


"""
def huber_hinge(A, y, beta, rho):
    h = np.maximum(0, 1 - y * A.dot(beta))
    s = 0
    for i in range(len(h)):
        if h[i] < rho:
            s += 2 * h[i] * rho - rho ** 2
        else:
            s += h[i] ** 2
    return s
"""