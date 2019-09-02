""" Calculate expenses """

import numpy as np
import pandas as pd

from simulator.tax import calc_tax

def calc_expense(params: dict,
                 tax: dict,
                 incomes: pd.DataFrame,
                 years: pd.Index):
    annual_expenses = []

    # Living.
    living = calc_living(params, years)
    annual_expenses.append(living)

    # Tax.
    tax = calc_tax(params, tax, incomes, years)
    tax = pd.Series(tax, index=years, name='tax')
    annual_expenses.append(tax)

    # Total.
    annual_expenses.append(
        pd.Series(np.sum(annual_expenses, axis=0), index=years, name='total'))

    return pd.DataFrame(annual_expenses)

def calc_living(params: dict,
                years: pd.Index) -> pd.Series:
    # Sum all recursively.
    def sum_all(item):
        sum = 0
        for i in item:
            if isinstance(i, (int, float)):
                sum += i
            elif isinstance(i, dict):
                sum += sum_all(i.values())
            elif isinstance(i, list):
                sum += sum_all(i)
        return sum

    # Monthly living.
    living = sum_all(params['expense']['monthly'].values())
    living = np.ones(len(years)) * living * 12
    living = pd.Series(living, index=years, name='living')

    return living

if __name__ == '__main__':
    from datetime import datetime
    import json

    from simulator.simulation import calc_age
    from simulator.income import calc_income

    num_years = 100

    # Load testdata.
    with open('testdata/family.json', 'r') as f:
        params = json.load(f)
    with open('testdata/tax.json', 'r') as f:
        tax = json.load(f)

    # Years to simulate.
    date_format = params['settings']['date format']
    start_date = datetime.strptime(
        params['settings']['start date'],date_format).date()
    years = pd.Index(np.arange(num_years) + start_date.year)

    # Calc ages of family members.
    ages = calc_age(params['family'], years, date_format=date_format)

    # Incomes.
    incomes = calc_income(params['income'], years, ages)
    print(incomes)

    # Expense.
    expenses = calc_expense(params, tax, incomes, years)
    print(expenses)
