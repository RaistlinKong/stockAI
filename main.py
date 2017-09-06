#coding:utf-8
from stockdata import StockData
import os


def main():
    print('starting...\n')
    args = option.parser.args()
    print('get options\n')
    if not options.checkFoldPermission(args.store_path):
        print('\nPermission denied: %s' % args.store_path)
        print('Please make sure you have the permission to save the data!\n')



if __name__ == '__main__':
    main()