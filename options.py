#coding: utf-8
import argparse
import datetime
import os

def get_date_str(offset):
    if(offset is None):
        offset = 0
    date_str = (datetime.datetime.today() + datetime.timedelta(days=offset)).strftime("%Y-%m-%d")
    return date_str

_default = dict(
    reload_data = 'N',
    predict_offset = 30,   # predict stock offset, default a month later
    batch_size = 100,      # the training batch size
    epochs = 1,             # the train epochs
    retraining = 'N',       # retrain the stock AI model
    predict_stocks = None,   # the predict stock, None is recommendation 10 stocks
    recommend_stocks_num = 10,  # the recommendation stocks number 
    start_date='2001-01-01',
    store_path='./datacache',
    download_threads=10
    )

parser =  argparse.ArgumentParser(description = 'A stock Deep Learning framework to predict future stock operation')

parser.add_argument('--reload', type=str, default=_default['reload_data'], dest='reload_data', help='Relod the stock data from internet or not(Y/N), default %s' % _default['reload_data'])

parser.add_argument('--predict_offset', type=int, default=_default['predict_offset'], dest='predict_offset', help='Predict offset days stock prices for operation selection(1-90),default %s' % _default['predict_offset'])

parser.add_argument('--batch_size', type = int, default=_default['batch_size'], dest='batch_size', help='Stock Training batch size(50-500, default %s' % _default['batch_size'])

parser.add_argument('--epochs', type = int, default=_default['epochs'], dest='epochs', help='Stock deep learning traing epochs(1-100), default %s' % _default['epochs'])

parser.add_argument('--predict_stocks', type=str, default=_default['predict_stocks'], dest='predict_stocks', help='The list id of stocks to predict, None for stocks recommendation, default %s' % _default['predict_stocks'])

parser.add_argument('--recommend_stocks_num', type=int, default=_default['recommend_stocks_num'], dest='recommend_stocks_num', help='The number of stocks performance better in Deep Learning model(1-20), default %s' % _default['recommend_stocks_num'])

parser.add_argument('--start_date', type=str, default=_default['start_date'], dest='start_date', help='The stock start date default %s' % _default['start_date'])

parser.add_argument('--store_path', type=str, default=_default['store_path'], dest='store_path', help='The data and model store path,default %s' % _default['store_path'])

parser.add_argument('--downlaod_threads', type=int, default=_default['download_threads'], dest='download_threads',help='The download threads number,default %d' % _default['download_threads'])

def checkFoldPermission(path):
    if(path == 'USER_HOME/tmp/stockAI_cache'):
        path = os.path.expanduser('~') + '/tmp/stockAI_cache'
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            txt = open(path + os.sep + "test.txt","w")
            txt.write("test")
            txt.close()
            os.remove(path + os.sep + "test.txt")
            
    except Exception as e:
        print(e)
        return False
    return True

def main():
    args = parser.parser_args()
    print(args)

if __name__ == '__main__':
    main()