from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import ElasticNet
from sklearn.cross_decomposition import CCA
from scipy.linalg import pinv2
from scipy.linalg import eigh
import numpy as np
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt


class Wrapper:
    # The idea is that this can take some data and run one of my many CCA_archive methods
    def __init__(self, outdim_size=2, method='l2', params=None, max_iter=100, tol=1e-5):
        self.outdim_size = outdim_size
        self.method = method
        self.params = params
        self.max_iter = max_iter
        self.tol = tol
        self.eps = np.finfo(np.float32).eps
        # I would like to be able to add more methods.
        if self.method == 'l2':
            if params is None:
                self.params = {'c_1': 0, 'c_2': 0}
            assert (self.params['c_1'] >= 0 or self.params['c_2'] >= 0)
        if self.method == 'kernel':
            if params is None:
                self.params = {}
            if 'kernel' not in self.params:
                self.params['kernel'] = 'linear'
            if 'degree' not in self.params:
                self.params['degree'] = 0
            if 'gausigma' not in self.params:
                self.params['gausigma'] = 1.0
            if 'reg' not in self.params:
                self.params['reg'] = 0.1

    def fit(self, X_train, Y_train):
        assert (X_train.shape[0] == Y_train.shape[0])
        if self.method == 'witten':
            assert (self.params['c_1'] >= 1)
            assert (self.params['c_2'] >= 1)
            assert (self.params['c_1'] <= np.sqrt(X_train.shape[1]))
            assert (self.params['c_2'] <= np.sqrt(Y_train.shape[1]))
        if self.method == 'waaijenborg':
            # constraint due to scikit learn
            assert (self.params['c_1'] > 0)
            assert (self.params['c_2'] > 0)
            # due to scikit learn stability
            assert (self.params['l1_ratio_1'] >= 0.01)
            assert (self.params['l1_ratio_2'] >= 0.01)
        if self.method == 'kernel':
            self.kcca([X_train, Y_train], numCC=self.outdim_size,
                      ktype=self.params.get('kernel'), gausigma=self.params.get('gausigma'),
                      degree=self.params.get('degree'), reg=self.params.get('reg'))
            self.recon([X_train, Y_train])
        else:
            if self.method == 'scikit':
                self.fit_scikit_cca(X_train, Y_train)
            else:
                self.outer_loop(X_train, Y_train)
            self.X_rotation = self.W.T @ pinv2(self.P @ self.W.T, check_finite=False)
            self.Y_rotation = self.C.T @ pinv2(self.Q @ self.C.T, check_finite=False)
        correlations = np.diag(self.U @ self.V.T) / (np.linalg.norm(self.U, axis=1) * np.linalg.norm(
            self.V, axis=1))
        self.train_correlations = correlations
        return self

    def cv_fit(self, X_train, Y_train, param_candidates, folds=5, verbose=False):
        self.params = cross_validate(X_train, Y_train, outdim_size=self.outdim_size, method=self.method,
                                     param_candidates=param_candidates, folds=folds,
                                     verbose=verbose)
        self.fit(X_train, Y_train)
        return self

    def predict_corr(self, X_test, Y_test):
        assert (X_test.shape[0] == Y_test.shape[0])
        if self.method == 'kernel':
            U_test, V_test = self.kernel_predict([X_test, Y_test], self.ws)
        else:
            U_test = X_test @ self.X_rotation
            V_test = Y_test @ self.Y_rotation
        correlations = np.diag(U_test.T @ V_test) / (
                np.linalg.norm(U_test, axis=0) * np.linalg.norm(V_test, axis=0))
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

            inner_loop = ALS_inner_loop(X_train_res, Y_train_res, params=self.params,
                                        method=self.method)
            self.W[k] = inner_loop.w
            self.C[k] = inner_loop.c
            self.U[k] = (X_train_res @ self.W[k, np.newaxis].T).T
            self.V[k] = (Y_train_res @ self.C[k, np.newaxis].T).T
            self.P[k] = X_train_res.T @ self.U[k]
            self.Q[k] = Y_train_res.T @ self.V[k]
            # Deflation
            if self.method == 'witten' or self.method == 'parkhomenko' or self.method == 'agoston':
                d = self.W[k, np.newaxis] @ C_train @ self.C[k, np.newaxis].T
                C_train_res -= d * self.W[k, np.newaxis].T @ self.C[k, np.newaxis]
                X_train_res -= (X_train_res.T @ (self.U[k, np.newaxis].T / np.linalg.norm(self.U[k])) @ (
                        self.U[k, np.newaxis] / np.linalg.norm(self.U[k]))).T
                Y_train_res -= (Y_train_res.T @ (self.V[k, np.newaxis].T / np.linalg.norm(self.V[k])) @ (
                        self.V[k, np.newaxis] / np.linalg.norm(self.V[k]))).T
            elif self.method == 'waaijenborg':
                X_train_res -= (X_train_res.T @ (self.U[k, np.newaxis].T / np.linalg.norm(self.U[k])) @ (
                        self.U[k, np.newaxis] / np.linalg.norm(self.U[k]))).T
                Y_train_res -= (Y_train_res.T @ (self.V[k, np.newaxis].T / np.linalg.norm(self.V[k])) @ (
                        self.V[k, np.newaxis] / np.linalg.norm(self.V[k]))).T
            else:
                self.U[k] = (X_train_res @ self.W[k, np.newaxis].T).T
                self.V[k] = (Y_train_res @ self.C[k, np.newaxis].T).T
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

    def recon(self, data):
        # Get canonical variates and CCs
        self.ws = self._listdot(data, self.comp)
        U, V = self._listdot([d.T for d in data], self.ws)
        self.U = U.T
        self.V = V.T
        return self

    def kcca(self, data, reg=0.01, numCC=None, ktype='linear',
             gausigma=1.0, degree=2):
        """Set up and solve the kernel CCA eigenproblem
        """
        kernel = [self.make_kernel(d, ktype=ktype, gausigma=gausigma,
                                   degree=degree) for d in data]

        nDs = len(kernel)
        nFs = [k.shape[0] for k in kernel]
        numCC = min([k.shape[1] for k in kernel]) if numCC is None else numCC

        # Get the auto- and cross-covariance matrices
        crosscovs = [np.dot(ki, kj.T) for ki in kernel for kj in kernel]

        # Allocate left-hand side (LH) and right-hand side (RH):
        LH = np.zeros((sum(nFs), sum(nFs)))
        RH = np.zeros((sum(nFs), sum(nFs)))

        # Fill the left and right sides of the eigenvalue problem
        for i in range(nDs):
            RH[sum(nFs[:i]): sum(nFs[:i + 1]),
            sum(nFs[:i]): sum(nFs[:i + 1])] = (crosscovs[i * (nDs + 1)]
                                               + reg * np.eye(nFs[i]))

            for j in range(nDs):
                if i != j:
                    LH[sum(nFs[:j]): sum(nFs[:j + 1]),
                    sum(nFs[:i]): sum(nFs[:i + 1])] = crosscovs[nDs * j + i]

        LH = (LH + LH.T) / 2.
        RH = (RH + RH.T) / 2.

        maxCC = LH.shape[0]
        r, Vs = eigh(LH, RH, eigvals=(maxCC - numCC, maxCC - 1))
        r[np.isnan(r)] = 0
        rindex = np.argsort(r)[::-1]
        self.comp = []
        Vs = Vs[:, rindex]
        for i in range(nDs):
            self.comp.append(Vs[sum(nFs[:i]):sum(nFs[:i + 1]), :numCC])
        return self

    def make_kernel(self, d, normalize=True, ktype='linear', gausigma=1.0, degree=2):
        """Makes a kernel for data d
          If ktype is 'linear', the kernel is a linear inner product
          If ktype is 'gaussian', the kernel is a Gaussian kernel, sigma = gausigma
          If ktype is 'poly', the kernel is a polynomial kernel with degree=degree
        """
        d = np.nan_to_num(d)
        cd = d - d.mean(axis=0, keepdims=True)
        if ktype == 'linear':
            kernel = np.dot(cd, cd.T)
        elif ktype == 'gaussian':
            from scipy.spatial.distance import pdist, squareform
            pairwise_dists = squareform(pdist(d, 'euclidean'))
            kernel = np.exp(-pairwise_dists ** 2 / 2 * gausigma ** 2)
        elif ktype == 'poly':
            kernel = np.dot(cd, cd.T) ** degree
        kernel = (kernel + kernel.T) / 2.
        if normalize:
            kernel = kernel / np.linalg.eigvalsh(kernel).max()
        return kernel

    def kernel_predict(self, vdata, ws, cutoff=1e-15):
        """Get predictions for each dataset based on the other datasets
        and weights. Find correlations with actual dataset."""
        iws = [np.linalg.pinv(w.T, rcond=cutoff) for w in ws]
        U_test, V_test = self._listdot([d.T for d in vdata], ws)
        return U_test, V_test

    def _listdot(self, d1, d2):
        return [np.dot(x[0].T, x[1]) for x in zip(d1, d2)]


class ALS_inner_loop:
    # an alternating least squares inner loop
    def __init__(self, X, Y, max_iter=100, tol=np.finfo(np.float32).eps, initialization='random', params=None,
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
        c = np.random.rand(self.X.shape[1])
        c /= np.linalg.norm(c)

        # Score/Projection vector for Y (normalized to 1)
        v = np.random.rand(self.X.shape[0])
        v = v / np.linalg.norm(v)

        u = None

        # Pre calculate inverses. Used for unregularized CCA_archive
        X_inv = pinv2(self.X)
        Y_inv = pinv2(self.Y)

        alpha_w = self.X.shape[1]
        alpha_c = self.Y.shape[1]

        # Object to store statistics for convergence analysis
        self.track_correlation = np.zeros(self.max_iter)
        self.track_correlation[:] = np.nan
        self.track_covariance = np.zeros(self.max_iter)
        self.track_covariance[:] = np.nan
        self.track_distance = np.zeros(self.max_iter)
        self.track_distance[:] = np.nan
        # Useful for the John one
        self.track_alpha_w = np.zeros(self.max_iter)
        self.track_alpha_w[:] = np.nan
        self.track_alpha_c = np.zeros(self.max_iter)
        self.track_alpha_c[:] = np.nan
        # Useful for the John one
        self.track_active_weights_w = np.zeros(self.max_iter)
        self.track_active_weights_w[:] = np.nan
        self.track_active_weights_c = np.zeros(self.max_iter)
        self.track_active_weights_c[:] = np.nan

        w_success = True
        c_success = True

        for _ in range(self.max_iter):

            # Update W
            ## I've implemented each update as I understand it for w and c. At the moment I've just repeated the updates for w and c
            if self.method == 'l2':
                # Use ridge solver or pseudo-inverse
                w = self.ridge_solver(self.X, v, X_inv, alpha=self.params['c_1'])
                w /= np.linalg.norm(self.X @ w)
            elif self.method == 'witten':
                # Use covariance matrix and then iterative soft-thresholding to fuflfil constraint on w directly
                w = self.C @ c
                w, w_success = self.update(w, self.params['c_1'])
                if not w_success:
                    w = self.C @ c
                w /= np.linalg.norm(w)
            elif self.method == 'parkhomenko':
                # Use covariance matrix and then iterative soft-thresholding at defined level
                w = self.C @ c
                if np.linalg.norm(w) == 0:
                    w = self.C @ c
                w /= np.linalg.norm(w)
                w = self.soft_threshold(w, self.params['c_1'] / 2)
                if np.linalg.norm(w) == 0:
                    w = self.C @ c
                w /= np.linalg.norm(w)
            elif self.method == 'SAR':
                # Apply lasso solver directly
                w = self.lasso_solver(self.X, v, alpha=self.params['c_1'])
                w /= np.linalg.norm(w)
            elif self.method == 'waaijenborg':
                # Apply elastic net
                w = self.elastic_solver(self.X, v, alpha=self.params['c_1'], l1_ratio=self.params['l1_ratio_1'])
                w /= np.linalg.norm(w)
            elif self.method == 'john':
                if u is not None:
                    target = u + v
                else:
                    target = v
                w, alpha = self.john_update(self.X, target, self.params['c_1'])
            elif self.method == 'agoston':
                # Use ridge solver or pseudo-inverse and then iterative soft thresholding for weight constraint
                w = self.ridge_solver(self.X, v, X_inv, alpha=0)
                w, w_success = self.update(w, self.params['c_1'])
                if not w_success:
                    w = self.C @ c
                    w /= np.linalg.norm(w)

            # TODO could we group the w and c update to prevent the duplication?

            # Update C
            if self.method == 'l2':
                u = self.X @ w
                c = self.ridge_solver(self.Y, u, Y_inv, alpha=self.params['c_2'])
                v = self.Y @ c
            elif self.method == 'witten':
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
            elif self.method == 'SAR':
                u = self.X @ w
                c = self.lasso_solver(self.Y, u, alpha=self.params['c_2'])
                # constraint
                c /= np.linalg.norm(c)
                v = self.Y @ c
            elif self.method == 'waaijenborg':
                u = self.X @ w
                c = self.elastic_solver(self.Y, u, alpha=self.params['c_2'], l1_ratio=self.params['l1_ratio_2'])
                # constraint
                c /= np.linalg.norm(c)
                v = self.Y @ c
            elif self.method == 'john':
                c, alpha = self.john_update(self.Y, target, self.params['c_2'])
                v = self.Y @ c
                u = self.X @ w
            elif self.method == 'agoston':
                u = self.X @ w
                c = self.ridge_solver(self.Y, u, Y_inv, alpha=0)
                c, c_success = self.update(c, self.params['c_2'])
                if not c_success:
                    c = self.C.T @ w
                    c /= np.linalg.norm(c)
                v = self.Y @ c

            # Print statement
            # if not w_success:
            #    print('Non-sparse w')
            # if not c_success:
            #    print('Non-sparse c')

            # Check for convergence
            if _ > 0:
                if np.linalg.norm(w - w_old) < self.tol and np.linalg.norm(c - c_old) < self.tol:
                    break

            w_old = w
            c_old = c

            # Update trackers
            self.track_correlation[_] = np.corrcoef(self.X @ w, self.Y @ c)[0, 1]
            self.track_covariance[_] = np.cov(self.X @ w, self.Y @ c)[0, 1]
            self.track_distance[_] = np.linalg.norm(self.X @ w - self.Y @ c)
            self.track_active_weights_w[_] = np.count_nonzero(w)
            self.track_active_weights_c[_] = np.count_nonzero(c)
            self.track_alpha_w[_] = alpha_w
            self.track_alpha_c[_] = alpha_c
        self.w = w
        self.c = c
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

    # @ignore_warnings(category=ConvergenceWarning)
    def lasso_solver(self, X, y, alpha=0.1):
        lassoreg = Lasso(alpha=alpha, fit_intercept=False)
        lassoreg.fit(X, y)
        beta = lassoreg.coef_
        if not np.any(beta):
            beta = np.ones(beta.shape)
        return beta

    # @ignore_warnings(category=ConvergenceWarning)
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

    # @ignore_warnings(category=ConvergenceWarning)
    def elastic_solver(self, X, y, alpha=0.1, l1_ratio=0.5):
        clf = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
        clf.fit(X, y)
        beta = clf.coef_
        if not np.any(beta):
            beta = np.ones(beta.shape)
        return beta


def permutation_test(train_set_1, train_set_2, outdim_size=5,
                     method='als', params=None, n_reps=100, level=0.05):
    # DOes
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


def cross_validate(view_1, view_2, outdim_size=5, method='l2', param_candidates=None, folds=5,
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
            train_set_1 = view_1[fold_inds[fold], :]
            train_set_2 = view_2[fold_inds[fold], :]
            val_set_1 = view_1[~fold_inds[fold], :]
            val_set_2 = view_2[~fold_inds[fold], :]
            hyperparameter_scores[(fold,) + index] = \
                Wrapper(outdim_size=outdim_size, method=method, params=params).fit(train_set_1,
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
