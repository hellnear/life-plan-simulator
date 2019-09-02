""" Calculate income. """

import numpy as np
import pandas as pd

from simulator.helpers import check_val

def calc_income(params_income: dict,
                years: pd.Index,
                ages: pd.DataFrame) -> pd.DataFrame:
    """[summary]

    Args:
        params_income (dict): [description]
        years (pd.Index): [description]
        ages (pd.DataFrame): [description]

    Raises:
        ValueError: [description]
        NotImplementedError: [description]
        ValueError: [description]

    Returns:
        pd.DataFrame: [description]

                      2019        2020  ...  2118
        Taro     7000000.0   7100000.0  ...   0.0
        Hanako   4000000.0   4000000.0  ...   0.0
        total   11000000.0  11100000.0  ...   0.0
    """

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

if __name__ == '__main__':
    from datetime import datetime
    import json

    from simulator.simulation import calc_age

    num_years = 100

    # Load testdata.
    with open('testdata/family.json', 'r') as f:
        params = json.load(f)

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
