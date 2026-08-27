import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize as opt
from statsmodels.formula.api import ols

import DataFrames as dfs
import Enums as en

import sys


#%% MY MODELS

def lin(x, a, b):
    return a*x + b
def quad(x, a, b, c):
    return a*x**2 + b*x + c

#%% GOODNESS

def RESIDUALS(data, model):
    return np.square(data - model)
def RSS(x, data, model):
    residuals = np.square(data - model)
    return np.sum(RESIDUALS(data, model))
def RMSE(x, data, model):
    return np.sqrt(np.mean(RESIDUALS(data, model)))    
def R_SQUARED(x, data, model):
    _var = np.sum(np.square(data - np.mean(data)))
    _rss = RSS(x, data, model)
    return 1 - (_rss / _var)

#%% HELPERS

def toDate(year):
    return pd.to_datetime(year, format="%Y")

#%% GET DFS

df_temp = dfs.Get_MeanTemp(en.Region.World)
df_temp.reset_index()

#%% LINEAR MODELING, GOODNESS, PARAM ERRORS, MODEL BOUNDS

# RSS, RMSE, rSquared, std error

x = df_temp["year"]
yData = df_temp["avgtemp"]

# guess params
linParam_a_guess = 0.01
linParam_b_guess = -19

# get ols params
olsModel_linFit = ols(formula="avgtemp ~ year", data=df_temp).fit()
linParam_a_ols = olsModel_linFit.params["year"]
linParam_b_ols = olsModel_linFit.params["Intercept"]
# get ols param errors
linParam_a_ols_err = olsModel_linFit.bse["year"]
linParam_b_ols_err = olsModel_linFit.bse["Intercept"]

# goodness of model - guess
y_linModel_guess = lin(x, linParam_a_guess, linParam_b_guess)
lin_myModel_rss = RSS(x, yData, y_linModel_guess)
lin_myModel_rmse = RMSE(x, yData, y_linModel_guess)
lin_myModel_rSquared = R_SQUARED(x, yData, y_linModel_guess)
# goodness of model - ols
y_linModel_ols = lin(x, linParam_a_ols, linParam_b_ols)
lin_olsModel_rss = RSS(x, yData, y_linModel_ols)
lin_olsModel_rmse = RMSE(x, yData, y_linModel_ols)
lin_olsModel_rSquared = R_SQUARED(x, yData, y_linModel_ols)

# param bounds
y_lin_olsModel_bound1 = lin(x, 
                          linParam_a_ols+linParam_a_ols_err, 
                          linParam_b_ols-linParam_b_ols_err)
y_lin_olsModel_bound2 = lin(x, 
                          linParam_a_ols-linParam_a_ols_err, 
                          linParam_b_ols+linParam_b_ols_err)

# compare my and ols model
goodness = {
    "model": ["lin_guess", "lin_ols"],
    "params": [(linParam_a_guess,linParam_b_guess), 
                  (f"{round(linParam_a_ols, 4)} +- {round(linParam_a_ols_err, 4)}",
                   f"{round(linParam_b_ols, 4)} +- {round(linParam_b_ols_err, 4)}")],
    "RSS": [round(lin_myModel_rss,4),round(lin_olsModel_rss,4), ],
    "RMSE": [round(lin_myModel_rmse,4),round(lin_olsModel_rmse,4)],
    "RSQUARED": [round(lin_myModel_rSquared,4),round(lin_olsModel_rSquared,4)],
    }

print("\n\t- Goodness linear models -")
print(pd.DataFrame(goodness).set_index("model"))

#%% OLS MODEL OF HIGHER ORDER

# get params
olsModel_quadFit = ols(formula="avgtemp ~ year + I(year**2)", data=df_temp).fit()
quadParam_c_ols = olsModel_quadFit.params["Intercept"]
quadParam_b_ols = olsModel_quadFit.params["year"]
quadParam_a_ols = olsModel_quadFit.params["I(year ** 2)"]

# get param errors
quadParam_c_ols_err = olsModel_quadFit.bse["Intercept"]
quadParam_b_ols_err = olsModel_quadFit.bse["year"]
quadParam_a_ols_err = olsModel_quadFit.bse["I(year ** 2)"]

# GOODNESS
y_quadModel = quad(x, quadParam_a_ols, quadParam_b_ols, quadParam_c_ols)
quad_olsModel_rss = RSS(x, yData, y_quadModel)
quad_olsModel_rmse = RMSE(x, yData, y_quadModel)
quad_olsModel_rSquared = R_SQUARED(x, yData, y_quadModel)

# MODEL BOUNDS
y_quadModel_bound1 = quad(x, 
                            quadParam_a_ols+quadParam_a_ols_err, 
                            quadParam_b_ols-quadParam_b_ols_err, 
                            quadParam_c_ols+quadParam_c_ols_err)
y_quadModel_bound2 = quad(x, 
                            quadParam_a_ols-quadParam_a_ols_err, 
                            quadParam_b_ols+quadParam_b_ols_err, 
                            quadParam_c_ols-quadParam_c_ols_err)

print("\n\t- Quadratic params ols model -")
print(f"a = {round(quadParam_a_ols, 6)} +- {round(quadParam_a_ols_err, 6)}")
print(f"b = {round(quadParam_b_ols, 6)} +- {round(quadParam_b_ols_err, 6)}")
print(f"c = {round(quadParam_c_ols, 6)} +- {round(quadParam_c_ols_err, 6)}")
print("\n\t- Goodness quadratic model -")
print(f"RSS = {round(quad_olsModel_rss,4)}")
print(f"RMSE = {round(quad_olsModel_rmse,4)}")
print(f"RSQUARED = {round(quad_olsModel_rSquared,4)}")


#%% plotting

x = toDate(x)
df_temp.set_index("year_ts", inplace=True)

# show mine and ols models
fig, axL = plt.subplots()

axL.plot(df_temp.index, df_temp["avgtemp"], color="black", linewidth=1, label="Temperature")
axL.plot(x, y_linModel_guess, color="grey", linestyle=":", label="My Linear Fit")

axL.fill_between(x, y_lin_olsModel_bound1, y_lin_olsModel_bound2, color="blue", alpha=.5, zorder=10, label="OLS Linear Model, Range")
axL.fill_between(x, y_quadModel_bound1, y_quadModel_bound2, color="green", alpha=.5, zorder=10, label="OLS Quadratic Model, Range")

axL.set_xlabel("Year")
axL.set_ylabel("Yearly mean temperature (°C)")
axL.set_title("Annual temperature annomaly\ncompared to mean from 1861-1890")

plt.grid(True, zorder=0)
plt.legend(loc="upper left")

axL.axhline(y=0, color="black", linewidth=1, linestyle=":")
axL.axhline(y=1.5, color="red", linestyle=":")

axL.text(toDate(1980), 1.55, "Paris Climate Agreement", color="red", alpha=1, fontsize=10)
axL.text(toDate(1994), 0.05, "1861-1890 mean", color="black", alpha=1, fontsize=10)

axL.set_xlim([df_temp.index.min(), df_temp.index.max()])
axL.set_ylim([-0.25,1.75])

plt.tight_layout()
plt.show()


#%% EXIT

# sys.exit()


#%% Extrapolation / predictions

#
x = np.arange(1900,2101,1)
y_quadModel = quad(x, quadParam_a_ols, quadParam_b_ols, quadParam_c_ols)
y_quadModel_bound1 = quad(x, 
                            quadParam_a_ols+quadParam_a_ols_err, 
                            quadParam_b_ols-quadParam_b_ols_err, 
                            quadParam_c_ols+quadParam_c_ols_err)
y_quadModel_bound2 = quad(x, 
                            quadParam_a_ols-quadParam_a_ols_err, 
                            quadParam_b_ols+quadParam_b_ols_err, 
                            quadParam_c_ols-quadParam_c_ols_err)

x = toDate(x)
fig, axL = plt.subplots()

axL.plot(df_temp.index, df_temp["avgtemp"], color="black", linewidth=1, label="Temperature")
axL.fill_between(x, y_quadModel_bound1, y_quadModel_bound2, color="green", alpha=.5, zorder=10, label="OLS Quadratic Model")
axL.fill_between(toDate(np.arange(2075,2101,1)),
                 [3 for j in range(len(np.arange(2075,2101,1)))],
                 [4 for j in range(len(np.arange(2075,2101,1)))], color="blue", alpha=.1)

plt.grid(True, zorder=0)

axL.axhline(y=0, color="black", linewidth=1, linestyle=":")
axL.axhline(y=1.5, color="red", linestyle=":")
axL.axvline(x=toDate(2025), color="black", linewidth=1, linestyle="--")
#
axL.hlines(y=3, xmin=toDate(2065), xmax=toDate(2100), color="blue", alpha=.5, label="Prediction made by IPCC")
axL.hlines(y=3.1, xmin=toDate(2065), xmax=toDate(2100), color="red", alpha=.5, label="Prediction made by UN")
axL.hlines(y=4, xmin=toDate(2065), xmax=toDate(2100), color="blue", alpha=.5)

axL.set_xlim([x.min(), x.max()])
axL.set_ylim([-0.5,4.2])

plt.legend(loc="upper left")

axR = axL.twinx()
axR.set_ylim([-0.5,4.2])

axR.set_yticks([round(y_quadModel_bound1[-1],2), round(y_quadModel_bound2[-1],2)])
axR.tick_params(axis="y", colors="green")

axL.text(toDate(2065), 3.8, "4", color='blue', alpha=.5, fontsize=10)
axL.text(toDate(2065), 2.8, "3", color='blue', alpha=.5, fontsize=10)
axL.text(toDate(2065), 3.2, "3.1", color='red', alpha=.5, fontsize=10)
#
axL.text(toDate(1902), 1.6, "Paris Climate Agreement", color="red", alpha=1, fontsize=10)
axL.text(toDate(2050), 0.1, "1861-1890 mean", color="black", alpha=1, fontsize=10)
axL.text(toDate(2019), 1.7, "Jan 2025", color="black", alpha=1, fontsize=10, rotation=90)

axL.set_ylabel("Yearly mean temperature (°C)")
axL.set_xlabel("Year")

axL.set_title("Annual temperature annomaly\ncompared to mean from 1861-1890")

plt.tight_layout()
plt.show()

print("\n\t- Estimations for 2100 -")
print(f"quadratic OLS model:\t{round(y_quadModel_bound2[-1],2)} ... {round(y_quadModel_bound1[-1],2)} °C")
print("IPCC (Intergovernmental Panel on Climate Change):\t3 °C ... 4 °C")
print("UN-Bericht („Emissions Gap Report“):\tca. 3.1 °C")
