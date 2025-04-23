#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/5/29 22:27
Desc: 新浪财经-交易日历
https://finance.sina.com.cn/realstock/company/klc_td_sh.txt
此处可以用来更新 calendar.json 文件，注意末尾没有 "," 号
"""
import datetime
import traceback

import pandas as pd
import requests
from py_mini_racer import py_mini_racer

from akshare.stock.cons import hk_js_decode
import extra_utils

def tool_trade_date_hist_sina() -> pd.DataFrame:
    """
    交易日历-历史数据
    https://finance.sina.com.cn/realstock/company/klc_td_sh.txt
    :return: 交易日历
    :rtype: pandas.DataFrame
    """
    url = "https://finance.sina.com.cn/realstock/company/klc_td_sh.txt"
    proxy = None
    for i in range(3):
        try:
            headers = extra_utils.get_headers()
            headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            r = requests.get(url, timeout=15, headers=headers, proxies=proxy, verify=False)
            break
        except:
            traceback.print_exc()
            proxy = extra_utils.get_proxy()
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(hk_js_decode)
    dict_list = js_code.call("d", r.text.split("=")[1].split(";")[0].replace('"', ""))
    temp_df = pd.DataFrame(dict_list)
    temp_df.columns = ["trade_date"]
    temp_df["trade_date"] = pd.to_datetime(temp_df["trade_date"]).dt.date
    temp_list = temp_df["trade_date"].to_list()
    # 该日期是交易日，但是在新浪返回的交易日历缺失该日期，这里补充上
    temp_list.append(datetime.date(1992, 5, 4))
    temp_list.sort()
    temp_df = pd.DataFrame(temp_list, columns=["trade_date"])
    return temp_df


if __name__ == "__main__":
    tool_trade_date_hist_df = tool_trade_date_hist_sina()
    print(tool_trade_date_hist_df)
