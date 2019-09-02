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
        'income tax': {
            'deduction': {
                'salary': [{
                    'year range': (None, 2019),
                    'minimum': 650_000,
                    'table': [
                        # Include range[1], not include range[0]
                        # range[0] < income <= range[1]
                        # deduction = income * 'rate' + 'offset'
                        {'range': (-1, 1_800_000), 'rate': 0.4, 'offset': 0},
                        {'range': (1_800_000, 3_600_000), 'rate': 0.3, 'offset': 180_000},
                        {'range': (3_600_000, 6_600_000), 'rate': 0.2, 'offset': 540_000},
                        {'range': (6_600_000, 10_000_000), 'rate': 0.1, 'offset': 1_200_000},
                        {'range': (10_000_000, None), 'rate': 0.0, 'offset': 2_200_000}
                    ]
                }],
                'basic': 380_000,
                'public pension': [
                    # Do not include 'upper age'
                    # ('upper age' is compared with 'less than')
                    {'upper age': 65, 'amount': 700_000},
                    {'upper age': None, 'amount': 1_200_000}
                ]
            },
            'tax rate': [
                {'range': (-1, 1_950_000), 'rate': 0.05, 'deduction': 0},
                {'range': (1_950_000, 3_300_000), 'rate': 0.10, 'deduction': 97_500},
                {'range': (3_300_000, 6_950_000), 'rate': 0.20, 'deduction': 427_500},
                {'range': (6_950_000, 9_000_000), 'rate': 0.23, 'deduction': 636_000},
                {'range': (9_000_000, 18_000_000), 'rate': 0.33, 'deduction': 1_536_000},
                {'range': (18_000_000, 40_000_000), 'rate': 0.40, 'deduction': 2_796_000},
                {'range': (40_000_000, None), 'rate': 0.45, 'deduction': 4_796_000}
            ]
        },

        'social insurance': {
            'standard monthly remuneration': {
                'health': [
                    # range[0] <= average monthly income < range[1]
                    {'grade': 1, 'range': (0, 63000), 'amount': 58000},
                    {'grade': 2, 'range': (63000, 73000), 'amount': 68000},
                    {'grade': 3, 'range': (73000, 83000), 'amount': 78000},
                    {'grade': 4, 'range': (83000, 93000), 'amount': 88000},
                    {'grade': 5, 'range': (93000, 101000), 'amount': 98000},
                    {'grade': 6, 'range': (101000, 107000), 'amount': 104000},
                    {'grade': 7, 'range': (107000, 114000), 'amount': 110000},
                    {'grade': 8, 'range': (114000, 122000), 'amount': 118000},
                    {'grade': 9, 'range': (122000, 130000), 'amount': 126000},
                    {'grade': 10, 'range': (130000, 138000), 'amount': 134000},
                    {'grade': 11, 'range': (138000, 146000), 'amount': 142000},
                    {'grade': 12, 'range': (146000, 155000), 'amount': 150000},
                    {'grade': 13, 'range': (155000, 165000), 'amount': 160000},
                    {'grade': 14, 'range': (165000, 175000), 'amount': 170000},
                    {'grade': 15, 'range': (175000, 185000), 'amount': 180000},
                    {'grade': 16, 'range': (185000, 195000), 'amount': 190000},
                    {'grade': 17, 'range': (195000, 210000), 'amount': 200000},
                    {'grade': 18, 'range': (210000, 230000), 'amount': 220000},
                    {'grade': 19, 'range': (230000, 250000), 'amount': 240000},
                    {'grade': 20, 'range': (250000, 270000), 'amount': 260000},
                    {'grade': 21, 'range': (270000, 290000), 'amount': 280000},
                    {'grade': 22, 'range': (290000, 310000), 'amount': 300000},
                    {'grade': 23, 'range': (310000, 330000), 'amount': 320000},
                    {'grade': 24, 'range': (330000, 350000), 'amount': 340000},
                    {'grade': 25, 'range': (350000, 370000), 'amount': 360000},
                    {'grade': 26, 'range': (370000, 395000), 'amount': 380000},
                    {'grade': 27, 'range': (395000, 425000), 'amount': 410000},
                    {'grade': 28, 'range': (425000, 455000), 'amount': 440000},
                    {'grade': 29, 'range': (455000, 485000), 'amount': 470000},
                    {'grade': 30, 'range': (485000, 515000), 'amount': 500000},
                    {'grade': 31, 'range': (515000, 545000), 'amount': 530000},
                    {'grade': 32, 'range': (545000, 575000), 'amount': 560000},
                    {'grade': 33, 'range': (575000, 605000), 'amount': 590000},
                    {'grade': 34, 'range': (605000, 635000), 'amount': 620000},
                    {'grade': 35, 'range': (635000, 665000), 'amount': 650000},
                    {'grade': 36, 'range': (665000, 695000), 'amount': 680000},
                    {'grade': 37, 'range': (695000, 730000), 'amount': 710000},
                    {'grade': 38, 'range': (730000, 770000), 'amount': 750000},
                    {'grade': 39, 'range': (770000, 810000), 'amount': 790000},
                    {'grade': 40, 'range': (810000, 855000), 'amount': 830000},
                    {'grade': 41, 'range': (855000, 905000), 'amount': 880000},
                    {'grade': 42, 'range': (905000, 955000), 'amount': 930000},
                    {'grade': 43, 'range': (955000, 1005000), 'amount': 980000},
                    {'grade': 44, 'range': (1005000, 1055000), 'amount': 1030000},
                    {'grade': 45, 'range': (1055000, 1115000), 'amount': 1090000},
                    {'grade': 46, 'range': (1115000, 1175000), 'amount': 1150000},
                    {'grade': 47, 'range': (1175000, 1235000), 'amount': 1210000},
                    {'grade': 48, 'range': (1235000, 1295000), 'amount': 1270000},
                    {'grade': 49, 'range': (1295000, 1355000), 'amount': 1330000},
                    {'grade': 50, 'range': (1355000, None), 'amount': 1390000}
                ],
                'pension': [
                    # range[0] <= average monthly income < range[1]
                    {'grade': 1, 'range': (83000, 93000), 'amount': 88000},
                    {'grade': 2, 'range': (93000, 101000), 'amount': 98000},
                    {'grade': 3, 'range': (101000, 107000), 'amount': 104000},
                    {'grade': 4, 'range': (107000, 114000), 'amount': 110000},
                    {'grade': 5, 'range': (114000, 122000), 'amount': 118000},
                    {'grade': 6, 'range': (122000, 130000), 'amount': 126000},
                    {'grade': 7, 'range': (130000, 138000), 'amount': 134000},
                    {'grade': 8, 'range': (138000, 146000), 'amount': 142000},
                    {'grade': 9, 'range': (146000, 155000), 'amount': 150000},
                    {'grade': 10, 'range': (155000, 165000), 'amount': 160000},
                    {'grade': 11, 'range': (165000, 175000), 'amount': 170000},
                    {'grade': 12, 'range': (175000, 185000), 'amount': 180000},
                    {'grade': 13, 'range': (185000, 195000), 'amount': 190000},
                    {'grade': 14, 'range': (195000, 210000), 'amount': 200000},
                    {'grade': 15, 'range': (210000, 230000), 'amount': 220000},
                    {'grade': 16, 'range': (230000, 250000), 'amount': 240000},
                    {'grade': 17, 'range': (250000, 270000), 'amount': 260000},
                    {'grade': 18, 'range': (270000, 290000), 'amount': 280000},
                    {'grade': 19, 'range': (290000, 310000), 'amount': 300000},
                    {'grade': 20, 'range': (310000, 330000), 'amount': 320000},
                    {'grade': 21, 'range': (330000, 350000), 'amount': 340000},
                    {'grade': 22, 'range': (350000, 370000), 'amount': 360000},
                    {'grade': 23, 'range': (370000, 395000), 'amount': 380000},
                    {'grade': 24, 'range': (395000, 425000), 'amount': 410000},
                    {'grade': 25, 'range': (425000, 455000), 'amount': 440000},
                    {'grade': 26, 'range': (455000, 485000), 'amount': 470000},
                    {'grade': 27, 'range': (485000, 515000), 'amount': 500000},
                    {'grade': 28, 'range': (515000, 545000), 'amount': 530000},
                    {'grade': 29, 'range': (545000, 575000), 'amount': 560000},
                    {'grade': 30, 'range': (575000, 605000), 'amount': 590000},
                    {'grade': 31, 'range': (605000, None), 'amount': 620000}
                ]
            }
        }
    }

    with open('testdata/tax.json', 'w') as f:
        json.dump(tax, f, indent=4)
