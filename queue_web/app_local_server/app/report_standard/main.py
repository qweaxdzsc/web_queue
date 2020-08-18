from . import txt_to_python
from . import python_to_html
from . import data_to_excel
import cgitb

global project_address
global project_name
# designate path
project_address = r"G:/test/queue_test2"
project_name = "Test_V1_solve"
path = project_address + '\\result_%s\\' % project_name

# Txt input path
txt_name = path + 'total_result.txt'

# Excel output info
excel_name = project_name                                   # Output excel name
sheet_name = excel_name                                     # The sheet in excel
data_name = excel_name                                      # get a title for your data

# Html output info
html_output_path = path
title = data_name

# run module get excel
data_matrix = txt_to_python.process_data(txt_name)
data_to_excel.get_xls(path, data_matrix, sheet_name, excel_name, data_name)

# run module get html
python_to_html.get_html(data_matrix, title, html_output_path)

# get fan efficiency
cgitb.enable(format='text')
