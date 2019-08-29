""" Write a parameter file for personal simulation. """

import json

if __name__ == '__main__':

    params = {
        # Simulation settings.
        'settings': {
            'currency': 'JPY',
            'display unit': {'multiplier': 0.0001, 'unit':  'MAN YEN'},
            'date format': '%Y/%m/%d',
            'start date': '2019/08/01' # 1st day only.
        },

        # Family structure.
        'family': [
            # Mandatory: 'name' and ('birthday' or 'age')
            # 'name' is used as an id in other parts.
            # 'age' will be overwritten if 'birthday' is set.
            # Set 'age' of Dec. 31 in the year of 'start date'.
            {'name': 'Taro', 'birthday': '1985/5/05', 'age': None, 'sex': 'male'},
            {'name': 'Hanako', 'birthday': '1987/03/21', 'age': None, 'sex': 'female'},
            {'name': 'Jiro', 'birthday': '2013/01/11', 'age': None, 'sex': 'male'},
            {'name': 'Hanayo', 'birthday': '2017/12/30', 'age': None, 'sex': 'female'}
        ],

        'income': {
            # Annual basis.
            'annual': [
                {
                    'name': 'Taro',
                    'amount': 7_000_000,
                    # 'increase type' has 3 kinds of value.
                    #   - 'rate': specifies increase rates in 'increase'
                    #   - 'piece-wise linear': specifies target amount in 'increase'
                    #   - 'constant': sets None in 'increase'
                    'increase type': 'piece-wise linear',
                    'increase': [
                        {'age': 50, 'amount': 8_000_000},
                        {'age': 60, 'amount': 5_500_000}
                    ],
                    'retirement age': 60,
                    'bonus': {'type': 'multiplier to monthly income', 'amount': 4}
                },
                {
                    'name': 'Hanako',
                    'amount': 4_000_000,
                    'increase type': 'constant',
                    'increase': None,
                    'retirement age': 55,
                    'bonus': {'type': 'multiplier to monthly income', 'amount': 4}
                }
            ],
            # Monthly basis.
            'monthly': None,
            # Irregular.
            'irregular': [
                {'name': 'Hanako', 'year': 2019, 'annual': 2_000_000, 'type': 'overwrite'}
            ]
        },


        'expense': {
            'total': None,

            'monthly': {
                'living': {
                    'food': 50_000,
                    'utility': {
                        'gas': 4_000,
                        'water': 3_000,
                        'electricity': 10_000
                    },
                    'phone': None,
                    'internet': 3000,
                    'transport': None,
                    'miscellaneous': 40_000,
                    'hobby': None,
                    'leisure': None,
                    'clothing': None,
                    'socializing': None,
                    'allowance': [
                        {'name': 'Taro', 'amount': 30_000},
                        {'name': 'Hanako', 'amount': 20_000}
                    ]
                },
                'housing': {
                    'rent': 120_000,
                    'loan': 0,
                    'management': 0
                },
                'education': 0,
                'insurance': None
            },

            'annual tax': {
                'property tax': 0,
            }
        },

        'property': {
            # Current savings on 'start date'
            'savings': 5_200_000
        }
    }

    with open('testdata/family.json', 'w') as f:
        json.dump(params, f, indent=4)

    # Rough calculation.
    tax = {
        'year': 2019,
        'income tax': {
            'deduction': {
                'basic': 380_000,
                'salary': [
                    # Include 'upper income', not include 'bottom income'
                    # 'bottom income' < income <= 'upper income'
                    # deduction = income * 'rate' + 'offset'
                    # Ignoring the table
                    {'bottom income': None,'upper income': 1_625_000, 'rate': 0.0, 'offset': 650_000},
                    {'bottom income': 1_625_000,'upper income': 1_800_000, 'rate': 0.4, 'offset': 0},
                    {'bottom income': 1_800_000,'upper income': 3_600_000, 'rate': 0.3, 'offset': 180_000},
                    {'bottom income': 3_600_000,'upper income': 6_600_000, 'rate': 0.2, 'offset': 540_000},
                    {'bottom income': 6_600_000,'upper income': 10_000_000, 'rate': 0.1, 'offset': 1_200_000},
                    {'bottom income': 10_000_000,'upper income': None, 'rate': 0.0, 'offset': 2_200_000}
                ],
                'public pension': [
                    # Do not include 'upper age'
                    # ('upper age' is compared with 'less than')
                    {'upper age': 65, 'amount': 700_000},
                    {'upper age': None, 'amount': 1_200_000}
                ]
            }
        }
    }

    with open('testdata/tax.json', 'w') as f:
        json.dump(tax, f, indent=4)
