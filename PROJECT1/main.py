import sys, os
sys.path.insert(1, './src') #Search the src folder for the modules
import plotting_functions as plotfnc
from franke_fit import *
import numpy as np
import matplotlib.pyplot as plt
import utils


def generate_reults(showfigs = False):
    """
    Generate all the results for FrankeFunction shown in report. Figures will be saved
    to folder ./Plots in different subdirectories depending on the plottingfunction being used.

    Figures are generated in the order:
    - MSE and R2 scores as function of the polynomial degree, OLS
    - beta parameters, as function of polydeg, OLS
    - Bias-variance tradeoff, as function of polydeg using only bootstrap, and only OLS
    - Comparison between estimates of MSE in crossval and bootstrap, OLS. 2 plots to reuse plotting func
    - Crossvalidation with k-fold gridsearch with ridge and lasso. MSE score
    - No resampling gridsearch with ridge and lasso. MSE score
    - Bias variance tradeoff. Using ridge and lasso, both with bootstrap.

    Args:
        showfigs (bool) : Set True to display all figures that are generated, default = False
    """
    methods = [OLS, Ridge, Lasso]
    np.random.seed(3463223)
    np.random.seed(133)
    # Make data.
    Nx_ = 16
    Ny_ = 16
    maxdeg = 12
    #generate x,y data from uniform distribution
    x__ = np.random.rand(Nx_, 1)
    y__ = np.random.rand(Ny_, 1)
    x_, y_ = np.meshgrid(x__,y__)
    z_ = (utils.FrankeFunction(x_, y_) + 0.1*np.random.randn(Nx_,Ny_)).reshape(-1,1)

    #1 MSE AND R2 SCORES AS FUNCTION OF THE POLYNOMIAL DEGREE, OLS
    maxdeg = 11
    print("Plotting MSE and R2 score for OLS.")
    list_train = []
    test = []
    degrees_list, MSE_train_list, MSE_test_list, _, _, _, R2_train_list, R2_test_list, _ \
    = Solver(x_, y_, z_, Nx_, Ny_, OLS, lamb = 0, useBootstrap=False, useCrossval=False, maxdegree = maxdeg)
    plotfnc.MSE_R2_plot(degrees_list, MSE_train_list, MSE_test_list, R2_train_list, R2_test_list, savefig = True)

    # (2) BETA PARAMETERS, AS FUNCTION OF POLYDEG, OLS
    #Betamatrix plot
    print("Plotting betavalues, OLS.")
    deg_toplot = 6
    nr_of_betas = 6
    degrees_list, MSE_train_list, MSE_test_list, bias, variance, beta_matrix, _, _, _ = Solver(x_, y_, z_, Nx_, Ny_, OLS, useBootstrap=False, useCrossval=False, lamb=0.0001, maxdegree = maxdeg)
    plotfnc.betaval_plot(degrees_list, beta_matrix, nr_of_betas, maxdeg = deg_toplot, title = f"Betavalues_{nr_of_betas}", savefig = True)

    #(3) Bias-variance tradeoff, AS FUNCTION OF POLYDEG USING ONLY BOOTSTRAP, and only OLS
    print("Plotting biasvariance tradeoff, OLS w/bootstrap.")
    maxdeg_ = 10
    degrees_list, MSE_train_list, MSE_test_list, bias, variance, beta_matrix, R2_train_list, R2_test_list, z_pred \
    = Solver(x_, y_, z_, Nx_, Ny_, OLS, lamb = 0, useBootstrap=True, useCrossval=False, maxdegree = maxdeg_)
    plotfnc.bias_var_plot(degrees_list, bias, variance, MSE_test_list, savename = "biasvar_bootOLS",  savefig = True)

    #(4)COMPARISON BETWEEN ESTIMATES OF MSE IN CROSSVAL AND BOOTSTRAP, OLS. 2 plots to reuse plotting func
    #Bootstrap value goes a bit crazy for higher complexity.
    print("Plotting MSE for OLS w/boot and w/crossval.")
    maxdeg = 11
    MSE_list_train = []
    MSE_list_test = []
    titles = ["Bootstrap", "Cross-validation"]

    degrees_list, MSE_tr_boot, MSE_te_boot, _, _, _, _, _, _ \
    = Solver(x_, y_, z_, Nx_, Ny_, OLS, lamb = 0, useBootstrap=True, useCrossval=False, maxdegree = maxdeg)
    MSE_list_train.append(MSE_tr_boot)
    MSE_list_test.append(MSE_te_boot)

    degrees_list, MSE_tr_cross, MSE_te_cross, _, _, _, _, _, _ \
    = Solver(x_, y_, z_, Nx_, Ny_, OLS, lamb = 0, useBootstrap=False, useCrossval=True, maxdegree = maxdeg)
    MSE_list_train.append(MSE_tr_cross)
    MSE_list_test.append(MSE_te_cross)

    plotfnc.MSE_plot(degrees_list, MSE_list_train, MSE_list_test, titles_ = titles, savename = "bootcross", savefig = True)

    #(5) Crossvalidation with k-fold gridsearch with ridge and lasso. MSE score
    print("Plotting gridsearch MSE, ridge and lasso with crossval.")
    lambda_vals = np.logspace(-6, 0, 7)
    mindeg = 3
    maxdeg = 10
    method = Ridge
    MSE_2d = np.zeros(shape=(maxdeg+1-mindeg ,len(lambda_vals)))
    #Fill array with MSE values. x-axis lambda, y-axis degree
    for i in range(len(lambda_vals)):
        degrees_list, MSE_train_list, MSE_test_list, _, _, _, _, _, _ = \
        Solver(x_, y_, z_, Nx_, Ny_, Ridge, useBootstrap=False, useCrossval=True, lamb=lambda_vals[i], mindegree = mindeg, maxdegree = maxdeg)
        for j in range(maxdeg-mindeg+1):
            MSE_2d[j,i] = MSE_test_list[j] #fix indexing cause of length
    plotfnc.gridsearch_plot(MSE_2d, lambda_vals, mindeg, maxdeg, title = "Ridge", savename="Ridge_crossval_grid", savefig = True)

    maxdeg = 20
    lambda_vals = np.logspace(-7, -3, 5)
    method = Lasso
    MSE_2d = np.zeros(shape=(maxdeg+1-mindeg ,len(lambda_vals)))
    #Fill array with MSE values. x-axis lambda, y-axis degree
    for i in range(len(lambda_vals)):
        degrees_list, MSE_train_list, MSE_test_list, _, _, _, _, _, _ = \
        Solver(x_, y_, z_, Nx_, Ny_, method, useBootstrap=False, useCrossval=True, lamb=lambda_vals[i], mindegree = mindeg, maxdegree = maxdeg)
        for j in range(maxdeg-mindeg+1):
            MSE_2d[j,i] = MSE_test_list[j] #fix indexing cause of length
    plotfnc.gridsearch_plot(MSE_2d, lambda_vals, mindeg, maxdeg, title = "Lasso", savename="Lasso_crossval_grid", savefig = True)

    #(6) No resampling gridsearch with ridge and lasso. MSE score
    print("Plotting gridsearch MSE, ridge and lasso.")
    maxdeg = 13
    crossval = True
    lambda_vals = np.logspace(-6, 0, 7)
    method = Ridge
    MSE_2d = np.zeros(shape=(maxdeg+1-mindeg ,len(lambda_vals)))
    #Fill array with MSE values. x-axis lambda, y-axis degree
    for i in range(len(lambda_vals)):
        degrees_list, MSE_train_list, MSE_test_list, _, _, _, _, _, _ = \
        Solver(x_, y_, z_, Nx_, Ny_, Ridge, useBootstrap=False, useCrossval=False, lamb=lambda_vals[i], mindegree = mindeg, maxdegree = maxdeg)
        for j in range(maxdeg-mindeg+1):
            MSE_2d[j,i] = MSE_test_list[j] #fix indexing cause of length
    plotfnc.gridsearch_plot(MSE_2d, lambda_vals, mindeg, maxdeg, title = "Ridge", savename="Ridge_grid", savefig = True)

    maxdeg = 14
    lambda_vals = np.logspace(-7, -3, 5)
    method = Lasso
    MSE_2d = np.zeros(shape=(maxdeg+1-mindeg ,len(lambda_vals)))
    #Fill array with MSE values. x-axis lambda, y-axis degree
    for i in range(len(lambda_vals)):
        degrees_list, MSE_train_list, MSE_test_list, _, _, _, _, _, _ = \
        Solver(x_, y_, z_, Nx_, Ny_, method, useBootstrap=False, useCrossval=False, lamb=lambda_vals[i], mindegree = mindeg, maxdegree = maxdeg)
        for j in range(maxdeg-mindeg+1):
            MSE_2d[j,i] = MSE_test_list[j] #fix indexing cause of length
    plotfnc.gridsearch_plot(MSE_2d, lambda_vals, mindeg, maxdeg, title = "Lasso", savename="Lasso_grid", savefig = True)

    #7 Bias variance tradeoff. Using ridge and lasso, both with bootstrap.
    print("Plotting bias variance with ridge and lasso using bootstrap.")
    lambda_vals = np.array([1e-5, 1e-1,  50 ])
    lists = [ [], [] ]
    mindeg = 1
    maxdeg = 8
    i = 0

    for lambda_ in lambda_vals:
        for jj, method in enumerate([Ridge, Lasso]):
            degrees_list, MSE_train_list, MSE_test_list, bias, variance, _, _, _, _ = \
            Solver(x_, y_, z_, Nx_, Ny_, method, useBootstrap=True, useCrossval=False, lamb=lambda_, mindegree = mindeg, maxdegree = maxdeg)
            lists[jj].append([MSE_test_list, bias, variance])
    plotfnc.bias_var_lambdas(degrees_list, lists, lambda_vals, savename="biasvarname", savefig=True)

    #Finished
    print("Finished all results for FrankeFunction. ")
    col = os.get_terminal_size()[0]
    print("-"*col + "\n")
    if showfigs:
        plt.show()

    return


def get_bool(var):
    """
    Simple function to evaluate answer from y(yes) or n(no) paramter.
    Args:
        var (string) : Answer to be interpreted
    Returns:
        val_ (bool) : True if answer is y, flase if n or exits program if not either.
    """
    if var == "y":
        var_ = True
    elif var == "n":
        var_ = False
    else:
        sys.exit("Wrong input, must be 'y' or 'n'. Exiting run. ")
    return var_

def main():
    """
    Asks if user wants to generate figures and plot.
    Simply answer y or n. 
    """
    #Run to generate all the plots using the frankie function.
    bool_gen = input("Do you want to generate all figures for FrankeFunction? (y/n)")
    bool_gen = get_bool(bool_gen)
    if bool_gen:
        showfigs_ = input("Do you want to show all figures? (y/n)")
        bool_show = get_bool(showfigs_)
        print("")
        generate_reults(showfigs = bool_show)

    #Plot whatever you want.
    #gen x, y ,z data
    # Call on solver with parameters
    # Call on what to plot.
    return

if __name__ == "__main__":
    main()
