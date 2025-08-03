# !/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import time
import requests
import socket
from concurrent.futures import ThreadPoolExecutor

host_list = ["192.168.1.7", "192.168.1.8"]
target_ports = [52001]


def check_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # 设置超时时间为1秒
            result = s.connect_ex((ip, port))
            if result == 0:
                return ip
    except Exception as e:
        pass
    return None


def scan_network(start_ip, end_ip, port):
    active_hosts = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_ip = {executor.submit(check_port, f"192.168.1.{i}", port): i for i in range(start_ip, end_ip + 1)}
        for future in future_to_ip:
            ip = future.result()
            if ip:
                active_hosts.append(ip)
                print(f"Port {port} is open on {ip}")
    return active_hosts


def get_proxy():
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
                user = proxy_data[0].get("user")
                pwd = proxy_data[0].get("pwd")
                if user and pwd:
                    proxy_url = f"http://{user}:{pwd}@{proxy_list[0]}:{proxy_list[1]}"
                else:
                    proxy_url = f"http://{proxy_list[0]}:{proxy_list[1]}"
                proxy_json = {
                    "http": proxy_url,
                    "https": proxy_url,
                }
                print(f"{formatted_time} host:{host} 取得代理：{proxy_url}")
            else:
                print(f"{formatted_time} host:{host} 无法取得代理")
                proxy_json = None
            return proxy_json
        else:
            print(f"{formatted_time} host:{host} 请求接口失败，状态码: {response.status_code}")
    except requests.RequestException as e:
        print(f"{formatted_time} host:{host} 请求发生错误: {e}")
    except Exception as e:
        print(f"{formatted_time} 无法解析接口返回的 JSON 数据:", e)
    host_bak = host_list.pop(0)
    host_list.append(host_bak)

    for port in target_ports:
        active_hosts = scan_network(2, 254, port)
        print(f"Active host:{active_hosts}: {port}")
        random.shuffle(active_hosts)
        for active_host in active_hosts:
            if active_host not in host_list:
                host_list.insert(0, active_host)

    return None


def get_headers():
    user_agent_pool = [
        # Firefox
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel_3ULD) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Linux Android 11; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0 Safari/537.36",

        # Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux x86_64; Android 12; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",

        # Edge
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36 Edg/120.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0",
        "Mozilla/5.0 (Linux x86_64; Android 12; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0",

        # Safari
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",

        # Opera
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36 OPR/95.0",

        # Internet Explorer
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1)",

        # Chrome for Android
        "Mozilla/5.0 (Linux; Android 12; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36",

        # Firefox for Android
        "Mozilla/5.0 (Linux; Android 12; Mobile) Gecko/20100101 Firefox/113.0",

        "ozilla/3.75 (compatible; Netscape 4.0)",
        "Dalvik/2.1.0 (Linux; Android 9)",
        "iPhone OS 14_7_1 (18G89) AppleWebKit/605.1.15",
        "iPadOS 15.2.1 (16F214) AppleWebKit/605.1.15",
    ]

    v = random.randint(100, 120)
    default_headers = {
        # "Accept": '*/*',
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36"
    }

    return default_headers


if __name__ == "__main__":
    for i in range(3):
        # 调用函数获取代理
        proxy = get_proxy()
        if proxy:
            print(f"获取到的代理: {proxy}")
        else:
            print("未获取到有效的代理，返回空代理。")
