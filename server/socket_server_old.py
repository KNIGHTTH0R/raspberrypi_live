#-*- coding: UTF-8 -*-
import socketserver
import struct
import os
import hashlib

host = '0.0.0.0'
port = 12306
ADDR = (host, port)

def calc_md5(f_name):
    with open(f_name, 'rb') as fr:
        md5 = hashlib.md5()
        md5.update(fr.read())
        md5 = md5.hexdigest()
    return md5

class MyRequestHandler(socketserver.BaseRequestHandler):
    # def __init__(self, request, client_address, server):
    #     socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
    #     self.mq_obj = producer.mq_producer()

    def handle(self):
        # self.mq_obj = producer.mq_producer()
        print('connected from:', self.client_address)
        while True:
            # 定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sII32s')
            self.buf = self.request.recv(fileinfo_size)
            if self.buf:  # 如果不加这个if，第一个文件传输完成后会自动走到下一句
                try:
                    self.filename, self.filenamesize, self.filesize,self.md5 = struct.unpack(
                        '128sII32s', self.buf)  # 根据128sII32s解包文件信息，与client端的打包规则相同
                except struct.error as e:
                    print(e)
                    continue
                self.filesize = int(self.filesize)
                # 文件名长度为128，大于文件名实际长度
                self.filename = self.filename[:self.filenamesize]
                self.md5 = self.md5.decode('utf8')
                print('filesize is: ', self.filesize, 'filename size is: ', len(self.filename))
                try:
                    self.filenewname = os.path.join(
                    '/usr/local/project/tmp_video/', ('new_' + self.filename.decode('utf8')).strip('\00').strip('\\x00'))  # 使用strip()删除打包时附加的多余空字符
                except Exception as e:
                    print(e)
                    print(self.filename)
                    continue#出现错误宁愿丢弃文件也不能影响程序运行
                # self.mq_obj.put_message(self.filenewname)
                print(self.filenewname, type(self.filenewname))
                recvd_size = 0  # 定义接收了的文件大小
                file = open(self.filenewname, 'wb')
                print('stat receiving...')
                while not recvd_size == self.filesize:#todo 文件名无法解析 我才是因为这一块计数有问题，或者发送方和接收方的速率不一致
                    if self.filesize - recvd_size > 1024:
                        rdata = self.request.recv(1024)
                        recvd_size += len(rdata)
                    else:
                        rdata = self.request.recv(self.filesize - recvd_size)
                        recvd_size = self.filesize
                    file.write(rdata)
                file.close()
                md5_recv = calc_md5(self.filenewname)
                if md5_recv == self.md5:
                    print('receive done')
                else:
                    print('md5 do not match')
        # self.request.close()


tcpServ = socketserver.ThreadingTCPServer(ADDR, MyRequestHandler)
print('waiting for connection...')
tcpServ.serve_forever()
