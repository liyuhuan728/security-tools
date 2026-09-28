#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
port_scanner.py —— 多线程 TCP 端口扫描器
================================================================
⚠️ 使用声明：本工具仅用于你自己搭建的实验环境和获得明确授权的测试目标。
   未经授权对他人主机或网络进行扫描是违法行为，请不要这么做。

原理（三句话）：
  1. 一台主机有 65535 个端口，跑着不同服务（80 是网页，22 是 SSH，3306 是数据库）。
  2. TCP 连接就像敲门：敲开了（能建立连接）说明这个端口有服务在听；被拒绝说明没开。
  3. 一个个敲太慢，所以开多线程，同时敲几百个门。

你会在这份代码里用到的知识点：
  · socket        —— 网络编程的地基，所有安全工具都从它长出来
  · 多线程        —— ThreadPoolExecutor，搞懂为什么扫描必须并发
  · 异常处理      —— 网络编程里"连不上"是常态，不是 bug
  · argparse      —— 让脚本能接命令行参数，像个正经工具
----------------------------------------------------------------
作者：李瑜桓（网络空间安全 · 大一）
"""

import socket
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 常见端口对应的服务名。扫出来之后把数字翻译成"这是干嘛的"
COMMON_PORTS = {
    21: "FTP 文件传输",
    22: "SSH 远程登录",
    23: "Telnet 远程登录(明文,不安全)",
    25: "SMTP 邮件发送",
    53: "DNS 域名解析",
    80: "HTTP 网页",
    110: "POP3 邮件接收",
    135: "Windows RPC",
    139: "NetBIOS",
    143: "IMAP 邮件接收",
    443: "HTTPS 加密网页",
    445: "Windows 文件共享",
    1433: "SQL Server 数据库",
    3306: "MySQL 数据库",
    3389: "Windows 远程桌面",
    5432: "PostgreSQL 数据库",
    6379: "Redis 缓存数据库",
    8080: "HTTP 代理/备用网页端口",
    9000: "常见 Web 服务端口",
}


def scan_port(host: str, port: int, timeout: float):
    """
    尝试与 host:port 建立一次 TCP 连接。
    返回 (端口号, 是否开放, 服务名)。

    为什么用 with? —— socket 是系统资源,不关会泄漏。
    为什么只连不发数据? —— 对很多服务来说,连上就够了,能知道它在。
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        # connect 成功 = 三次握手完成 = 端口开放
        sock.connect((host, port))
        return port, True, COMMON_PORTS.get(port, "未知服务")
    except (socket.timeout, ConnectionRefusedError, OSError):
        # 超时 / 拒绝 / 网络不可达,都算"没开"。这是正常结果,不是错误。
        return port, False, None
    finally:
        sock.close()


def parse_ports(ports_str: str):
    """
    把用户输入的端口串解析成列表。支持两种写法:
      "80,443,3306"  -> [80, 443, 3306]
      "1-1024"       -> [1, 2, 3, ..., 1024]
    """
    ports = set()
    for part in ports_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end) + 1))
        elif part:
            ports.add(int(part))
    return sorted(p for p in ports if 1 <= p <= 65535)


def resolve(host: str) -> str:
    """域名转 IP。扫描器只认 IP,所以要先把域名翻译成地址。"""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        raise SystemExit(f"[!] 无法解析主机: {host}")


def main():
    parser = argparse.ArgumentParser(
        description="多线程 TCP 端口扫描器（仅用于授权环境）",
        epilog="示例: python port_scanner.py 127.0.0.1 -p 1-1024",
    )
    parser.add_argument("host", nargs="?", default="127.0.0.1",
                        help="目标主机,IP 或域名,默认扫本机 127.0.0.1")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="端口范围,如 '1-1024' 或 '80,443,3306',默认 1-1024")
    parser.add_argument("-t", "--threads", type=int, default=100,
                        help="并发线程数,默认 100(太大容易被防火墙当成攻击)")
    parser.add_argument("--timeout", type=float, default=0.5,
                        help="单端口超时秒数,默认 0.5(网络差可调到 1-2)")
    args = parser.parse_args()

    ip = resolve(args.host)
    ports = parse_ports(args.ports)

    print("=" * 52)
    print(f"  目标     : {args.host}  ({ip})")
    print(f"  端口数   : {len(ports)} 个 ({args.ports})")
    print(f"  并发     : {args.threads} 线程   超时 {args.timeout}s")
    print("=" * 52)
    print("  扫描中...\n")

    start = time.time()
    open_ports = []

    # 线程池:把 1024 次"敲门"分配给 100 个线程同时干
    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        futures = {pool.submit(scan_port, ip, p, args.timeout): p for p in ports}
        for future in as_completed(futures):
            port, is_open, service = future.result()
            if is_open:
                open_ports.append((port, service))
                print(f"  [+] {port:<6} 开放    {service}")

    elapsed = time.time() - start

    print("\n" + "=" * 52)
    if open_ports:
        print(f"  扫描完成,发现 {len(open_ports)} 个开放端口:")
        for port, service in sorted(open_ports):
            print(f"      {port:<6} {service}")
    else:
        print("  扫描完成,未发现开放端口。")
        print("  提示:先确认目标主机开机,或把 --timeout 调大再试。")
    print(f"  耗时 {elapsed:.2f} 秒")
    print("=" * 52)


if __name__ == "__main__":
    main()
