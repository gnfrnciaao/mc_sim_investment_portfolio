import numpy as np
import pandas as pd
from openbb import obb
import matplotlib.pyplot as plt
from random import randint
import seaborn

''' download parameters '''
equity_index = "^GSPC"
bond_index = "TLT"
portfolio = [equity_index, bond_index]
start_date = "1923-01-01"
provider = "yfinance"

''' simulation parameters '''
trading_days_in_year = 252
number_simulations = 1_000
max_number_years = 41 #effective number of simulation years + 1
buckets = 11  #number of groups on the x axis (add +1)
bucket_size = 100_000
simulation_type = "norm"  # "hist", "norm"
results_type = "ratio"  #"ratio" - "value" & "returns" for control/debug purposes only


''' portfolio assumptions '''
equity_share = 1
bond_share = 0
# initial_capital = 600_000
annual_expenditures = 30_000
inflation = 0.03
dividend_yield = 0.02  # as ^GSPC is not TR, ^SP500TR is TR but goes back to only 1988 vs 1923 of ^GSPC
annual_pension = 24_000
pension_start_year = 15

def download_data():
    equity_data = obb.equity.price.historical(
        equity_index,
        start_date=start_date,
        provider=provider
    ).to_df()

    annual_data_equity = equity_data.iloc[::trading_days_in_year]
    annual_data_equity.reset_index(drop=True, inplace=True)
    annual_data_equity["pct_change"] = annual_data_equity["close"].pct_change()

    bond_data = obb.equity.price.historical(
        bond_index,
        start_date=start_date,
        provider=provider
    ).to_df()

    annual_data_bond = bond_data.iloc[::trading_days_in_year]
    annual_data_bond.reset_index(drop=True, inplace=True)
    annual_data_bond["pct_change"] = annual_data_bond["close"].pct_change()

    return annual_data_equity["pct_change"].dropna(), annual_data_bond["pct_change"].dropna()

def run_simulations(returns_equity, returns_bonds):
    if simulation_type == "hist":
        sim_to_call = hist_return_simulation
    else:
        sim_to_call = normal_dist_simulation

    results = np.zeros((max_number_years, 10))
    for j in range(1, buckets):
        for i in range(1, max_number_years + 1):
            results[i - 1, j - 1] = sim_to_call(i, j * bucket_size, returns_equity, returns_bonds)

    if results_type == "value":
        results = pd.DataFrame(results).clip(lower=0)

    return results

def hist_return_simulation(year, capital, equity_rets, bond_rets):
    extracted_returns = np.ones((year, number_simulations))
    sim_matrix = np.ones((year, number_simulations)) * capital

    for i in range(0, number_simulations):
        for j in range(1, year):
            if equity_share:
                random_return_equity = equity_rets[randint(1, len(equity_rets) - 1)]
                extracted_returns[j][i] = random_return_equity
                sim_matrix[j][i] = ((sim_matrix[j - 1][i] - annual_expenditures * (1 + inflation) ** j + (j >= pension_start_year) * annual_pension) *
                                    (1 + random_return_equity + dividend_yield))
            else:
                random_return_bond = bond_rets[randint(1, len(bond_rets) - 1)]
                extracted_returns[j][i] = random_return_bond
                sim_matrix[j][i] = ((sim_matrix[j - 1][i] - annual_expenditures * (1 + inflation) ** j + (j >= pension_start_year) * annual_pension) *
                                (1 + random_return_bond))

    if results_type == "value":
        return calculate_value(sim_matrix)
    elif results_type == "ratio":
        return calculate_ratio(sim_matrix)
    else:
        return calculate_returns(extracted_returns)

def normal_dist_simulation(year, capital, equity_rets, bond_rets):
    extracted_returns = np.ones((year, number_simulations))
    sim_matrix = np.ones((year, number_simulations)) * capital

    mu_equity, sigma_equity = equity_rets.mean(), equity_rets.std()
    mu_bonds, sigma_bonds = bond_rets.mean(), bond_rets.std()

    for i in range(0, number_simulations):
        for j in range(1, year):
            if equity_share:
                random_return_equity = np.random.normal(mu_equity, sigma_equity, 1)
                extracted_returns[j][i] = random_return_equity
                sim_matrix[j][i] = ((sim_matrix[j - 1][i] - annual_expenditures * (1 + inflation) ** j + (j >= pension_start_year) * annual_pension) *
                                    (1 + random_return_equity + dividend_yield))
            else:
                random_return_bond = np.random.normal(mu_bonds, sigma_bonds, 1)
                extracted_returns[j][i] = random_return_bond
                sim_matrix[j][i] = ((sim_matrix[j - 1][i] - annual_expenditures * (1 + inflation) ** j + (j >= pension_start_year) * annual_pension) *
                                (1 + random_return_bond))

    if results_type == "value":
        return calculate_value(sim_matrix)
    elif results_type == "ratio":
        return calculate_ratio(sim_matrix)
    else:
        return calculate_returns(extracted_returns)

def calculate_ratio(matrix):
    positive = 0
    for h in range(number_simulations):
        if matrix[-1][h] >= 0:
            positive += 1
    return (positive / number_simulations) * 100

def calculate_value(matrix):
    value = 0
    for h in range(number_simulations):
        value += matrix[-1][h]
    return value / number_simulations

def calculate_returns(extracted_returns):
    value = 0
    for h in range(number_simulations):
        value += extracted_returns[-1][h]
    return value / number_simulations * 100

def main():
    returns_equity, returns_bonds = download_data()
    results_matrix = run_simulations(returns_equity, returns_bonds)

    if results_type == "value":
        digit_format = ",.0f"
    elif results_type == "ratio":
        digit_format = ".0f"
    else:
        pass

    X_labels = [str(x * 100) + "k" for x in range(1, buckets, 1)]
    Y_labels = [x for x in range(0,max_number_years)]
    plt.figure(figsize=(30, 25))
    seaborn.set(font_scale=1)
    seaborn.heatmap(results_matrix, cmap="PiYG", fmt=digit_format, annot=True, center=0, xticklabels=X_labels, yticklabels=Y_labels, annot_kws={"size": 11})

    plt.show()


if __name__ == "__main__":
    main()
