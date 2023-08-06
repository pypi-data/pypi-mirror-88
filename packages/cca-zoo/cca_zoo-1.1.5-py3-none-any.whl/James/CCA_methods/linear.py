from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression, SGDRegressor, LassoLars
from sklearn.linear_model import ElasticNet
from sklearn.cross_decomposition import CCA, PLSSVD
from sklearn.linear_model import lars_path
from scipy.linalg import pinv2
from sklearn.metrics.pairwise import rbf_kernel, polynomial_kernel, linear_kernel
from scipy.linalg import eigh
import numpy as np
import matplotlib
from sklearn.utils.testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning
matplotlib.use('agg')
import matplotlib.pyplot as plt


# https://github.com/lorenzoriano/PyKCCA/blob/master/kcca.py

class Wrapper:
    # The idea is that this can take some data and run one of my many CCA_archive methods
    def __init__(self, outdim_size=2, method='l2', params=None, max_iter=50, tol=1e-6):
        self.outdim_size = outdim_size
        self.method = method
        self.params = params
        self.max_iter = max_iter
        self.tol = tol
        self.eps = np.finfo(np.float32).eps
        # I would like to be able to add more methods.
        if params is None:
            self.params = {}
        if self.method == 'l2':
            if params is None:
                self.params = {'c_1': 0, 'c_2': 0}
        if self.method == 'kernel':
            if 'kernel' not in self.params:
                self.params['kernel'] = 'linear'
            if 'degree' not in self.params:
                self.params['degree'] = 0
            if 'sigma' not in self.params:
                self.params['sigma'] = 1.0
            if 'reg' not in self.params:
                self.params['reg'] = 100
            if 'c' not in self.params:
                self.params['c'] = 1

    def fit(self, X_train, Y_train):
        if self.method == 'kernel':
            self.KCCA = KCCA(X_train, Y_train, params=self.params, outdim_size=self.outdim_size)
            self.U = self.KCCA.U
            self.V = self.KCCA.V
        elif self.method == 'pls':
            self.fit_scikit_pls(X_train, Y_train)
        else:
            if self.method == 'scikit':
                self.fit_scikit_cca(X_train, Y_train)
            else:
                self.outer_loop(X_train, Y_train)
            self.X_rotation = self.W.T @ pinv2(self.P @ self.W.T, check_finite=False)
            self.Y_rotation = self.C.T @ pinv2(self.Q @ self.C.T, check_finite=False)
        self.U /= np.linalg.norm(self.U, axis=1, keepdims=True)
        self.V /= np.linalg.norm(self.V, axis=1, keepdims=True)
        self.train_correlations = np.diag(np.corrcoef(self.U, self.V)[:self.outdim_size, self.outdim_size:])
        return self

    def cv_fit(self, X_train, Y_train, param_candidates, folds=5, verbose=False):
        self.params.update(
            cross_validate(X_train, Y_train, max_iter=self.max_iter, outdim_size=self.outdim_size, method=self.method,
                           param_candidates=param_candidates, folds=folds,
                           verbose=verbose))
        self.fit(X_train, Y_train)
        return self

    def predict_corr(self, X_test, Y_test):
        if self.method == 'kernel':
            U_test, V_test = self.KCCA.transform(X_test, Y_test)
        elif self.method == 'pls':
            U_test, V_test = self.PLS.transform(X_test, Y_test)
        else:
            U_test = X_test @ self.X_rotation
            V_test = Y_test @ self.Y_rotation
        U_test /= np.linalg.norm(U_test, axis=0, keepdims=True)
        V_test /= np.linalg.norm(V_test, axis=0, keepdims=True)
        correlations = np.diag(np.corrcoef(U_test.T, V_test.T)[:self.outdim_size, self.outdim_size:])
        return correlations

    def outer_loop(self, X_train, Y_train):
        self.W = np.zeros((self.outdim_size, X_train.shape[1]))
        self.C = np.zeros((self.outdim_size, Y_train.shape[1]))
        self.U = np.zeros((self.outdim_size, X_train.shape[0]))
        self.V = np.zeros((self.outdim_size, Y_train.shape[0]))
        self.P = np.zeros((self.outdim_size, X_train.shape[1]))
        self.Q = np.zeros((self.outdim_size, Y_train.shape[1]))
        C_train = X_train.T @ Y_train
        C_train_res = C_train.copy()
        X_train_res = X_train.copy()
        Y_train_res = Y_train.copy()
        # For each of the dimensions
        for k in range(self.outdim_size):
            self.inner_loop = ALS_inner_loop(X_train_res, Y_train_res, params=self.params,
                                             method=self.method, max_iter=self.max_iter)
            self.W[k] = self.inner_loop.w
            self.C[k] = self.inner_loop.c
            self.U[k] = (X_train_res @ self.W[k, np.newaxis].T).T
            self.V[k] = (Y_train_res @ self.C[k, np.newaxis].T).T
            self.P[k] = X_train_res.T @ self.U[k]
            self.Q[k] = Y_train_res.T @ self.V[k]
            # Deflation
            if self.method == 'pmd' or self.method == 'parkhomenko':
                d = self.W[k, np.newaxis] @ C_train @ self.C[k, np.newaxis].T
                C_train_res -= d * self.W[k, np.newaxis].T @ self.C[k, np.newaxis]
                X_train_res -= (X_train_res.T @ (self.U[k, np.newaxis].T / np.linalg.norm(self.U[k])) @ (
                        self.U[k, np.newaxis] / np.linalg.norm(self.U[k]))).T
                Y_train_res -= (Y_train_res.T @ (self.V[k, np.newaxis].T / np.linalg.norm(self.V[k])) @ (
                        self.V[k, np.newaxis] / np.linalg.norm(self.V[k]))).T
            else:
                X_train_res -= self.U[k, np.newaxis].T @ self.P[k, np.newaxis]
                Y_train_res -= self.V[k, np.newaxis].T @ self.Q[k, np.newaxis]
        return self

    def fit_scikit_cca(self, train_set_1, train_set_2):
        cca = CCA(n_components=self.outdim_size, scale=False)
        cca.fit(train_set_1, train_set_2)
        self.U = cca.x_scores_.T
        self.V = cca.y_scores_.T
        self.W = cca.x_weights_.T
        self.C = cca.y_weights_.T
        self.P = cca.x_loadings_.T
        self.Q = cca.y_loadings_.T
        return self

    def fit_scikit_pls(self, train_set_1, train_set_2):
        self.PLS = PLSSVD(n_components=self.outdim_size, scale=False)
        self.PLS.fit(train_set_1, train_set_2)
        self.U = self.PLS.x_scores_.T
        self.V = self.PLS.y_scores_.T
        self.W = self.PLS.x_weights_.T
        self.C = self.PLS.y_weights_.T
        return self


class ALS_inner_loop:
    # an alternating least squares inner loop
    def __init__(self, X, Y, max_iter=100, tol=1e-6, initialization='random', params=None,
                 method='l2'):
        self.initialization = initialization
        self.X = X
        self.Y = Y
        self.C = X.T @ Y
        self.max_iter = max_iter
        self.tol = tol
        self.params = params
        if params is None:
            self.params = {'c_1': 0, 'c_2': 0}
        self.method = method
        self.iterate()

    def iterate(self):
        # Any initialization required

        # Weight vectors for y (normalized to 1)
        c = np.random.rand(self.Y.shape[1])
        c /= np.linalg.norm(self.X@c)

        if any(self.method in _ for _ in ['scca', 'pmd', 'constrained_scca', 'sgcca', 'constrained_sgcca']):
            warm_start = ALS_inner_loop(self.X, self.Y)
            target = self.X @ warm_start.w + self.Y @ warm_start.c
            target /= np.linalg.norm(target)
            v = self.Y @ warm_start.c

        # Pre calculate inverses. Used for unregularized CCA
        if self.X.shape[1] < self.X.shape[0]:
            self.X_inv = pinv2(self.X, check_finite=False)
        else:
            self.X_inv = None

        if self.Y.shape[1] < self.X.shape[0]:
            self.Y_inv = pinv2(self.Y, check_finite=False)
        else:
            self.Y_inv = None

        # Object to store statistics for convergence analysis
        self.track_correlation = np.zeros(self.max_iter)
        self.track_correlation[:] = np.nan
        self.track_obj = np.zeros(self.max_iter)
        self.track_obj[:] = np.nan
        self.track_norms_w = np.zeros(self.max_iter)
        self.track_norms_w[:] = np.nan
        self.track_norms_c = np.zeros(self.max_iter)
        self.track_norms_c[:] = np.nan

        for _ in range(self.max_iter):

            if self.method == 'l2':
                # Use ridge solver or pseudo-inverse
                w = self.ridge_solver(self.X, v,self.X_inv, alpha=self.params['c_1'])
                w /= np.linalg.norm(self.X @ w)
            elif self.method == 'pmd':
                w = self.C @ c
                w, w_success = self.update(w, self.params['c_1'])
                if not w_success:
                    w = self.C @ c
                w /= np.linalg.norm(w)
            elif self.method == 'parkhomenko':
                w = self.C @ c
                if np.linalg.norm(w) == 0:
                    w = self.C @ c
                w /= np.linalg.norm(w)
                w = self.soft_threshold(w, self.params['c_1'] / 2)
                if np.linalg.norm(w) == 0:
                    w = self.C @ c
                w /= np.linalg.norm(w)
            elif self.method == 'elastic':
                w = self.elastic_solver(self.X, v, alpha=self.params['c_1'], l1_ratio=self.params['l1_ratio_1'])
                w /= np.linalg.norm(self.X @ w)
            elif self.method == 'constrained_scca':
                w = self.constrained_regression(self.X, v, self.params['c_1'])
            elif self.method == 'scca':
                target = self.Y @ c
                w = self.lasso_solver(self.X, target, self.X_inv, alpha=self.params['c_1'])
                w /= np.linalg.norm(self.X @ w)
                self.u = self.X @ w
            elif self.method == 'sgcca':
                w = self.lasso_solver(self.X, target, self.X_inv, alpha=self.params['c_1'] / 2)
                w /= np.linalg.norm(self.X @ w)
                self.u = self.X @ w
            elif self.method == 'constrained_sgcca':
                w = self.constrained_regression(self.X, target, self.params['c_1'])

            # TODO could we group the w and c update to prevent the duplication?

            if self.method == 'l2':
                u = self.X @ w
                c = self.ridge_solver(self.Y, u, self.Y_inv, alpha=self.params['c_2'])
                c /= np.linalg.norm(self.Y @ c)
                v = self.Y @ c
            elif self.method == 'pmd':
                c = self.C.T @ w
                c, c_success = self.update(c, self.params['c_2'])
                if not c_success:
                    c = self.C.T @ w
                c /= np.linalg.norm(c)
            elif self.method == 'parkhomenko':
                c = self.C.T @ w
                if np.linalg.norm(c) == 0:
                    c = self.C.T @ w
                c /= np.linalg.norm(c)
                c = self.soft_threshold(c, self.params['c_2'] / 2)
                if np.linalg.norm(c) == 0:
                    c = self.C.T @ w
                c /= np.linalg.norm(c)
            elif self.method == 'elastic':
                u = self.X @ w
                c = self.elastic_solver(self.Y, u, alpha=self.params['c_2'], l1_ratio=self.params['l1_ratio_2'])
                # constraint
                c /= np.linalg.norm(self.Y @ c)
                v = self.Y @ c
            elif self.method == 'constrained_scca':
                u = self.X @ w
                c = self.constrained_regression(self.Y, u, self.params['c_2'])
                v = self.Y @ c
            elif self.method == 'scca':
                target = self.X @ w
                c = self.lasso_solver(self.Y, target, self.Y_inv, alpha=self.params['c_2'])
                c /= np.linalg.norm(self.Y @ c)
            elif self.method == 'sgcca':
                c = self.lasso_solver(self.Y, target, self.Y_inv, alpha=self.params['c_2'] / 2)
                c /= np.linalg.norm(self.Y @ c)
                target = (self.Y @ c + self.X @ w) / 2
            elif self.method == 'constrained_sgcca':
                c = self.constrained_regression(self.Y, target, self.params['c_2'])
                target = (self.Y @ c + self.X @ w) / 2

            if _ > 0:
                if np.linalg.norm(w - w_old) < self.tol and np.linalg.norm(c - c_old) < self.tol:
                    break

            self.w = w
            self.c = c
            w_old = w
            c_old = c
            # Update trackers
            self.track_correlation[_] = np.corrcoef(self.X @ w, self.Y @ c)[0, 1]
            if any(self.method in _ for _ in ['scca', 'pmd', 'constrained_scca', 'sgcca', 'constrained_sgcca']):
                self.track_obj[_] = self.lasso_lyuponov()
                self.track_norms_w[_] = np.linalg.norm(w, ord=1)
                self.track_norms_c[_] = np.linalg.norm(c, ord=1)
        return self

    def soft_threshold(self, x, delta):
        diff = abs(x) - delta
        diff[diff < 0] = 0
        out = np.sign(x) * diff
        return out

    def bisec(self, K, c, x1, x2):
        # does a binary search between x1 and x2 (thresholds). Outputs weight vector.
        converge = False
        success = True
        tol = 1e-5
        while not converge and success:
            x = (x2 + x1) / 2
            out = self.soft_threshold(K, x)
            if np.linalg.norm(out, 2) > 0:
                out = out / np.linalg.norm(out, 2)
            else:
                out = np.empty(out.shape)
                out[:] = np.nan
            if np.sum(np.abs(out)) == 0:
                x2 = x
            elif np.linalg.norm(out, 1) > c:
                x1 = x
            elif np.linalg.norm(out, 1) < c:
                x2 = x

            diff = np.abs(np.linalg.norm(out, 1) - c)
            if diff <= tol:
                converge = True
            elif np.isnan(np.sum(diff)):
                success = False
        return out

    def update(self, w, c):
        success = True
        delta = 0
        # update the weights
        # Do the soft thresholding operation
        up = self.soft_threshold(w, delta)
        if np.linalg.norm(up, 2) > 0:
            up = up / np.linalg.norm(up, 2)
        else:
            up = np.empty(up.shape)
            up[:] = np.nan

        # if the 1 norm of the weights is greater than c
        it = 0
        if np.linalg.norm(up, 1) > c:
            delta1 = delta
            delta2 = delta1 + 1.1
            converged = False
            max_delta = 0
            while not converged and success:
                up = self.soft_threshold(w, delta2)
                if np.linalg.norm(up, 2) > 0:
                    up = up / np.linalg.norm(up, 2)
                # if all zero or all nan then delta2 too big
                if np.sum(np.abs(up)) == 0 or np.isnan(np.sum(np.abs(up))):
                    delta2 = delta2 / 1.618
                # if too big then increase delta
                elif np.linalg.norm(up, 1) > c:
                    delta1 = delta2
                    delta2 = delta2 * 2
                # if there is slack then converged
                elif np.linalg.norm(up, 1) <= c:
                    converged = True

                # update the maximum attempted delta
                if delta2 > max_delta:
                    max_delta = delta2

                # if the threshold
                if delta2 == 0:
                    success = False
                it += 1
                if it == self.max_iter:
                    delta1 = 0
                    delta2 = max_delta
                    success = False
            if success:
                up = self.bisec(w, c, delta1, delta2)
                if np.isnan(np.sum(up)) or np.sum(up) == 0:
                    success = False
        return up, success

    @ignore_warnings(category=ConvergenceWarning)
    def lasso_solver(self, X, y, X_inv=None, alpha=0.1):
        if alpha == 0:
            if X_inv is not None:
                beta = np.dot(X_inv, y)
            else:
                clf = LinearRegression(fit_intercept=False)
                clf.fit(X, y)
                beta = clf.coef_
        else:
            lassoreg = Lasso(alpha=alpha, fit_intercept=False)
            lassoreg.fit(X, y)
            beta = lassoreg.coef_
        return beta

    @ignore_warnings(category=ConvergenceWarning)
    def ridge_solver(self, X, y, X_inv=None, alpha=0.1):
        if alpha == 0:
            if X_inv is not None:
                beta = np.dot(X_inv, y)
            else:
                clf = LinearRegression(fit_intercept=False)
                clf.fit(X, y)
                beta = clf.coef_
        else:
            clf = Ridge(alpha=alpha, fit_intercept=False)
            clf.fit(X, y)
            beta = clf.coef_
        return beta

    @ignore_warnings(category=ConvergenceWarning)
    def elastic_solver(self, X, y, alpha=0.1, l1_ratio=0.5):
        clf = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
        clf.fit(X, y)
        beta = clf.coef_
        if not np.any(beta):
            beta = np.ones(beta.shape)
        return beta

    @ignore_warnings(category=ConvergenceWarning)
    def constrained_regression(self, X, y, p, search='bin'):
        if p == 0:
            coef = SGDRegressor(fit_intercept=False).fit(X, y).coef_
        if search == 'bin':
            converged = False
            min_ = 0
            max_ = 1
            current = 1
            previous = 1
            previous_val = 1e+10
            i = 0
            while not converged:
                i += 1
                # coef = Lasso(alpha=current, selection='cyclic', max_iter=10000).fit(X, y).coef_
                coef = Lasso(alpha=current, selection='cyclic').fit(X, y).coef_
                if np.linalg.norm(X @ coef) > 0:
                    current_val = p - np.linalg.norm(coef / np.linalg.norm(X @ coef), ord=1)
                else:
                    current_val = p
                current, previous, min_, max_ = bin_search(current, previous, current_val, previous_val, min_, max_)
                previous_val = current_val
                if np.abs(current_val) < 1e-5:
                    converged = True
                elif current < 1e-15:
                    converged = True
                elif np.abs(max_ - min_) < 1e-30 or i == 50:
                    converged = True
                    # coef = Lasso(alpha=min_, selection='cyclic', max_iter=10000).fit(X, y).coef_
                    coef = Lasso(alpha=min_, selection='cyclic').fit(X, y).coef_
        else:
            alphas, _, coefs = lars_path(X, y)
            coefs_l1 = np.linalg.norm(coefs, ord=1, axis=0)
            projs_l2 = np.linalg.norm(X @ coefs, ord=2, axis=0)
            projs_l2[projs_l2 == 0] = 1e-20
            l1_normalized_norms = coefs_l1 / projs_l2
            l1_normalized_norms[np.isnan(l1_normalized_norms)] = 0
            alpha_max = np.argmax(l1_normalized_norms > p)
            alpha_min = alpha_max - 1
            if alpha_max == 0:  # -1:
                coef = SGDRegressor(fit_intercept=False).fit(X, y).coef_
            elif alpha_min == 0:
                success = False
            else:
                new_vec_hat = X @ (coefs[:, alpha_max] - coefs[:, alpha_min])
                old_vec = X @ coefs[:, alpha_min]
                m = coefs_l1[alpha_max] - coefs_l1[alpha_min]
                c = coefs_l1[alpha_min]
                A = m ** 2 - p ** 2 * new_vec_hat.T @ new_vec_hat
                B = 2 * m * c - 2 * p ** 2 * new_vec_hat.T @ old_vec
                C = c ** 2 - p ** 2 * old_vec.T @ old_vec
                f_pos = (-B + np.sqrt(B ** 2 - 4 * A * C)) / (2 * A)
                coef = coefs[:, alpha_min] + f_pos * (coefs[:, alpha_max] - coefs[:, alpha_min])
        coef = coef / np.linalg.norm(X @ coef)
        return coef

    def lasso_lyuponov(self):
        lyuponov = 2 / (2 * self.X.shape[0]) - 2 * (self.X @ self.w).T @ (self.Y @ self.c) / (2 * self.X.shape[0]) + \
                   self.params[
                       'c_1'] * np.linalg.norm(
            self.w, ord=1) + self.params['c_2'] * np.linalg.norm(self.c, ord=1)
        return lyuponov


class KCCA:
    # an alternating least squares inner loop
    def __init__(self, X, Y, params=None, outdim_size=2):
        self.X = X
        self.Y = Y
        self.outdim_size = outdim_size
        self.ktype = params.get('kernel')
        self.sigma = params.get('sigma')
        self.degree = params.get('degree')
        self.reg = params.get('reg')
        self.c = params.get('c')
        if self.c is None:
            print('here')
        self.K1 = self.make_kernel(X, X)
        self.K2 = self.make_kernel(Y, Y)
        R, D = self.hardoon_method()
        # solve generalized eigenvalues problem
        betas, alphas = eigh(R, D)
        # sorting according to eigenvalue
        betas = np.real(betas)
        ind = np.argsort(betas)
        N = self.K1.shape[0]
        alphas = alphas[:, ind]
        alpha = alphas[:, :outdim_size]
        # making unit vectors
        alpha = alpha / (np.sum(np.abs(alpha) ** 2, axis=0) ** (1. / 2))
        alpha1 = alpha[:N, :]
        alpha2 = -alpha[N:, :]
        self.U = np.dot(self.K1, alpha1).T
        self.V = np.dot(self.K2, alpha2).T
        self.alpha1 = alpha1
        self.alpha2 = alpha2

    def make_kernel(self, X, Y):
        if self.ktype == 'linear':
            kernel = linear_kernel(X, Y=Y)
        elif self.ktype == 'gaussian':
            kernel = rbf_kernel(X, Y=Y, gamma=(1 / (2 * self.sigma)))
        elif self.ktype == 'poly':
            kernel = polynomial_kernel(X, Y=Y, degree=self.degree, coef0=self.c)
        return kernel

    def hardoon_method(self):

        N = self.K1.shape[0]
        I = np.eye(N)
        Z = np.zeros((N, N))

        R1 = np.c_[Z, np.dot(self.K1, self.K2)]
        R2 = np.c_[np.dot(self.K2, self.K1), Z]
        R = np.r_[R1, R2]

        D1 = np.c_[np.dot(self.K1, self.K1) + self.reg * I, Z]
        D2 = np.c_[Z, np.dot(self.K2, self.K2) + self.reg * I]
        D = 0.5 * np.r_[D1, D2]
        # http://www.squobble.com/academic/kcca_wiener/node4.html
        return R, D

    def transform(self, X_test, Y_test):
        n_dims = self.alpha1.shape[1]
        Ktest = self.make_kernel(X_test, self.X)
        U_test = np.dot(Ktest, self.alpha1[:, :n_dims])
        Ktest = self.make_kernel(Y_test, self.Y)
        V_test = np.dot(Ktest, self.alpha2[:, :n_dims])
        return U_test, V_test


def permutation_test(train_set_1, train_set_2, outdim_size=5,
                     method='als', params=None, n_reps=100, level=0.05):
    if params is None:
        params = {}
    rho_train = np.zeros((n_reps, outdim_size))

    for _ in range(n_reps):
        print('permutation test rep: ', _ / n_reps, flush=True)
        results = Wrapper(outdim_size=outdim_size, method=method, params=params).fit(train_set_1,
                                                                                     train_set_2).train_correlations
        np.random.shuffle(train_set_1)
        rho_train[_, :] = results

    p_vals = np.zeros(outdim_size)
    # FWE Adjusted
    for i in range(outdim_size):
        p_vals[i] = (1 + (rho_train[:, 0] > rho_train[0, i]).sum()) / n_reps
    hypothesis_test = False
    significant_dims = 0
    while not hypothesis_test:
        if p_vals[significant_dims] > level:
            hypothesis_test = True
        else:
            significant_dims += 1
        if significant_dims == len(p_vals):
            hypothesis_test = True

    print('significant dims at level: ', str(level * 100), '%:', str(significant_dims), flush=True)
    print(p_vals, flush=True)
    return p_vals, significant_dims


def cross_validate(view_1, view_2, max_iter=100, outdim_size=5, method='l2', param_candidates=None, folds=5,
                   verbose=False):
    print('cross validation with ', method, flush=True)
    print('number of folds: ', folds, flush=True)

    # Set up an array for each set of hyperparameters (perhaps could construct this automatically in the future?)
    assert (len(param_candidates) > 0)
    hyperparameter_grid_shape = [len(v) for k, v in param_candidates.items()]
    hyperparameter_scores = np.zeros(tuple([folds] + hyperparameter_grid_shape))

    # set up fold array. Suspect will need a function for this in future due to family/twins etc.
    inds = np.arange(view_1.shape[0])
    np.random.shuffle(inds)
    fold_inds = np.array_split(inds, folds)

    for index, x in np.ndenumerate(hyperparameter_scores[0]):
        params = {}
        p_num = 0
        for key in param_candidates.keys():
            params[key] = param_candidates[key][index[p_num]]
            p_num += 1
        if verbose:
            print(params)
        for fold in range(folds):
            train_set_1 = np.delete(view_1, fold_inds[fold], axis=0)
            train_set_2 = np.delete(view_2, fold_inds[fold], axis=0)
            val_set_1 = view_1[fold_inds[fold], :]
            val_set_2 = view_2[fold_inds[fold], :]
            hyperparameter_scores[(fold,) + index] = \
                Wrapper(outdim_size=outdim_size, method=method, params=params, max_iter=max_iter).fit(train_set_1,
                                                                                                      train_set_2).predict_corr(
                    val_set_1, val_set_2).sum()
        if verbose:
            print(hyperparameter_scores.sum(axis=0)[index] / folds)

    hyperparameter_scores_avg = hyperparameter_scores.sum(axis=0) / folds
    hyperparameter_scores_avg[np.isnan(hyperparameter_scores_avg)] = 0
    # Find index of maximum value from 2D numpy array
    result = np.where(hyperparameter_scores_avg == np.amax(hyperparameter_scores_avg))
    # Return the 1st
    best_params = {}
    p_num = 0
    for key in param_candidates.keys():
        best_params[key] = param_candidates[key][result[p_num][0].item()]
        p_num += 1
    print('Best score : ', np.amax(hyperparameter_scores_avg), flush=True)
    print(best_params, flush=True)
    if len(param_candidates) == 2:
        if not method == 'kernel':
            cv_plot_2(hyperparameter_scores_avg, param_candidates, method)
    return best_params


def cv_plot_2(scores, param_dict, reg):
    x1_name = list(param_dict.keys())[0]
    x1_vals = list(param_dict.values())[0]
    x2_name = list(param_dict.keys())[1]
    x2_vals = list(param_dict.values())[1]
    plt.figure()
    lineObjects = plt.plot(x1_vals, scores.T)
    plt.xlabel(x1_name)
    plt.legend(lineObjects, x2_vals, title=x2_name)
    plt.title('Hyperparameter plot ' + reg)
    plt.ylabel('Score (sum of first n correlations)')
    plt.savefig('Hyperparameter_plot ' + reg)


def bin_search(current, previous, current_val, previous_val, min_, max_):
    """Binary search helper function:
    current:current parameter value
    previous:previous parameter value
    current_val:current function value
    previous_val: previous function values
    min_:minimum parameter value resulting in function value less than zero
    max_:maximum parameter value resulting in function value greater than zero
    Problem needs to be set up so that greater parameter, greater target
    """

    if current_val < 0:
        if previous_val < 0:
            new = (current + max_) / 2
        if previous_val > 0:
            new = (current + previous) / 2
        if current > min_:
            min_ = current
    if current_val > 0:
        if previous_val > 0:
            new = (current + min_) / 2
        if previous_val < 0:
            new = (current + previous) / 2
        if current < max_:
            max_ = current

    return new, current, min_, max_
