""" Simulator entry point. """

from datetime import date, datetime
import json

import numpy as np
import pandas as pd

# Simulation specification.
# Incomes and expenses are the total value of the time period.
# Savings indicates the value at the end of the time period.

check_val = lambda x, p: (x in p) & (p[x] is not None)

def simulate(params: dict,
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
    expenses = calc_expense(params, years)

    # Start year adjustment.
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

def calc_income(params_income: dict,
                years: pd.Index,
                ages: pd.DataFrame):
    # Mode usage check.
    # mode_sanity = check_mode('annual') + check_mode('monthly')
    # if mode_sanity > 1 | mode_sanity < 1:
    #     raise ValueError('Income is not set properly.')

    # Calculate annual total income.
    if check_val('annual', params_income):
        annual_incomes = []

        # Linear function generator for later use.
        linear_gen = lambda i, j: lambda x: \
            (j[1] - i[1]) / (j[0]- i[0]) * (x - i[0]) + i[1]

        for person in params_income['annual']:
            age = ages.loc[person['name']].values.astype('float')
            if person['increase type'] == 'piece-wise linear':
                # Increase definition.
                # Add initial and final points.
                increase = \
                    [{'age': age[0], 'amount': person['amount']}] \
                    + person['increase'] \
                    + [{'age': person['retirement age'], 'amount': 0}]
                # Extrace age and amount.
                points = np.stack([[v['age'], v['amount']] for v in increase])\
                    .astype('float')
                # Pieces of age selector.
                piece_x = [np.logical_and(age >= i, age < j)
                           for i, j in zip(points[:-1, 0], points[1:, 0])]
                # Pieces of linear function.
                piece_y = [linear_gen(i, j)
                           for i, j in zip(points[:-2, :], points[1:-1, :])]
                # Keep the last linear function till retirement.
                piece_y += [piece_y[-1]]
                amount = np.piecewise(age, piece_x, piece_y)
            elif person['increase type'] == 'constant':
                amount = np.piecewise(
                    age,
                    [age < person['retirement age'],
                     age >= person['retirement age']],
                    [person['amount'], 0])
            else:
                raise NotImplementedError('')

            annual_income = pd.Series(amount, index=years, name=person['name'])

            if check_val('irregular', params_income):
                irr = [i for i in params_income['irregular']
                       if i['name'] == person['name']]
                for ir in irr:
                    if ir['type'] == 'overwrite':
                        annual_income[ir['year']] = ir['annual']
                    elif ir['type'] == 'add':
                        annual_income[ir['year']] += ir['annual']
                    else:
                        raise ValueError('')

            annual_incomes.append(annual_income)

        # Total.
        annual_incomes.append(
            pd.Series(np.sum(annual_incomes, axis=0), index=years, name='total'))

    return pd.DataFrame(annual_incomes)

def calc_expense(params: dict,
                 years: pd.Index):
    # Monthly living.
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
    living = sum_all(params['expense']['monthly living'].values())

    total_expense = np.ones(len(years)) * living * 12
    total_expense = pd.Series(total_expense, index=years, name='total')

    return pd.DataFrame([total_expense])

if __name__ == '__main__':
    with open('test.json', 'r') as f:
        params = json.load(f)
    simulate(params)
