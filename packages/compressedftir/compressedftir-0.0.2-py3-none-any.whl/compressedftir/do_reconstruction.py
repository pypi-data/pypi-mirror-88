import numpy as np
from scipy.sparse import load_npz
from utils import (lr_recon_single, get_regularizer, get_nnz_indices, sum_sq_nnz, get_corner_node)
from datareader import load_data_file
import matplotlib.pyplot as plt
import json
import os

filepath = "Xomega_test.npz"            # sparse samples dataset
exportpath = "test_result/"
export_every_lambda_result = True

Xomega = load_data_file(filepath)       # Get data from file. 

r = 5                                   # desired rank parameter
tau = 1e-5                              # convergence tolerance
lam = np.logspace(-8, 1, num=100)       # L-curve points
max_iter = 20                           # maximal number of local interation

Xh = dict()
res_l = np.zeros(len(lam))
res_g = np.zeros(len(lam))
lcurve = dict()


# data-preprocessing
Z0 = Xomega.toarray()
scl = np.std(Z0, ddof=1)
Xomega = Xomega/scl
nnz = np.nonzero(Z0)

# solver preparation
lapU, lapV = get_regularizer(np.sqrt(Z0.shape[0]), Z0.shape[1], r)
nnzU, nnzV = get_nnz_indices(Z0)
solver_info = {
    "Xomega": Z0,
    "r": r,
    "T": max_iter,
    "tau": tau,
    "lapU": lapU,
    "lapV": lapV,
    "nnz_Z0_U": nnzU,
    "nnz_Z0_V": nnzV
}

if True:
    for lia, l in enumerate(lam):
        curr_path = exportpath + "iter{}/".format(lia)
        with open(curr_path + "result.dat", "r") as fp:
            curr_res = json.load(fp)
        lcurve[lia]= curr_res["lcurve"]

    l_opt = get_corner_node(lcurve)
    fig = plt.figure()
    plt.plot([np.log(lcurve[lia][0]) for lia in range(len(lam))], [np.log(lcurve[lia][1]) for lia in range(len(lam))], '-xb')
    plt.plot(np.log(lcurve[l_opt][0]), np.log(lcurve[l_opt][1]), 'or')
    plt.show()
    exit()


# start iteration over L-curve items
for lia, l in enumerate(lam):
    print("L-curve step: {}/{}".format(lia+1, len(lam)))
    print("Experimental setup:\n lambda: {}\n maximal rank: {}\n convergence tol: {}\n max iteration: {}".format(l, r, tau, max_iter))
    curr_path = exportpath + "iter{}/".format(lia)
    solver_info["l_regu"] = l
    curr_result = lr_recon_single(**solver_info)
    Xh[l] = curr_result["Xh"] * scl
    res_l[lia] = curr_result["resL"]
    res_g[lia] = curr_result["resG"]
    U = curr_result["U"] * np.sqrt(scl)
    V = curr_result["V"] * np.sqrt(scl)
    dd = Xh[l] - Z0
    lcurve[lia] = [sum_sq_nnz(nnz, dd)/sum_sq_nnz(nnz, Z0), U.reshape(-1, order="F").dot(lapU.dot(U.reshape(-1, order="F"))) + V.reshape(-1, order="F").dot(lapV.dot(V.reshape(-1, order="F")))]
    if export_every_lambda_result:
        export_dict = {
            "U": U.tolist(),
            "V": V.tolist(),
            "Z0": Z0.tolist(),
            "lambda": l,
            # "lapU": lapU,
            # "lapV": lapV,
            "lcurve": lcurve[lia]
        }
        
        if not os.path.exists(curr_path):
            os.makedirs(curr_path)        
        with open(curr_path + "result.dat", "w") as fp:
            json.dump(export_dict, fp)
