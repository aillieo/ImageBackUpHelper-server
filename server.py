#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import cgi
if sys.version_info >= (3, 0):
    from http import server as httpserver
    from urllib import parse as urllibparse
    unicode = str
else:
    import BaseHTTPServer as httpserver
    import urllib as urllibparse


class MyHandler(httpserver.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllibparse.urlparse(self.path)
        message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address, self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))
        return

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     }
        )
        self.send_response(200)
        self.end_headers()
        self.wfile.write(('Client: %sn ' % str(self.client_address)).encode("utf-8"))
        self.wfile.write(('User-agent: %sn' % str(self.headers['user-agent'])).encode("utf-8"))
        self.wfile.write(('Path: %sn' % self.path).encode("utf-8"))
        self.wfile.write('Form data:n'.encode("utf-8"))
        for field in form.keys():
            field_item = form[field]
            filename = field_item.filename
            filevalue = field_item.value
            filesize = len(filevalue)
            print(filesize)
            with open(filename +'a', 'wb') as f:
                f.write(filevalue)
        return


if __name__ == '__main__':
    server = httpserver.HTTPServer(('localhost', 8080), MyHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
