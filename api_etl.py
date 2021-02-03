#import random
#from get_all_tickers import get_tickers as gt
#random.seed(10)
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
from io import StringIO # python3; python2: BytesIO
import boto3
from datetime import datetime
import s3fs


#def get_stocks(num_symbols):
    # Get a list of favorite financial stocks #

    # Get list of all symbols
    # all_symbols = gt.get_tickers()

    # select number of favorite symbols
    #select_stocks = random.sample(all_symbols, num_symbols)
    #print(select_stocks)
    #return select_stocks


# function to extract stocks information from alpha advantage API

def main():


    appended_data = []
    stock_list=['IBM', 'MSFT', 'TMUS', 'FDIV', 'KSMTU', 'AWR', 'NYV', 'DUO', 'UUUU', 'FSBW', 'NAK', 'TPRE', 'OXBRW', 'DXR', 'JE', 'BZH', 'HCSG', 'FRAF', 'ATSG', 'CMA', 'WTTR', 'OLB', 'AVT', 'BUI', 'CNMD', 'HSC', 'MAR', 'ASTC', 'BWB', 'CPSS', 'TGI', 'RVP', 'PSET', 'STE', 'EUCRU', 'BMA', 'METC', 'HIO', 'PTON', 'AYTU', 'GRC', 'AAPL', 'PPH', 'RMD', 'DHCNI', 'MOFG', 'BEAT', 'BST', 'LE', 'AAP', 'PACK', 'GPK', 'IRL', 'EHI', 'ISNS', 'BWFG', 'VBIV', 'REV', 'EGHT', 'PIRS', 'BSJP', 'ELYS', 'XRAY', 'INBKL', 'CVX', 'OM', 'LFTRU', 'AIH', 'AIQ', 'SJM', 'PING', 'CCNEP', 'RTP', 'BSM', 'BSAC', 'GFNSL', 'WEI', 'IOR', 'MDGS', 'PKOH', 'CNF', 'IPWR', 'CAAP', 'ING', 'BPYUP', 'UAE', 'BMRA', 'MANH', 'SFUN', 'VTNR', 'VEON', 'DX', 'DKNG', 'LH', 'LEU', 'NFG', 'AQB', 'PLAY', 'CVLY', 'ESSCR', 'SFE', 'PPBT', 'TMX', 'HLT', 'MPWR', 'HLIO', 'MA', 'PFD', 'SNX', 'ESSA', 'WEA', 'KEP', 'PCB', 'OPRX', 'MTA', 'MFD', 'CEY', 'MMD', 'RMG', 'CPA', 'SCS', 'ADOC', 'CJJD', 'LMRKP', 'HEQ', 'CSIQ', 'GCMG', 'PINC', 'RBA', 'TAIT', 'HSTO', 'TEO', 'HHR', 'MRVI', 'GLADL', 'CEPU', 'FOXA', 'PRMW']

    print('getting data for stocks')
    for stk in stock_list:

        print('getting data for ',stk)
        ts = TimeSeries(key='R1PVPC1AFCK8MHTZ', output_format='pandas')
        data, meta_data = ts.get_daily(symbol=stk, outputsize='full')
        data.reset_index(inplace=True)
        data.insert(loc=0, column='symbol', value=stk)

        # store DataFrame in list
        appended_data.append(data)

        time.sleep(20)

    return appended_data



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    

    # Get full dataFrame
    print('starting execution')
    df = pd.concat(main())

    etl_runtime = datetime.today().strftime('%Y%m%d%H%M%S')

    bucket = 's3://etl-landing-zone'  # already created on S3
    df.to_csv(bucket + '/source-files/' + etl_runtime + '.csv')


