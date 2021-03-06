#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import cgi
import os
if sys.version_info >= (3, 0):
    from http import server as httpserver
    from urllib import parse as urllibparse
    unicode = str
else:
    import BaseHTTPServer as httpserver
    import urllib as urllibparse


def save_file(filename, filevalue):
    if not os.path.exists('backup'):
        os.mkdir('backup')
    file_path_name = os.path.join('backup', filename)
    fpath, fext = os.path.splitext(file_path_name)
    i = 1
    while os.path.exists(file_path_name):
        file_path_name = "%s-%d%s" % (fpath, i, fext)
        i += 1
    with open(file_path_name, 'wb') as f:
        f.write(filevalue)


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
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        print('message: \r\n%s' % message)
        self.wfile.write('{"name":"name","content":"content"}'.encode("utf-8"))
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
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        message_parts = [
                'Client: %s ' % str(self.client_address),
                'User-agent: %s' % str(self.headers['user-agent']),
                'Path: %s' % self.path
                ]
        message = '\r\n'.join(message_parts)
        message += '\r\nForm data:\r\n'
        for field in form.keys():
            field_item = form[field]
            message += ('\t%s=%s\n' % (field, str(field_item.value)[0:100]))
        print('message: \r\n%s' % message)
        self.wfile.write('{"name":"name","content":"content"}'.encode("utf-8"))
        for field in form.keys():
            field_item = form[field]
            filename = field_item.filename
            filevalue = field_item.value
            filesize = len(filevalue)
            #print(filesize)
            if filename:
                save_file(filename, filevalue)
        return


if __name__ == '__main__':
    server = httpserver.HTTPServer(('', 8080), MyHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
