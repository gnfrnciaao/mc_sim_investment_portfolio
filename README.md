# Portfolio Simulation

Simulates the performance of a portfolio over a specified time period. 
It uses historical or normal distribution returns to project the portfolio's success rate to service annual expenses. 

## Dependencies
- `python3.9` please use python 3.9 to avoid dependency issues with distutils in openbb
- `numpy` (Numerical Python) for numerical computations.
- `pandas` (Python Data Analysis Library) for data manipulation.
- `openbb` (Open Bloomberg) for accessing financial data.
- `matplotlib` for creating plots.
- `seaborn` for enhancing visualization.

## Parameters

- **Download Parameters**:
- `equity_index`: Symbol for the equity index.
- `bond_index`: Symbol for the bond index. 
- `equity_share, bond_share`: CURRENTLY only 100% Equity or 100% Bond portfolio (TLT Bond Fund)
- `portfolio`: List of symbols for assets in the portfolio.
- `start_date`: Start date for fetching historical data.
- `provider`: Data provider for financial data.

- **Simulation Parameters**:
- `trading_days_in_year`: Number of trading days in a year.
- `number_simulations`: Number of simulations to run.
- `max_number_years`: Maximum number of simulation years.
- `buckets`: Number of groups on the x-axis.
- `bucket_size`: Size of each bucket.
- `simulation_type`: Type of simulation ("hist" for historical, "norm" for normal distribution).
- `results_success_rate`: Boolean flag to indicate whether to show portfolio success rate or portfolio value.

- **Portfolio Assumptions**:
- `annual_expenditures`: Annual expenditures from the portfolio.
- `inflation`: Annual inflation rate.
- `dividend_yield`: Dividend yield.
- `annual_pension`: Annual pension - assumed to be paid in bulk at beginning of the year.
- `pension_start_year`: First year of pension entitlement.


## How It Works

1. **Download Data**: Fetches historical price data for the specified equity and bond indices.

2. **Run Simulations**: Simulates portfolio performance based on historical or normal distribution returns. 
Calculates either the success rate or the portfolio value for each simulation.
Expenses are deducted from the portfolio at the beginning of each year
(assumption: part of the portfolio is converted into cash). 








