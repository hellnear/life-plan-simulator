""" 社会保険料の計算 """

import numpy as np
import pandas as pd

from simulator.helpers import select_range

def calc_social_insurance(params: dict,
                          tax: dict,
                          incomes: pd.DataFrame,
                          years: pd.Index):
    # Drop total.
    incomes = incomes.drop('total')
    inc_shape = incomes.values.shape

    # 標準報酬月額(SMR)
    # 現状は年収額で設定しているので、正確には計算できない
    # ボーナスが月収の何か月分かをパラメータに入れているので、それを利用する
    # TODO: typeをチェックしていない
    bonus_month = {}
    [bonus_month.update({p['name']: p['bonus']['amount']})
     for p in params['income']['annual']]
    bonus_month = np.ones(inc_shape) * [bonus_month[p] for p in incomes.index]
    average_monthly_income = incomes.values / (12 + bonus_month)

    # Load table.
    smr_table_health = pd.DataFrame.from_dict(tax['social insurance']['health'])
    smr_table_pension = pd.DataFrame.from_dict(tax['social insurance']['pension'])

    idx_health = select_range(average_monthly_income, smr_table_health['range'])


    return income_tax

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
    social_insurance = calc_social_insurance(params, tax, incomes, years)
    print(social_insurance)
