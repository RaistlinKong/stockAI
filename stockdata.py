#coding:utf-8
import tushare as ts
import pandas as pd
import os
import timeit
import options
import datetime
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
import crash_on_ipy

## the file to get the stock data, now only cover the china main land stocks

# the stock features used in deep learning, note: your should not use lienar feature data same time
_stock_features=[
    'open',         # the stock open price
    'high',         # the highest stock price
    'close',        # the stock close price
    'low',          # the lowest price
    'volume',       # the volume traded today
    'turnover',     # the turnover percentage
]

class StockData(object):
    def __init__(self, args):
        self.reload_data = args.reload_data
        self.store_path = args.store_path
        self.start_date = args.start_date
        self.download_threads = args.download_threads

    def get_stock_basics(self,datestr,failedcount,count,totaltry):
        # continued failed regard as download all the data
        totaltry.append(1)
        try:
            b = ts.get_stock_basics(datestr)
            b.to_csv(self.store_path + os.sep + 'stockbasics' + datestr + '.csv')
        except Exception as e:
            failedcount.append(1)
            print('Failed %d to downlod stock basics of %s:%s' %(len(failedcount),datestr, e))
            return
        #clear the failed count if there is succeed one
        count.append(1)
        print('stock basics of %s downloaed\n' % datestr)

    def get_all_basics(self):
        print('start stock basics downloading...\n')
        daydelta = datetime.timedelta(1, 0, 0)
        date = datetime.datetime.today() - daydelta
        dates = []
        start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
        # get the date array from yesterday to the start date
        while date >= start_date:
            dates.append(date.strftime('%Y-%m-%d'))
            date -= daydelta
        print('Start to download %d days basics...\n' % len(dates))
        print(dates[1:20])
        failcount = []
        count = []
        totaltry = []
        start = timeit.default_timer()
        mapfunc = partial(self.get_stock_basics, failedcount=failcount, count=count, totaltry=totaltry)
        pool = ThreadPool(self.download_threads)
        pool.map(mapfunc, dates) ## multi-threads executing
        pool.close() 
        pool.join()

        print("get_all_basics "+ str(len(totaltry)) + " tries " + str(len(count)) + " days basics downloaded... time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")
        return len(count)

    def get_stock_dailydata(self,stockcode,count):
        try:
            todaystr = datetime.datetime.today().strftime('%Y-%m-%d');
            x = ts.get_hist_data(stockcode, start=self.start_date, end=todaystr)
            x.to_csv(self.store_path + os.sep + 'dailydata' + stockcode + '.csv')
        except Exception as e:
            print('Failed to download dailydata of stocks %s:%s\n'%(stockcode, e))
            return
        count.append(1)
        print('stock %s dailytdata downloaded\n' % stockcode)

    def get_all_dailydata(self):
        
        # first get the stocks list
        print('get all stock list...\n')
        sbs = ts.get_stock_basics()
        print('start to download daily data of %s stocks\n' % sbs.index.size)
        start = timeit.default_timer()

        count = []
        mapfunc = partial(self.get_stock_dailydata, count=count)
        pool = ThreadPool(self.download_threads)
        pool.map(mapfunc, sbs.index) ## multi-threads executing
        pool.close() 
        pool.join()

        print("get_all_dailydata " + str(len(count)) + " stocks end... time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")
        return len(count)
    
    def check_cached_data(self):
        # check the daily data file exist or not
        filepath = self.store_path + os.sep + "cacheddata";
        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                # the data do not need to be downloaded if relaod data is not set to Y
                txt = open(filepath,"r")
                print(txt.read())
                if self.reload_data != 'Y':
                    print('cacheddata exist and reload data %s, save download\n' % self.reload_data)
                    return True
            else:
                os.remove(filepath)
        return False

    def download(self):
        # create the directory
        if not os.path.exists(self.store_path):
            os.makedirs(self.store_path)
        if self.check_cached_data():
            print('StockData')
        else:
            print('StockData start downloading...\n')
            basics_num = self.get_all_basics()
            dailydata_num = self.get_all_dailydata()
            txt = open(self.store_path + os.sep + "cacheddata", "w")
            txt.write('Stock data cached at {0} with {1} dailydata and {2} days stock basics'.format(datetime.datetime.today().strftime('%Y-%m-%d'), dailydata_num, basics_num))
            txt.close()


# the main funciton used to debug StockData alone
def main():
    print('starting...\n')
    args = options.parser.parse_args()
    print('get options\n')
    if not options.checkFoldPermission(args.store_path):
        print('\nPermission denied: %s' % args.store_path)
        print('Please make sure you have the permission to save the data!\n')
    sd = StockData(args)
    sd.download()



if __name__ == '__main__':
    main()



