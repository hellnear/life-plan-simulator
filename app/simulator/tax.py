""" Calculates tax. """

import numpy as np
import pandas as pd

from simulator.helpers import select_range

def calc_tax(params: dict,
             tax: dict,
             incomes: pd.DataFrame,
             years: pd.Index):
    # 所得税
    income_tax = calc_income_tax(params, tax, incomes, years)
    # 住民税

    return income_tax


def calc_income_tax(params: dict,
                    tax: dict,
                    incomes: pd.DataFrame,
                    years: pd.Index):
    """
    """
    # NOTE: 給与所得のみ対応
    # NOTE: 年による税の変化未考慮

    # Drop total.
    # 給与収入
    incomes = incomes.drop('total')
    inc_shape = incomes.values.shape

    # Get 給与所得控除 table.
    tax_deduc = tax['income tax']['deduction']
    tax_salary = tax_deduc['salary'][0]
    deduc_table = pd.DataFrame.from_dict(tax_salary['table'])

    # Get deduction values of each person and each year.
    idx = select_range(incomes, deduc_table['range'], mode='(]')
    rate = np.take(deduc_table['rate'].values, idx)
    offset = np.take(deduc_table['offset'].values, idx)
    salary_deduction = incomes * rate + offset
    salary_deduction = np.maximum(salary_deduction.values, tax_salary['minimum'])

    # 給与所得
    incomes = incomes - salary_deduction
    incomes = np.floor(np.maximum(incomes, 0))

    # 所得控除
    deducs = []
    # 基礎控除
    deducs.append(np.ones(inc_shape) * tax_deduc['basic'])
    # 配偶者控除・配偶者特別控除 未対応(共働きならだいたい0円)
    # 扶養控除 未対応(対象は16歳～、共働きでないなら考慮すべき)
    # 社会保険料控除　未対応　必ずやる

    # 課税対象所得
    incomes = incomes - np.sum(deducs, axis=0)
    incomes = np.maximum(incomes, 0)
    incomes = np.floor(incomes / 1000) * 1000  # 千円未満切り捨て

    # 所得税
    # Get 所得税率 table.
    tax_table = pd.DataFrame.from_dict(tax['income tax']['tax rate'])
    idx = np.reshape(
        [np.nonzero(list(zip(*tax_table['range'].values))[0] < inc)[0][-1]
         for inc in incomes.values.reshape(-1)], inc_shape)
    rate = np.take(tax_table['rate'].values, idx)
    deduc = np.take(tax_table['rate'].values, idx)
    # 所得税額
    income_tax = incomes * rate - deduc
    income_tax = np.maximum(income_tax, 0)

    return np.sum(income_tax, axis=0)

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

    # Tax.
    taxes = calc_tax(params, tax, incomes, years)
    print(taxes)
