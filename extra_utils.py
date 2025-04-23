# !/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import requests

host_list = ["192.168.1.8", "192.168.1.11"]


def get_proxy():
    # 获取当前时间戳（从 1970 年 1 月 1 日 00:00:00 UTC 到现在的秒数）
    timestamp = time.time()
    local_time = time.localtime(timestamp)
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    try:
        # 发送请求到指定接口
        host = host_list[0]
        url = f"http://{host}:52001/get/?http_only=false"
        response = requests.get(url)
        # 检查响应状态码
        if response.status_code == 200:
            proxy_data = response.json()
            if not proxy_data:
                url = f"http://{host}:52001/get/?http_only=true"
                response = requests.get(url)
                proxy_data = response.json()

            if proxy_data:
                proxy_list = proxy_data[0]['m_ip']
                proxy_json = {
                    "http": f"http://{proxy_list[0]}:{proxy_list[1]}",
                    "https": f"http://{proxy_list[0]}:{proxy_list[1]}",
                }
                print(f"{formatted_time} 取得代理：{proxy_list}")
            else:
                print(f"{formatted_time} 无法取得代理")
                proxy_json = None
            return proxy_json
        else:
            print(f"{formatted_time} 请求接口失败，状态码: {response.status_code}")
    except requests.RequestException as e:
        print(f"{formatted_time} 请求发生错误: {e}")
    except Exception:
        print(f"{formatted_time} 无法解析接口返回的 JSON 数据。")
    host_bak = host_list.pop(0)
    host_list.append(host_bak)
    return None


if __name__ == "__main__":
    for i in range(3):
        # 调用函数获取代理
        proxy = get_proxy()
        if proxy:
            print(f"获取到的代理: {proxy}")
        else:
            print("未获取到有效的代理，返回空代理。")
