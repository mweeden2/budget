# created by Matt Weeden
# 10/19/16
#
# This file contains the settings for update_budget.py

CURRENT_YEAR = 2017

PATH_TO_FILE = '/path/to/budget.xlsx'

# The keys are category names from the log (Bank website or Mint.com), while
#   values are categories found in the budget sheet itself
CATEGORIES = {
    # Income
    'Paycheck' : 'Salary',


    # Variable Expenses
    'Groceries' : 'Groceries',
    'Alcohol' : 'Alcohol',

    'Miscellaneous' : 'Misc.',


    # Variable Utilities

    # Variable Savings

    # Fixed Expenses
    'Housing' : 'Rent',

    # Fixed Savings
    'emergency' : 'Emergency Fund'
}

SUB_CHARITY = {
    'charity description 1': 'main_key'
}

SUB_SAVINGS = {
    'transfer description': 'emergency'
}
