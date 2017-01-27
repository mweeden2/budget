# created by Matt Weeden
# 10/17/16

# This script reads txt and xls files to update an xls file with category
#   totals for a monthly budget

import sys
import settings
from utils import get_month, get_year, month_string, in_month, gather_log_rows, get_cat_totals, set_actuals
from settings import PATH_TO_FILE
from openpyxl import load_workbook


m = get_month(sys.argv)
m_string = month_string(m)
y = get_year(sys.argv)

m_y = (m, y)
m_y_string = m_string + '_' + str(y)

wb = load_workbook(PATH_TO_FILE)

ls = wb['Log']
ws = wb[m_y_string]

# get the relevant log entries
log_rows = gather_log_rows(m_y, ls)

# for each log entry, assign it to a budget category
cat_totals, missed_rows = get_cat_totals(log_rows)

if len(missed_rows) > 0:
    print 'UNRECOGNIZED ROWS:'
    for r in missed_rows:
        count = len(r)
        for x in r:
            sys.stdout.write(str(x.value))
            if count > 1:
                sys.stdout.write(' | ')
            count -= 1
        print
    print

set_actuals(cat_totals, ws)

wb.save(PATH_TO_FILE)
