import socket
from urllib.parse import unquote
from org.excuter import excutefun
import json
def handle_request(conn, addr):
    try:
        parammap = "{}"
        # 接收数据（最多1024字节）
        data = conn.recv(1024)
        if not data:
            # 如果没有接收到数据，关闭连接
            return

            # 解码并解析请求
        request_data = data.decode('utf-8')
        start = request_data.find('/')
        end = request_data.find('HTTP')
        if start == -1 or end == -1:
            # 如果找不到URL或HTTP关键字，返回错误
            response = b'HTTP/1.1 400 Bad Request\r\n\r\n'
        else:
            url = request_data[start + 1:end].strip()
            url = unquote(url)
            module = url[0:url.find("!")]
            functionname = ""
            if (url.find("?") == -1):
                functionname = url[url.find("!") + 1:]
            else:
                functionname = url[url.find("!") + 1:url.find("?")]
                strparams = url[url.find("?") + 1:]

                if (strparams.find("&") == -1):
                    name_value = strparams.split("=")
                    name = name_value[0]
                    value = name_value[1]
                    parammap = {name: value}
                else:
                    name_value_s = strparams.split("&")
                    parammap = {key.split("=")[0]: key.split("=")[1] for key in name_value_s}

            returnvalue = ""
            try:
                returnvalue = excutefun(module, functionname, parammap)
            except:
                returnvalue = "映射找不到..."
                if(url != 'favicon.ico'):
                    print("映射找不到...")

            # 构建响应
            ##response_body = f"{json.dumps(returnvalue)}".encode('utf-8')
            response_body = json.dumps(returnvalue, ensure_ascii=False).encode('utf-8')
            response = (
                    b'HTTP/1.1 200 OK\r\n'
                    b'Content-Type:application/json; charset=utf-8\r\n'
                    b'Access-Control-Allow-Origin: *\r\n'
                    b'\r\n'
                    + response_body
            )
            # 发送响应
        conn.sendall(response)
    except Exception as e:
        print(f"Error handling request from {addr}: {e}")
    finally:
        # 无论如何都关闭连接
        conn.close()

def start_server(host='127.0.0.1', port=80):
    print('port:',port)
    with socket.socket() as sock:
        sock.bind((host, port))
        sock.listen(5)
        ##print(f"Server is listening on {host}:{port}")
        try:
            while True:
                conn, addr = sock.accept()
                #print(f"Accepted connection from {addr}")
                # 使用新的线程或进程来处理请求，以避免阻塞主线程
                # 这里为了简化，我们直接在主线程中处理
                handle_request(conn, addr)
        except KeyboardInterrupt:
            print("Server is shutting down")


if __name__ == "__main__":
    start_server()