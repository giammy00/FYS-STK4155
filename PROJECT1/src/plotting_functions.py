import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pathlib
from franke_fit import *
import utils
from mpl_toolkits import mplot3d
import matplotlib

colorpal = sns.color_palette("deep")
sns.set_style('darkgrid') # darkgrid, white grid, dark, white and ticks
plt.rc('axes', titlesize=18)     # fontsize of the axes title
plt.rc('axes', labelsize=14)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=13)    # fontsize of the tick labels
plt.rc('ytick', labelsize=13)    # fontsize of the tick labels
plt.rc('legend', fontsize=13)    # legend fontsize
plt.rc('font', size=13)          # controls default text sizes

def MSE_plot(degrees_list, MSE_train_list, MSE_test_list, mindegree= 0, titles_ = ["MSE"], savefig = False, savename = "MSE", path = "./Plots/MSE"):
    """
    Plots the MSE for test and training and saves figure to path. Can take mulitple data of MSE for
    different runs and will automatically extend the figure and include anohter plot.
    Args:
        degrees_list (ndarray) : 1D containing degrees of complexity for x-axis
        MSE_train_list (ndarray) : Nested array, contains MSE for the train data for y-axis
        MSE_test_list (ndarray) : Nested array, contains MSE for the test data for y-axis
        mindegree = 0 (ndarray) :  Min degree to start x-axis , default = 0
        titles_ (list[string]) : List of titles to apply to figure, default = ["MSE"]
        savefig (bool) : True to save figure, default = False
        savename (string) : Name of file to save, default = "MSE"
        path (string) : Path to save figure, default = "./Plots/MSE"
    """
    fig, axs = plt.subplots(nrows = 1, ncols = len(MSE_train_list), sharey = True, tight_layout=True, figsize=(7*len(MSE_train_list),5))
    plt.gca().set_ylim(bottom=0)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    for i in range(len(MSE_train_list)):
        #A fix for if length is 1 as u cant call upon axs[0]
        if len(MSE_train_list) > 1:
            axs_ = axs[i]
        else:
            axs_ = axs
        axs_.autoscale(enable=True, axis="y", tight=False)
        axs_.plot(degrees_list, MSE_train_list[i][mindegree:], label = "Train", color = colorpal[0])
        axs_.plot(degrees_list, MSE_test_list[i][mindegree:], label = "Test", color = colorpal[1])
        axs_.title.set_text(f"{titles_[i]}")
        axs_.set_xlabel("Order of polynomial")
        axs_.legend()

    if len(MSE_train_list) > 1:
        axs[0].set_ylabel("MSE")
    else:
        axs.set_ylabel("MSE")
    plt.grid(True)
    if savefig:
        plt.savefig(f"{path}/{savename}.pdf", dpi = 300)
    return

def MSE_R2_plot(degrees_list, MSE_train_list, MSE_test_list, R2_train_list, R2_test_list, savefig = False, path = "./Plots/MSER2"):
    """
    Subplot the MSE and R2 score for test and training and saves figure to path if requested.
    Args:
        degrees_list (ndarray) : 1D containing degrees of complexity for x-axis
        MSE_train_list (ndarray) : Contains MSE for the train data for y-axis
        MSE_test_list (ndarray) : Contains MSE for the test data for y-axis
        R2_train_list (ndarray) : Contains R2 scores for the train data for y-axis
        R2_test_list (ndarray) : Contains R2 scores for the test data for y-axis
        savefig (bool) : True to save figure, default = False
        path (string) : Path to save figure, default = "./Plots/MSER2"
    """
    fig, axs = plt.subplots(nrows = 1, ncols = 2, sharey = False, tight_layout=True, figsize=(7*2,5))
    plt.gca().set_ylim(bottom=0)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    #axs.autoscale(enable=True, axis="y", tight=False)
    axs[0].plot(degrees_list, MSE_train_list, label = "Train", color = colorpal[0])
    axs[0].plot(degrees_list, MSE_test_list, label = "Test", color = colorpal[1])
    axs[1].plot(degrees_list, R2_train_list, label = "Train", color = colorpal[0])
    axs[1].plot(degrees_list, R2_test_list, label = "Test", color = colorpal[1])
    for i in range(2):
        axs[i].set_xlabel("Order of polynomial")
        axs[i].legend()
    axs[0].set_ylabel("MSE")
    axs[1].set_ylabel("R2")
    plt.grid(True)
    if savefig:
        plt.savefig(f"{path}/MSER2_OLS.pdf", dpi = 300)
    return

def bias_var_plot(degrees_list, bias, variance, MSE_test_list, savename = "biasvar", savefig = False, path = "./Plots/BiasVar"):
    """
    Plot the bias, variance and error for test and training and saves figure to path if requested.
    Args:
        degrees_list (ndarray) : 1D containing degrees of complexity for x-axis
        bias (ndarray) : Contains the bias for the train data for y-axis
        variance (ndarray) : Contains the variance for the train data for y-axis
        MSE_test_list (ndarray) : Contains the MSE for the test data for y-axis
        savename (string) : : Name of file to save, default = "biasvar"
        savefig (bool) : True to save figure, default = False
        path (string) : Path to save figure, default = "./Plots/BiasVar"
    """
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7,5), tight_layout=True)
    plt.plot(degrees_list, bias, label = "Bias", color = colorpal[0])
    plt.plot(degrees_list, variance, label = "Variance", color = colorpal[1])
    plt.plot(degrees_list, MSE_test_list, label = "MSE", color = colorpal[2])
    plt.xlabel("Order of polynomial")
    plt.ylabel("Numerical estimate")
    plt.grid(True)
    plt.legend()
    if savefig:
        plt.savefig(f"{path}/{savename}.pdf", dpi = 300)
    return

def bias_var_lambdas(degrees_list, lists , lambdas, title = "BiasVar", savefig = False, savename = "fig", path = "./Plots/BiasVarLamb"):
    """
    Plots the bias, variance and error for different lambdas. First plot being with Ridge method and second with Lasso.
    Args:
        degrees_list (ndarray) : 1D containing degrees of complexity for x-axis
        lists (ndarray) : Inludes all the data: bias, variance and error for both methods.
        variance (ndarray) : Contains the variance for the train data for y-axis
        MSE_test_list (ndarray) : Contains the MSE for the test data for y-axis
        savename (string) : : Name of file to save, default = "biasvar"
        savefig (bool) : True to save figure, default = False
        path (string) : Path to save figure, default = "./Plots/BiasVar"
    """
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    fig, axs = plt.subplots(nrows = 1, ncols = 2, sharey = False, tight_layout=True, figsize=(7*2,5))
    linestyles = ["solid", "dotted", "dashed", "dashdot"]
    methods = ['Ridge', 'Lasso']
    for i in range(2):
        for j in range(len(lambdas)):
            axs[i].plot(degrees_list, lists[i][j][0], label = f"$\\lambda$={lambdas[j]}", linestyle=linestyles[0], color = colorpal[j])
            axs[i].plot(degrees_list, lists[i][j][1], linestyle=linestyles[1], color = colorpal[j])
            axs[i].plot(degrees_list, lists[i][j][2], linestyle=linestyles[2], color = colorpal[j])
        axs[i].legend()
        axs[i].set_xlabel("Order of polynomial")
        axs[i].set_yscale("log")

        axs[i].set_title(methods[i])

    if savefig:
        plt.savefig(f"{path}/{savename}.pdf", dpi = 300)
    return

def betaval_plot(degrees_list, beta_mat, nr_ofbeta, maxdeg, title = "Betavalues", savefig = False, path = "./Plots/Betamatrix"):
    """
    Plots the first number of beta values and saves figure.
    Args:
        degrees_list (ndarray) : 1D containing degrees of complexity for x-axis
        beta_mat (ndarray) : Contains the beta matrix
        nr_ofbeta (int) : Number of betas to plot starting with 0.
        maxdeg (int) : Set the max degree for the polynomial to plot
        title (string) : : Title of figure, default = "Betavalues"
        savefig (bool) : True to save figure, default = False
        path (string) : Path to save figure, default = "./Plots/Betamatrix"
    """
    plt.figure(figsize=(7,5), tight_layout=True)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    for i in range(nr_ofbeta):
        plt.plot(degrees_list[:maxdeg], beta_mat[i,:maxdeg], label=f"$\\beta_{i}$", color = colorpal[i])
    plt.grid(True)
    plt.xlabel("Order of polynomial")
    plt.ylabel("Optimal parameter")
    plt.legend()
    if savefig:
        plt.savefig(f"{path}/{title}.pdf", dpi = 300)
    return

def gridsearch_plot(MSE_2d_values, lambda_vals, mindeg, maxdeg, savefig = False, title = "Generic title", savename = "grid", path = "./Plots/Gridsearch"):
    """
    Plots a heatmap showing the MSE values for given different lambdas and degrees of complexity. Saves figure to path.
    Args:
        MSE_2d_values (ndarray) : 2D array which contains the MSE values
        lambda_vals (ndarray) : Contains all the lambda values
        mindeg (int) : Set the min degree for the polynomial to plot
        maxdeg (int) : Set the max degree for the polynomial to plot
        savefig (bool) : True to save figure, default = False
        title (string) : : Title of figure, default = "Generic title"
        savename (string) : Name to which to save the file as, default = "grid"
        path (string) : Path to save figure, default = "./Plots/Gridsearch"
    """
    plt.figure(figsize=(7,5), tight_layout=True)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(MSE_2d_values, columns= lambda_vals, index = np.arange(mindeg, maxdeg+1))
    df.round(2)
    fig = sns.heatmap(df, cbar_kws={'label': 'MSE'})
    fig.set(xlabel="Lambda", ylabel="Order of polynomial")
    plt.title(title)
    if savefig:
        plt.savefig(f"{path}/{savename}.pdf", dpi = 300)
    return
