__all__ = [
    "eval_nls",
    "ev_nls",
]

from grama import add_pipe, pipe, custom_formatwarning, df_make
from grama import eval_df, eval_nominal, eval_monte_carlo
from grama import comp_marginals, comp_copula_independence
from grama import tran_outer
from numpy import Inf, isfinite
from numpy.random import seed as setseed
from pandas import DataFrame, concat
from scipy.optimize import minimize
from toolz import curry

## Nonlinear least squares
# --------------------------------------------------
@curry
def eval_nls(
    model,
    df_data=None,
    out=None,
    var_fix=None,
    append=False,
    tol=1e-6,
    ftol=1e-9,
    gtol=1e-5,
    maxiter=100,
    n_restart=1,
    method="L-BFGS-B",
    seed=None,
):
    r"""Estimate with Nonlinear Least Squares (NLS)

    Estimate best-fit variable levels with nonlinear least squares (NLS).

    Args:
        model (gr.Model): Model to analyze. All model variables
            selected for fitting must be bounded or random. Deterministic
            variables may have semi-infinite bounds.
        df_data (DataFrame): Data for estimating parameters. Variables not
            found in df_data optimized in fitting.
        out (list or None): Output contributions to consider in computing MSE.
            Assumed to be model.out if left as None.
        var_fix (list or None): Variables to fix to nominal levels. Note that
            variables with domain width zero will automatically be fixed.
        append (bool): Append metadata? (Initial guess, MSE, optimizer status)
        tol (float): Optimizer convergence tolerance
        maxiter (int): Optimizer maximum iterations
        n_restart (int): Number of restarts; beyond n_restart=1 random
            restarts are used.
        seed (int OR None): Random seed for restarts

    Returns:
        DataFrame: Results of estimation

    Examples:
        >>> import grama as gr
        >>> from grama.data import df_trajectory_full
        >>> from grama.models import make_trajectory_linear
        >>>
        >>> md_trajectory = make_trajectory_linear()
        >>>
        >>> df_fit = (
        >>>     md_trajectory
        >>>     >> gr.ev_nls(df_data=df_trajectory_full)
        >>> )
        >>>
        >>> print(df_fit)

    """
    ## Check `out` invariants
    if out is None:
        out = model.out
        print("... eval_nls setting out = {}".format(out))
    set_diff = set(out).difference(set(df_data.columns))
    if len(set_diff) > 0:
        raise ValueError(
            "out must be subset of df_data.columns\n"
            + "difference = {}".format(set_diff)
        )

    ## Determine variables to be fixed
    if var_fix is None:
        var_fix = set()
    else:
        var_fix = set(var_fix)
    for var in model.var_det:
        wid = model.domain.get_width(var)
        if wid == 0:
            var_fix.add(var)
    print("... eval_nls setting var_fix = {}".format(list(var_fix)))

    ## Determine variables for evaluation
    var_feat = set(model.var).intersection(set(df_data.columns))
    print("... eval_nls setting var_feat = {}".format(list(var_feat)))

    ## Determine variables for fitting
    var_fit = set(model.var).difference(var_fix.union(var_feat))
    if len(var_fit) == 0:
        raise ValueError(
            "No var selected for fitting!\n"
            + "Try checking model bounds and df_data.columns."
        )

    ## Separate var_fit into det and rand
    var_fit_det = list(set(model.var_det).intersection(var_fit))
    var_fit_rand = list(set(model.var_rand).intersection(var_fit))

    ## Construct bounds, fix var_fit order
    var_fit = var_fit_det + var_fit_rand
    bounds = []
    var_prob = []
    for var in var_fit_det:
        if not isfinite(model.domain.get_nominal(var)):
            var_prob.append(var)
        bounds.append(model.domain.get_bound(var))
    if len(var_prob) > 0:
        raise ValueError(
            "all variables to be fitted must finite nominal value\n"
            + "offending var = {}".format(var_prob)
        )

    for var in var_fit_rand:
        bounds.append(
            (model.density.marginals[var].q(0), model.density.marginals[var].q(1),)
        )

    ## Determine initial guess points
    df_nom = eval_nominal(model, df_det="nom", skip=True)

    df_init = df_nom[var_fit]
    if n_restart > 1:
        if not (seed is None):
            setseed(seed)
        ## Collect sweep-able deterministic variables
        var_sweep = list(
            filter(
                lambda v: isfinite(model.domain.get_width(v))
                & (model.domain.get_width(v) > 0),
                model.var_det,
            )
        )
        ## Generate pseudo-marginals
        dicts_var = {}
        for v in var_sweep:
            dicts_var[v] = {
                "dist": "uniform",
                "loc": model.domain.get_bound(v)[0],
                "scale": model.domain.get_width(v),
            }
        ## Overwrite model
        md_sweep = comp_marginals(model, **dicts_var)
        md_sweep = comp_copula_independence(md_sweep)
        ## Generate random start points
        df_rand = eval_monte_carlo(
            md_sweep,
            n=n_restart - 1,
            df_det="nom",
            skip=True,
        )
        df_init = concat(
            (df_init, df_rand[var_fit]),
            axis=0
        )

    ## Iterate over initial guesses
    df_res = DataFrame()

    for i in range(n_restart):
        x0 = df_init[var_fit].iloc[i].values
        ## Build evaluator
        def objective(x):
            """x = [var_fit]"""
            ## Evaluate model
            df_var = tran_outer(
                df_data[var_feat],
                concat(
                    (df_nom[var_fix].iloc[[0]], df_make(**dict(zip(var_fit, x)))),
                    axis=1,
                ),
            )
            df_tmp = eval_df(model, df=df_var)

            ## Compute joint MSE
            return ((df_tmp[out].values - df_data[out].values) ** 2).mean()

        ## Run optimization
        res = minimize(
            objective,
            x0,
            args=(),
            method=method,
            jac=False,
            tol=tol,
            options={
                "maxiter": maxiter,
                "disp": False,
                "ftol": ftol,
                "gtol": gtol,
            },
            bounds=bounds,
        )

        ## Package results
        df_tmp = df_make(
            **dict(zip(var_fit, res.x)),
            **dict(zip(map(lambda s: s + "_0", var_fit), x0)),
        )
        df_tmp["success"] = [res.success]
        df_tmp["message"] = [res.message]
        df_tmp["n_iter"] = [res.nit]
        df_tmp["mse"] = [res.fun]

        df_res = concat(
            (
                df_res,
                df_tmp,
            ),
            axis=0,
        ).reset_index(drop=True)

    ## Post-process
    if append:
        return df_res
    else:
        return df_res[var_fit]


ev_nls = add_pipe(eval_nls)
