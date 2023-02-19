import pandas as pd
import sys, os

from datetime import datetime

def save_to_xls(dataframe):
    try:
        address_file = sys.path[0]
        address_file = address_file.replace('\\','/')
        os.mkdir(f'{address_file}/xls_store/')

    except FileExistsError:
        print('folder already exists')
        address_file = f'{address_file}/xls_store/'
    os.chdir(address_file)

    now = datetime.now().strftime('%b %d %y %H_%M_%S')
    dataframe.to_excel((f'xls_store_{now}.xlsx'), index=False)

    return f'xls_store_{now}.xlsx'
