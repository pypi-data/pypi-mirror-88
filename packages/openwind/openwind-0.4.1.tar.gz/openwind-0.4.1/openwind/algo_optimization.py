#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
              "Alexis Thibault", "Tobias Van Baarsel"]
__copyright__ = "Copyright 2020, Inria"
__credits__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
               "Alexis Thibault", "Tobias Van Baarsel"]
__license__ = "GPL 3.0"
__version__ = "0.4.1"
__email__ = "openwind-contact@inria.fr"
__status__ = "Dev"

import numpy as np
import pdb

def stop_message(iteropt, max_iter, cost, step_cost, minstep_cost, gradient,
                 tresh_grad):
    if np.max(np.abs(gradient)) <= tresh_grad:
        print('Algorithm stops: the gradient is below the tolerance treshold ({:.2e})'.format(tresh_grad))
    elif step_cost <= minstep_cost:
        print('Algorithm stops: the cost variation is below the tolerance treshold ({:.2e})'.format(minstep_cost))
    else:
        print('Algorithm stops: the maximum iteration number has been reached ({:d})'.format(max_iter))
    print(('    Iterations:{:d} \n    Final cost = {:.2e} \n    '
           'Norm of gradient = {:.2e}').format(iteropt, cost, np.linalg.norm(gradient)))


def print_cost(index_iter, cost, gradient):
    norm_grad = np.linalg.norm(gradient)
    # print('Iteration {:d}; Cost={:.8e}; Gradient={:.8e}'.format(index_iter, cost, norm_grad))
    if index_iter % 20 == 0:
        print('{:<12}{:<16}{:<16}'.format('Iteration','Cost','Gradient'))
    print('{:<12d}{:<16.8e}{:<16.8e}'.format(index_iter, cost, norm_grad))



def __hessianFiniteDiff(get_cost_grad, params_values, stepSize=1e-8):
    Nderiv = len(params_values)
    hessFor = np.zeros((Nderiv, Nderiv))
    hessBack = np.zeros((Nderiv, Nderiv))

    _, grad_init = get_cost_grad(params_values)
    params_init = np.array(params_values, copy=True)
    params = np.array(params_values, copy=True)
    for diff_index in range(Nderiv):
        params[diff_index] = params_init[diff_index] + stepSize
        _, gradFor = get_cost_grad(params)
        hessFor[diff_index, :] = (gradFor - grad_init) / stepSize

        params[diff_index] = params_init[diff_index] - stepSize
        _, gradBack = get_cost_grad(params)
        hessBack[diff_index, :] = (grad_init - gradBack) / stepSize

        params[diff_index] = params_init[diff_index]
    get_cost_grad(params_init)
#    pdb.set_trace()
    return (hessFor + hessBack) / 2


def __hessianBFGS(x0, x1, grad, Bk):
    # equation 6.19 du Nocedal
    sk = x1 - x0
    yk = grad[1] - grad[0]
    sk = sk[:, np.newaxis]
    yk = yk[:, np.newaxis]
    num1 = Bk.dot(sk.dot(sk.T.dot(Bk.T)))
    den1 = sk.T.dot(Bk.dot(sk))
    num2 = yk.dot(yk.T)
    den2 = yk.T.dot(sk)

    Bnew = Bk - num1/den1 + num2/den2
    return Bnew


def __inv__hessianBFGS(x0, x1, grad, Hk):
    # equation 6.17 du Nocedal
    sk = x1 - x0
    yk = grad[1] - grad[0]
    sk = sk[:, np.newaxis]
    yk = yk[:, np.newaxis]
    rho = 1/(yk.T.dot(sk))
    A = np.eye(Hk.shape[0]) - rho * (sk.dot(yk.T))
    Hnew = A.dot(Hk.dot(A)) + rho * (sk.dot(sk.T))
    return Hnew


def __backtracking(get_cost_grad, params_old, direction, cost_old, phi_prime):
    alpha_0 = 1
    rho = 0.75
    c = 1e-3

    alpha = alpha_0
    kadapt = 0
    delta_f = c * phi_prime
    params_new = params_old + alpha * direction
    cost_new, _ = get_cost_grad(params_new)
    while cost_new > cost_old + alpha * delta_f and kadapt < 100:
        kadapt = kadapt + 1
        alpha = alpha * rho
        params_new = params_old + alpha * direction
        cost_new, _ = get_cost_grad(params_new)
    return params_old + alpha/rho * direction  # penultimate step


def __linesearch(get_cost_grad, params_old, direction, phi, phi_prime):
    #  linesearch algorithm 3.5 from Nocedal
    c1 = 1e-4  # 1e-3
    c2 = 0.9
    alpha_def = 1  # default value for QuasiNewton

    alpha_k = 0
    alpha_k = np.append(alpha_k, alpha_def)
    alpha_max = 10
    kadapt = 1
    alphaStar = []

    while not alphaStar:
        params_new = params_old + alpha_k[kadapt] * direction
        cost_new, grad_new = get_cost_grad(params_new)

        phi = np.append(phi, cost_new)
        phi_prime = np.append(phi_prime, grad_new @ direction)
        if (phi[kadapt] > phi[0] + c1*alpha_k[kadapt]*phi_prime[0] or
           (phi[kadapt] >= phi[kadapt-1] and kadapt > 1)):
            alphaStar = __zoomLinesearch(get_cost_grad, kadapt-1, kadapt,
                                         alpha_k, phi, phi_prime, direction,
                                         params_old, c1, c2)
        elif np.abs(phi_prime[kadapt]) <= -c2*phi_prime[0]:
            alphaStar = alpha_k[kadapt]
        elif phi_prime[kadapt] >= 0:
            alphaStar = __zoomLinesearch(get_cost_grad, kadapt, kadapt-1,
                                         alpha_k, phi, phi_prime, direction,
                                         params_old, c1, c2)
        else:
            alpha_k = np.append(alpha_k, 0.5*(alpha_k[kadapt]+alpha_max))
            kadapt = kadapt + 1

        if kadapt >= 100:
            raise ValueError("Linesearch failed to find the step length.")

    return params_old + alphaStar * direction


def __zoomLinesearch(get_cost_grad, k_lo, k_hi, alpha_k, phi, phi_prime,
                     direction, params_optim, c1, c2):
    a_lo = alpha_k[k_lo]
    a_hi = alpha_k[k_hi]
    phi_lo = phi[k_lo]
    alphaStar = []
    niter = 0
    while not alphaStar and niter < 100:
        niter = niter+1
        a_j = 0.5*(a_lo + a_hi)
        params_j = params_optim + a_j * direction
        cost_j, grad_j = get_cost_grad(params_j)

        if cost_j > phi[0] + c1*a_j*phi_prime[0] or (cost_j >= phi_lo):
            a_hi = a_j
        else:
            if np.abs(grad_j @ direction) <= -c2*phi_prime[0]:
                alphaStar = a_j
            elif (grad_j @ direction)*(a_hi - a_lo) >= 0:
                a_hi = a_lo
            a_lo = a_j
            phi_lo = cost_j
    if not alphaStar:
        alphaStar = a_j
    return alphaStar


def _search_step_length(get_cost_grad, params_old, direction, cost_old,
                        gradient_old, steptype='linesearch'):
    phi_prime = gradient_old @ direction
    if steptype == 'backtracking':
        newparams = __backtracking(get_cost_grad, params_old,
                                   direction, cost_old, phi_prime)
    else:
        newparams = __linesearch(get_cost_grad, params_old,
                                 direction, cost_old, phi_prime)
    return newparams


# %% Algorithms
def _linesearch_algorithm(get_cost_grad_direction, get_cost_grad,
                          initial_params, max_iter=100, minstep_cost=1e-8,
                          tresh_grad=1e-10, iter_detailed=False,
                          steptype='linesearch', hessiantype=None):
    step_cost = np.inf
    iteropt = 0

    if hessiantype == 'BFGS':
        cost, gradient, direction, Hk = get_cost_grad_direction(initial_params,
                                                                0., 0., 0., 0.)
    else:
        cost, gradient, direction = get_cost_grad_direction(initial_params)

    params_evol = [np.array(initial_params)]
    cost_evol = [cost]
    if iter_detailed:
        print_cost(iteropt,cost, gradient)
    while (iteropt < max_iter and step_cost > minstep_cost
           and np.linalg.norm(gradient) > tresh_grad):
        iteropt = iteropt + 1
        newparams = _search_step_length(get_cost_grad, params_evol[iteropt-1],
                                        direction, cost, gradient,
                                        steptype=steptype)
        if hessiantype == 'BFGS':
            (cost, gradient, direction,
             Hk) = get_cost_grad_direction(newparams, params_evol[-1],
                                           gradient, iteropt, Hk)
        else:
            cost, gradient, direction = get_cost_grad_direction(newparams)

        params_evol.append(newparams)
        cost_evol.append(cost)
        if iter_detailed:
            print_cost(iteropt, cost, gradient)
        step_cost = np.abs(cost_evol[-2] - cost_evol[-1])/cost_evol[-1]

    stop_message(iteropt, max_iter, cost, step_cost, minstep_cost, gradient,
                 tresh_grad)
    return params_evol, cost_evol


def QuasiNewtonBFGS(get_cost_grad, initial_params, max_iter=100,
                    minstep_cost=1e-8, tresh_grad=1e-10, iter_detailed=False,
                    steptype='linesearch'):

    def get_cost_grad_direction(x, x0, old_grad, iteropt, old_Hk):
        cost, gradient = get_cost_grad(x)
        if np.mod(iteropt, 10) == 0:
            hessian = __hessianFiniteDiff(get_cost_grad, x)
            try:
                Hk = np.linalg.inv(hessian)
            except:
                Hk = np.eye(len(hessian))
        else:
#            hessian = __hessianBFGS(x0, x, [old_grad, gradient], np.linalg.inv(old_Hk))
            Hk = __inv__hessianBFGS(x0, x, [old_grad, gradient], old_Hk)
        direction = -1 * Hk.dot(gradient)
        if (gradient @ direction) >= 0:
            direction = -1*gradient
        return cost, gradient, direction, Hk

    return _linesearch_algorithm(get_cost_grad_direction, get_cost_grad,
                                 initial_params, max_iter, minstep_cost,
                                 tresh_grad, iter_detailed, steptype,
                                 hessiantype='BFGS')


def Steepest(get_cost_grad, initial_params, max_iter=100, minstep_cost=1e-8,
             tresh_grad=1e-10, iter_detailed=False,
             steptype='linesearch'):

    def get_cost_grad_direction(x):
        cost, gradient = get_cost_grad(x)
        direction = -1 * gradient
        return cost, gradient, direction

    return _linesearch_algorithm(get_cost_grad_direction, get_cost_grad,
                                 initial_params, max_iter, minstep_cost,
                                 tresh_grad, iter_detailed, steptype)


def GaussNewton(get_cost_grad_hessian, initial_params, max_iter=100,
                minstep_cost=1e-8, tresh_grad=1e-10, iter_detailed=False):

    def get_cost_grad(x):
        cost, gradient, _ = get_cost_grad_hessian(x)
        return cost, gradient

    def get_cost_grad_direction(x):
        cost, gradient, hessian = get_cost_grad_hessian(x)
        direction = np.linalg.solve(hessian, -1 * gradient)
        if (gradient @ direction) >= 0:
            direction = -1*gradient
        return cost, gradient, direction

    return _linesearch_algorithm(get_cost_grad_direction, get_cost_grad,
                                 initial_params, max_iter, minstep_cost,
                                 tresh_grad, iter_detailed)


def LevenbergMarquardt(get_cost_grad_hessian, initial_params, max_iter=100,
                       minstep_cost=1e-8, tresh_grad=1e-10,
                       iter_detailed=False):
    method = '3'
    if method == '1':
        # cf document by H.P. Gavin method 1
        lambdaMin = 1e-10  # 1e-7??
        lambdamax = 1e10
        Lup = 11
        Ldown = 9

        def one_step_LM(hessian, lambda0, minusgrad):
            diag_hess = np.diag(hessian)
            direction = np.linalg.solve(hessian + lambda0*diag_hess
                                        * np.identity(Nparam),
                                        minusgrad)  # eq(13)
            params_test = params_evol[-1] + direction
            cost, gradient, hessian = get_cost_grad_hessian(params_test)
            DeltaCost = cost_evol[-1] - cost
            rho = (DeltaCost) / (direction @ (lambda0 * diag_hess * direction
                                              + minusgrad))  # eq(16)
            if rho > eps_4:
                lambda0 = np.maximum(lambda0/Ldown, lambdaMin)
            else:
                lambda0 = np.minimum(lambda0*Lup, lambdamax)
            return params_test, cost, gradient, hessian, rho, lambda0

    elif method == '2':
        # cf document by H.P. Gavin method 2
        lambdaMin = 1e-10

        def one_step_LM(hessian, lambda0, minusgrad):
            direction = np.linalg.solve(hessian + lambda0*np.identity(Nparam),
                                        minusgrad)  # eq(12)
            params_test = params_evol[-1] + direction
            cost, _, _ = get_cost_grad_hessian(params_test)
            alpha = minusgrad @ direction / ((cost - cost_evol[-1])/2
                                             + 2 * minusgrad @ direction)
            params_test = params_evol[-1] + alpha * direction
            cost, gradient, hessian = get_cost_grad_hessian(params_test)
            DeltaCost = cost_evol[-1] - cost
            rho = (DeltaCost) / (alpha*direction @ (lambda0*alpha*direction
                                                    + minusgrad))  # eq(15)
            if rho > eps_4:
                lambda0 = np.maximum(lambda0/(1 + alpha), lambdaMin)
            else:
                lambda0 = lambda0 + np.abs(DeltaCost)/(2*alpha)
            return params_test, cost, gradient, hessian, rho, lambda0

    elif method == '3':
        # cf document by H.P. Gavin method 3
        def one_step_LM(hessian, lambda0, minusgrad):
            direction = np.linalg.solve(hessian + lambda0*np.identity(Nparam),
                                        minusgrad)  # eq(12)
            params_test = params_evol[-1] + direction

            cost, gradient, hessian = get_cost_grad_hessian(params_test)

            DeltaCost = cost_evol[-1] - cost
            rho = DeltaCost/(direction @ (lambda0*direction
                                          + minusgrad))  # eq(15)
            if rho > eps_4:
                lambda0 = lambda0 * np.maximum(1/3, 1 - (2 * rho - 1)**3)
            else:
                lambda0 = lambda0 * nui
            return params_test, cost, gradient, hessian, rho, lambda0

    Nparam = len(initial_params)
    lambda0 = 1e-8  # 1e-5 #
    eps_4 = 0 #1e-1
    step_cost = np.inf
    rho = np.inf
    iteropt = 0
    nui = 2

    params_evol = [np.array(initial_params)]
    cost, gradient, hessian = get_cost_grad_hessian(params_evol[iteropt])
    if iter_detailed:
        print_cost(iteropt, cost, gradient)
    cost_evol = [cost]
    minusgrad = -1 * gradient

    if method == '2' or method == '3':
        lambda0 = lambda0*np.max(np.diag(hessian))

    while iteropt < max_iter and ( rho <= eps_4 or (step_cost > minstep_cost
                                                   and np.linalg.norm(gradient) > tresh_grad)):
        iteropt = iteropt + 1
        (new_param, cost, gradient,
         hessian, rho, lamda0) = one_step_LM(hessian, lambda0, minusgrad)
        # if iter_detailed:
        #         print_cost(iteropt, cost, gradient)
        #         print('This is rho: {:.2e}'.format(rho))
        if rho > eps_4:
            nui = 2
            minusgrad = -1 * gradient
            cost_evol.append(cost)
            params_evol.append(new_param)
            step_cost = (cost_evol[-2] - cost_evol[-1])/cost_evol[-1]
            if iter_detailed:
                print_cost(iteropt, cost, gradient)
        else:
            nui = 2*nui

    _, _, _ = get_cost_grad_hessian(params_evol[-1])
    stop_message(iteropt, max_iter, cost, step_cost, minstep_cost, gradient,
                 tresh_grad)
    return params_evol, cost_evol


#def optimize_freq_model(InverseFrequentialResponse, algorithm='LM',
#                        max_iter=100, minstep_cost=1e-8, tresh_grad=1e-10,
#                        iter_detailed=False, steptype='linesearch'):
#
#    inv_freq = InverseFrequentialResponse
#    initial_params = inv_freq.optim_params.values
#
#    def get_cost_grad_hessian(x):
#        return inv_freq.get_cost_grad_hessian(x, grad_type='frechet')
#
#    def get_cost_grad(x):
#        return inv_freq.get_cost_grad_hessian(x, grad_type='adjoint')[0:2]
#
#    if algorithm == 'LM':
#        params_evol, cost_evol = LevenbergMarquardt(get_cost_grad_hessian,
#                                                    initial_params, max_iter,
#                                                    minstep_cost, tresh_grad,
#                                                    iter_detailed)
#    elif algorithm == 'steepest':
#        params_evol, cost_evol = Steepest(get_cost_grad, initial_params, max_iter,
#                                          minstep_cost, tresh_grad,
#                                          iter_detailed, steptype)
#    elif algorithm == 'QN':
#        params_evol, cost_evol = QuasiNewtonBFGS(get_cost_grad, initial_params,
#                                                 max_iter, minstep_cost,
#                                                 tresh_grad, iter_detailed,
#                                                 steptype)
#    elif algorithm == 'GN':
#        params_evol, cost_evol = GaussNewton(get_cost_grad_hessian,
#                                             initial_params, max_iter,
#                                             minstep_cost, tresh_grad,
#                                             iter_detailed)
#    else:
#        print("""Unknown algorithm, choose between:
#            LM (Levenberg-Marquardt); steepest; QN (Quasi-Newton);
#            GN (Gauss-Newton)""")
#
#    inv_freq.get_cost_grad_hessian(params_evol[-1])
#    return params_evol, cost_evol
