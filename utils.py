# create by Matt Weeden
# 10/17/16

# This script provides helper functions for update_budget.py

import sys
import datetime
from settings import CURRENT_YEAR, CATEGORIES, SUB_CHARITY, SUB_SAVINGS
import decimal


CENTS = decimal.Decimal('.01')
usage = "That's not right.\nUsage: python update_budget.py month [year (default 2017)]"

#
# date functions
#####################################################################################
months = {"january": 1,"february": 2,"march": 3,"april": 4,"may": 5,"june": 6,"july": 7,"august": 8,"september": 9,"october": 10,"november": 11,"december": 12}

# return the month number based on cmd line argument (either month number or month string)
def get_month(args):
    if len(args) not in [2, 3]:
        print usage
        sys.exit()
    if args[1].lower() in months:
        return months[args[1].lower()]
    elif args[1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']:
        return int(args[1])
    print usage
    sys.exit()

months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

# return the year number based on cmd line argument
def get_year(args):
    year = CURRENT_YEAR
    if len(args) == 3:
        try:
            year = int(args[2])
        except ValueError:
            print usage
            sys.exit()
    return year

# return the month string based on the month number
def month_string(m):
    return months[m-1]

# return the dates at the edges of each month
def init_m_edges(y):
    month_edges = {
        1: datetime.datetime(y, 1, 1),
        2: datetime.datetime(y, 2, 1),
        3: datetime.datetime(y, 3, 1),
        4: datetime.datetime(y, 4, 1),
        5: datetime.datetime(y, 5, 1),
        6: datetime.datetime(y, 6, 1),
        7: datetime.datetime(y, 7, 1),
        8: datetime.datetime(y, 8, 1),
        9: datetime.datetime(y, 9, 1),
        10: datetime.datetime(y, 10, 1),
        11: datetime.datetime(y, 11, 1),
        12: datetime.datetime(y, 12, 1),
        13: datetime.datetime(y + 1, 1, 1)}
    return month_edges

# boolean; check if this date is in the month indicated by the month number
def in_month(m, d, m_edges):
    if m_edges[m] <= d and d < m_edges[m+1]:
        return True
    return False

#
# log sheet functions
#####################################################################################

# return the log rows that belong to the indicated month
def gather_log_rows(m_y, log_sheet):
    m = m_y[0]
    y = m_y[1]
    m_edges = init_m_edges(y)
    mon_rows = []
    count = 0
    for r in tuple(log_sheet.rows):
        # skip the header row
        if count > 0:
            if r[0].value is None:
                break
            if in_month(m, r[0].value, m_edges):
                mon_rows.append(r)
        else:
            count += 1
    return mon_rows

# return the category dictionary containing values
def get_cat_totals(log_rows):
    missed_rows = []
    cats = dict.fromkeys(CATEGORIES.values(), 0)
    for r in log_rows:
        # if this entry is not in a sub category, it is returned itself
        sub_cat = get_sub_cat(r)
        if sub_cat in CATEGORIES:
            if r[5].value == 'credit':
                cats[CATEGORIES[sub_cat]] += (decimal.Decimal(r[4].value).quantize(CENTS, decimal.ROUND_HALF_UP))
            elif r[5].value == 'debit':
                cats[CATEGORIES[sub_cat]] += (decimal.Decimal(r[4].value).quantize(CENTS, decimal.ROUND_HALF_UP))
        else:
            missed_rows.append(r)

    return cats, missed_rows

# return the sub_category keyword for this entry
def get_sub_cat(c):
    cat = c[3].value
    if cat == 'Charity':
        if c[2].value in SUB_CHARITY:
            return SUB_CHARITY[c[2].value]
    if cat == 'Financial Services : Savings':
        if c[2].value in SUB_SAVINGS:
            return SUB_SAVINGS[c[2].value]
    return cat

#
# month sheet functions
#####################################################################################
def set_actuals(c_totals, ws):
    rows = gather_ws_rows(ws)

    index = 0
    for r in rows:
        index += 1
        if r[1].value in c_totals:
            if c_totals[r[1].value] == 0:
                print '-->', c_totals[r[1].value], '\t\t',  r[1].value
            else:
                print '-->', c_totals[r[1].value], '\t',  r[1].value
            ws.cell(row=index, column=5).value = c_totals[r[1].value]

def gather_ws_rows(ws):
    rows = []
    for r in tuple(ws.rows):
        rows.append(r)
        if r[0].value == "Balance":
            break
    return rows
