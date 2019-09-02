""" Simulator entry point. """

from datetime import date, datetime
import json

import numpy as np
import pandas as pd

from simulator.income import calc_income
from simulator.expense import calc_expense

# Simulation specification.
# Incomes and expenses are the total value of the time period.
# Savings indicates the value at the end of the time period.

def simulate(params: dict,
             tax: dict,
             num_years: int = 100):
    # Years to simulate.
    date_format = params['settings']['date format']
    start_date = datetime.strptime(
        params['settings']['start date'],date_format).date()
    years = pd.Index(np.arange(num_years) + start_date.year)

    # Calc ages of family members.
    ages = calc_age(params['family'], years, date_format=date_format)

    # Incomes.
    incomes = calc_income(params['income'], years, ages)

    # Expenses.
    expenses = calc_expense(params, tax, incomes, years)

    # Start month adjustment.
    mult = 1 - (start_date.month - 1) / 12
    incomes.values[:, 0] *= mult
    expenses.values[:, 0] *= mult

    # Balance calculation.
    balance = incomes.loc['total'] - expenses.loc['total']
    savings = np.cumsum(balance) + params['property']['savings']

    balances = pd.DataFrame({
        'balance': balance,
        'savings': savings}).transpose()

    # Display unit adjustment.
    mult = params['settings']['display unit']['multiplier']
    adjust_func = lambda x: np.round(x * mult)
    incomes = adjust_func(incomes)
    expenses = adjust_func(expenses)
    balances = adjust_func(balances)

    # To multi-index.
    index_func = lambda x, y: y.set_index(
        pd.MultiIndex.from_product([[x], y.index]), inplace=True)
    index_func('age', ages)
    index_func('income', incomes)
    index_func('expense', expenses)
    index_func('balance', balances)

    # Concat.
    df = pd.concat([ages, incomes, expenses, balances])

    return df

def calc_age(params_family: dict,
             years: pd.Index,
             date_format: str):
    today = date.today()

    ages = []
    for person in params_family:
        # Calculate age.
        if person['birthday'] is not None:
            bd = datetime.strptime(person['birthday'], date_format).date()
            person['age'] = today.year - bd.year

        if person['age'] is None:
            raise ValueError('Cannot specify age of %s'.format(person['name']))

        age = np.arange(person['age'], person['age'] + len(years))
        ages.append(pd.Series(age, index=years, name=person['name']))

    return pd.DataFrame(ages)

if __name__ == '__main__':
    with open('testdata/family.json', 'r') as f:
        params = json.load(f)
    with open('testdata/tax.json', 'r') as f:
        tax = json.load(f)
    simulate(params, tax)
