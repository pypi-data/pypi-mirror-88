import socket
from urllib.parse import urlparse


class HttpWebRequest(object):

    @classmethod
    def get(cls, url: str, headers=None):
        return cls._request("GET", url, headers)

    @classmethod
    def _request(cls, method: str, url: str, headers: dict):
        try:
            headers_str = ""
            if method == 'GET':
                headers_str += "GET "
            elif method == "POST":
                headers_str += "POST "
            else:
                return None

            parsed_uri = urlparse(url)
            headers_str += parsed_uri.path + "?" + parsed_uri.query + " HTTP/1.1\r\n"
            host = parsed_uri.netloc
            scheme = parsed_uri.scheme  # 'http'、'https'、''
            headers_str += "Host: " + host + "\r\n"

            if headers:
                header_keys_lower = [k.lower() for k, v in headers.items()]
            else:
                headers_str += "Accept-Encoding: gzip, deflate\r\n"
                headers_str += "Accept: */*\r\n"
                headers_str += "Connection: keep-alive\r\n\r\n"

            tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_client.settimeout(200)  # 200秒
            if scheme == 'https':
                port = 443
            else:
                port = 80
            tcp_client.connect((host, port))
            tcp_client.sendall(str.encode(headers_str))
            result = bytearray(b'')
            while True:
                data = tcp_client.recv(1024)
                result.extend(data)
                if not data:
                    break
            # TODO
            # 应返回：消息头 + 内容， 需要结构化数据，同时数部分应该解码
            # 参考：http://www.zeroplace.cn/article.asp?id=985
            return result
        except Exception as e:
            print(repr(e))
        finally:
            if tcp_client:
                tcp_client.close()
