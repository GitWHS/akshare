#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2024/05/23 14:00
Desc: 个股新闻数据
https://so.eastmoney.com/news/s?keyword=%E4%B8%AD%E5%9B%BD%E4%BA%BA%E5%AF%BF&pageindex=1&searchrange=8192&sortfiled=4
"""

import json

import pandas as pd
import requests


def stock_news_em(keyword: str = "300059") -> pd.DataFrame:
    """
    东方财富-个股新闻-最近 100 条新闻
    https://so.eastmoney.com/news/s?keyword=%E4%B8%AD%E5%9B%BD%E4%BA%BA%E5%AF%BF&pageindex=1&searchrange=8192&sortfiled=4
    :param symbol: 股票代码
    :type symbol: str
    :return: 个股新闻
    :rtype: pandas.DataFrame
    """
    url = "http://search-api-web.eastmoney.com/search/jsonp"
    params = {
        "cb": "jQuery3510875346244069884_1668256937995",
        "param": '{"uid":"",'
        + f'"keyword":"{keyword}"'
        + ',"type":["cmsArticleWebOld"],"client":"web","clientType":"web","clientVersion":"curr",'
        '"param":{"cmsArticleWebOld":{"searchScope":"default","sort":"default","pageIndex":1,'
        '"pageSize":100,"preTag":"<em>","postTag":"</em>"}}}',
        "_": "1668256937996",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(
        data_text.strip("jQuery3510875346244069884_1668256937995(")[:-1]
    )
    temp_df = pd.DataFrame(data_json["result"]["cmsArticleWebOld"])
    temp_df.rename(
        columns={
            "date": "发布时间",
            "mediaName": "文章来源",
            "code": "编号",
            "title": "新闻标题",
            "content": "新闻内容",
            "url": "新闻链接",
            "image": "-",
        },
        inplace=True,
    )
    temp_df["关键词"] = "keyword_" + keyword
    temp_df = temp_df[
        [
            "编号",
            "关键词",
            "新闻标题",
            "新闻内容",
            "发布时间",
            "文章来源",
            "新闻链接",
        ]
    ]
    temp_df["新闻标题"] = (
        temp_df["新闻标题"]
        .str.replace(r"\(<em>", "", regex=True)
        .str.replace(r"</em>\)", "", regex=True)
    )
    temp_df["新闻标题"] = (
        temp_df["新闻标题"]
        .str.replace(r"<em>", "", regex=True)
        .str.replace(r"</em>", "", regex=True)
    )
    temp_df["新闻内容"] = (
        temp_df["新闻内容"]
        .str.replace(r"\(<em>", "", regex=True)
        .str.replace(r"</em>\)", "", regex=True)
    )
    temp_df["新闻内容"] = (
        temp_df["新闻内容"]
        .str.replace(r"<em>", "", regex=True)
        .str.replace(r"</em>", "", regex=True)
    )
    temp_df["新闻内容"] = temp_df["新闻内容"].str.replace(r"\u3000", "", regex=True)
    temp_df["新闻内容"] = temp_df["新闻内容"].str.replace(r"\r\n", " ", regex=True)
    return temp_df


def stock_news_list_info(code, code_type) -> pd.DataFrame:
    from akshare.fund.fund_etf_em import _fund_etf_code_id_map_em
    from akshare.fund.fund_lof_em import _fund_lof_code_id_map_em

    etf_map = _fund_etf_code_id_map_em()
    lof_map = _fund_lof_code_id_map_em()

    if code_type == "A股主板上海":
        secid_list = ["1"]
    elif code_type == "A股主板深圳":
        secid_list = ["0"]
    elif code_type == "A股主板北京":
        secid_list = ["0"]
    elif code_type == "科创板":
        secid_list = ["1"]
    elif code_type == "概念":
        secid_list = ["90"]
    elif code_type == "行业":
        secid_list = ["90"]
    elif code_type == "ETF":
        secid = str(etf_map.get(code, ""))
        if secid != "":
            secid_list = [secid]
        else:
            secid_list = ["1", "0"]
    elif code_type == "LOF":
        secid = str(lof_map.get(code, ""))
        if secid != "":
            secid_list = [secid]
        else:
            secid_list = ["1", "0"]
    else:
        raise Exception("invalid code:" + code)

    for secid in secid_list:
        try:
            url = "https://np-listapi.eastmoney.com/comm/web/getListInfo"
            params = {
                "cfh": "1",
                "client": "web",
                "mTypeAndCode": f"{secid}.{code}",
                "type": "1",
                "pageSize": "200",
                "callback": "jQuery35107504809342017689_1722167990793",
                "_":"1722167990794"
            }
            # proxies = {
            #     "http": "http://192.168.1.3:55930",
            #     "https": "http://192.168.1.3:55930",
            # }
            r = requests.get(url, params=params)
            data_text = r.text
            data_json = json.loads(
                data_text.strip("jQuery35107504809342017689_1722167990793(")[:-1]
            )
            temp_df = pd.DataFrame(data_json["data"]["list"])
            temp_df.rename(
                columns={
                    "Art_ShowTime": "发布时间",
                    "Art_Code": "编号",
                    "Np_dst": "文章来源",
                    "Art_Title": "新闻标题",
                    "Art_Url": "新闻链接",
                },
                inplace=True,
            )
            temp_df["关键词"] = "info_" + f"{secid}.{code}"
            temp_df["新闻内容"] = ""
            temp_df = temp_df[
                [
                    "编号",
                    "关键词",
                    "新闻标题",
                    "新闻内容",
                    "发布时间",
                    "文章来源",
                    "新闻链接",
                ]
            ]
            return temp_df
        except Exception as e:
            # traceback.print_exc()
            print("error secid", code)
            pass


if __name__ == "__main__":
    stock_news_list_info_df = stock_news_list_info("BK0428", '行业')
    print(stock_news_list_info_df)

    # stock_news_em_df = stock_news_em(symbol="标普")
    # print(stock_news_em_df)
