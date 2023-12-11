import base64
from flask import Flask, request, Request, render_template, jsonify, blueprints
import json
import os


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')
    

@app.route('/Encrypt', methods=['GET', 'POST'])
def Encrypt():

    if request.method == "GET":
        dicts = {}
        return jsonify(dicts)
    if request.method == "POST":

        key = request.form.get("key")
        expt = request.form.get("expt")
        mode = request.form.get("mode")

        key = bytes(key, encoding = 'utf-8')
        expt=bytes(expt, encoding = 'utf-8')

        if mode =='DES':
            d = DES(key)
            cipt = d.Encrypt(expt)
        if mode =='AES':
            a = AES(key)
            cipt = a.Encrypt(expt)

        # 必须要用base64转换一下才能得到密文的string
        base64_bytes = base64.b64encode(cipt)
        str_cipt = base64_bytes.decode('utf-8')

        # base64_bytes = str_cipt.encode('utf-8')
        # byte_cipt = base64.b64decode(base64_bytes)
        #
        # mm = d.Decrypt(byte_cipt)
        # print(mm.decode('utf-8').strip(b'\x00'.decode()))

        dicts = {'str_cipt':str_cipt}
        return jsonify(dicts)

@app.route('/Decrypt', methods=['GET', 'POST'])
def Decrypt():

    if request.method == "GET":
        dicts = {}
        return jsonify(dicts)
    if request.method == "POST":

        key = request.form.get("key")
        str_cipt = request.form.get("cipt")
        mode = request.form.get("mode")

        key = bytes(key, encoding='utf-8')

        base64_bytes = str_cipt.encode('utf-8')
        byte_cipt = base64.b64decode(base64_bytes)

        if mode == 'DES':
            d = DES(key)
            byte_expt = d.Decrypt(byte_cipt)
        if mode == 'AES':
            a = AES(key)
            byte_expt = a.Decrypt(byte_cipt)

        str_expt = byte_expt.decode('utf-8').strip(b'\x00'.decode())

        dicts={'str_expt':str_expt}
        return jsonify(dicts)

S_Box = [
    [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
     0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
    [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
     0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
    [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC,
     0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
    [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A,
     0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
    [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
     0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
    [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B,
     0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
    [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85,
     0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
    [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
     0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
    [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17,
     0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
    [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88,
     0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
    [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
     0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
    [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9,
     0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
    [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6,
     0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
    [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
     0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
    [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94,
     0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
    [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68,
     0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]]

Inv_S_Box = [
    [0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38,
     0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB],
    [0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87,
     0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB],
    [0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D,
     0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E],
    [0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2,
     0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25],
    [0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16,
     0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92],
    [0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA,
     0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84],
    [0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A,
     0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06],
    [0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02,
     0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B],
    [0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA,
     0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73],
    [0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85,
     0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E],
    [0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89,
     0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B],
    [0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20,
     0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4],
    [0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31,
     0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F],
    [0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D,
     0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF],
    [0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0,
     0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61],
    [0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26,
     0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D]]

# 轮常数，密钥扩展中用到。（AES-128只需要10轮）
Rcon = [0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000,
        0x20000000, 0x40000000, 0x80000000, 0x1b000000, 0x36000000]


# 密钥扩展
# 字循环左移一个字节
def RotWord(x):
    return ((x << 8) | (x >> 24)) & 0xffffffff


# S盒变换
def SubWord(x):
    temp = 0
    temp = (temp << 8) | S_Box[(x >> 28) & 0x0f][(x >> 24) & 0x0f]
    temp = (temp << 8) | S_Box[(x >> 20) & 0x0f][(x >> 16) & 0x0f]
    temp = (temp << 8) | S_Box[(x >> 12) & 0x0f][(x >> 8) & 0x0f]
    temp = (temp << 8) | S_Box[(x >> 4) & 0x0f][(x >> 0) & 0x0f]
    return temp


# 加密过程
# 轮密钥加变换 - 将每一列与扩展密钥进行异或
def AddRoundKey(mtx, ikey):
    rmtx = []
    for i in range(4):
        for j in range(4):
            rmtx.append((mtx[4 * i + j] ^ ((ikey[j] << 8 * i) >> 24)) & 0xff)
    return bytes(rmtx)


# S盒变换 - 前4位为行号，后4位为列号
def Subbytes(mtx):
    rmtx = []
    for i in mtx:
        rmtx.append(S_Box[i >> 4][i & 0x0f])
    return bytes(rmtx)


# 行变换 - 按字节循环移位
def ShiftRows(mtx):
    rmtx = b''
    rmtx += mtx[0:4] + \
            mtx[5:8] + mtx[4:5] + \
            mtx[10:12] + mtx[8:10] + \
            mtx[15:16] + mtx[12:15]
    return rmtx


# 有限域上的乘法 GF(2^8)
def GFMul(a, b):
    p, hi_bit_set = 0, 0
    for counter in range(8):
        if b & 1 != 0:
            p ^= a
        hi_bit_set = a & 0x80
        a = (a << 1) & 0xff
        if hi_bit_set != 0:
            a ^= 0x1b  # x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return p & 0xff


# 列变换
def MixColumns(mtx):
    rmtx = [0] * 16
    for i in range(4):
        arr = []
        for j in range(4):
            arr.append(mtx[i + j * 4])
        rmtx[i] = GFMul(0x02, arr[0]) ^ GFMul(0x03, arr[1]) ^ arr[2] ^ arr[3]
        rmtx[i + 4] = arr[0] ^ GFMul(0x02, arr[1]) ^ GFMul(0x03, arr[2]) ^ arr[3]
        rmtx[i + 8] = arr[0] ^ arr[1] ^ GFMul(0x02, arr[2]) ^ GFMul(0x03, arr[3])
        rmtx[i + 12] = GFMul(0x03, arr[0]) ^ arr[1] ^ arr[2] ^ GFMul(0x02, arr[3])
    return bytes(rmtx)


# 解密过程
# 逆行变换 - 按字节循环移位
def InvShiftRows(mtx):
    rmtx = b''
    rmtx += mtx[0:4] + \
            mtx[7:8] + mtx[4:7] + \
            mtx[10:12] + mtx[8:10] + \
            mtx[13:16] + mtx[12:13]
    return rmtx


# 逆S盒变换 - 前4位为行号，后4位为列号
def InvSubbytes(mtx):
    rmtx = []
    for i in mtx:
        rmtx.append(Inv_S_Box[i >> 4][i & 0x0f])
    return bytes(rmtx)


# 逆列变换
def InvMixColumns(mtx):
    rmtx = [0] * 16
    for i in range(4):
        arr = []
        for j in range(4):
            arr.append(mtx[i + j * 4])
        rmtx[i] = GFMul(0x0e, arr[0]) ^ GFMul(0x0b, arr[1]) ^ GFMul(0x0d, arr[2]) ^ GFMul(0x09, arr[3])
        rmtx[i + 4] = GFMul(0x09, arr[0]) ^ GFMul(0x0e, arr[1]) ^ GFMul(0x0b, arr[2]) ^ GFMul(0x0d, arr[3])
        rmtx[i + 8] = GFMul(0x0d, arr[0]) ^ GFMul(0x09, arr[1]) ^ GFMul(0x0e, arr[2]) ^ GFMul(0x0b, arr[3])
        rmtx[i + 12] = GFMul(0x0b, arr[0]) ^ GFMul(0x0d, arr[1]) ^ GFMul(0x09, arr[2]) ^ GFMul(0x0e, arr[3])
    return bytes(rmtx)


class AES(object):
    # AES-128
    #    Nk密钥长度(双字)，Nb分组大小(双字)，Nr轮数
    # 128   4               4               10 
    # 192   6               4               12
    # 256   8               4               14
    # 128 4*4*8=128bits   4*4*8=128bits     10轮
    def __init__(self, K: bytes):
        self.Nk, self.Nb, self.Nr = 4, 4, 10
        # 通过密钥K生成实例，密钥K位数不足补零
        self.K = K[:self.Nk * 4]
        while len(self.K) < self.Nk * 4:
            self.K += b'\x00'
        self.W = self.KeyExpansion()

    def Encrypt(self, m: bytes) -> bytes:
        # 加密
        # 明文不足16*8bits补零
        while len(m) % 16 != 0:
            m += b'\x00'
        c = b''
        for i in range(len(m) // 16):
            # 对每一个16*8bits的块进行循环
            mtx = m[i * 16:i * 16 + 16]
            ikey = self.W[:4]
            mtx = AddRoundKey(mtx, ikey)
            for round in range(1, self.Nr):
                mtx = Subbytes(mtx)
                mtx = ShiftRows(mtx)
                mtx = MixColumns(mtx)
                ikey = self.W[4*round:4*round+4]
                mtx = AddRoundKey(mtx, ikey)
            mtx = Subbytes(mtx)
            mtx = ShiftRows(mtx)
            ikey = self.W[4 * self.Nr:]
            mtx = AddRoundKey(mtx, ikey)
            c += mtx
        return c

    def Decrypt(self, m: bytes) -> bytes:
        # 解密
        c = b''
        for i in range(len(m) // 16):
            mtx = m[i * 16:i * 16 + 16]
            ikey = self.W[self.Nr * 4:]
            mtx = AddRoundKey(mtx, ikey)
            for round in range(self.Nr-1, 0, -1):
                mtx = InvShiftRows(mtx)
                mtx = InvSubbytes(mtx)
                ikey = self.W[4 * round:4 * round + 4]
                mtx = AddRoundKey(mtx, ikey)
                mtx = InvMixColumns(mtx)
            mtx = InvShiftRows(mtx)
            mtx = InvSubbytes(mtx)
            ikey = self.W[:4]
            mtx = AddRoundKey(mtx, ikey)
            c += mtx
        return c

    def KeyExpansion(self):
        # 密钥扩展函数，密钥 K 扩展生成 Nb(Nr+1)个字  4*4*8bits=128bits -> 4*(10+1)*32bits=1408bits
        w = []
        for i in range(self.Nk):
            temp = 0
            for j in range(4):
                temp = (temp << 8) | self.K[4 * i + j]
            w.append(temp)
        for i in range(self.Nk, self.Nb * (self.Nr + 1)):
            temp = w[i - 1]
            if i % self.Nk == 0:
                temp = SubWord(RotWord(temp)) ^ Rcon[i // self.Nk - 1]
            elif self.Nk > 6 and i % self.Nk == 4:
                temp = SubWord(temp)
            w.append(w[i - self.Nk] ^ temp)
        return w

    def getK(self) -> bytes:
        # 返回密钥K
        return self.K

    def generateK(self) -> bytes:
        # 随机产生密钥K
        pass


def print_bytes_hex(m):
    for i in m:
        print(hex(i)[2:].rjust(2, '0'), end='')
    print()





IP = (58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7)
FP = (40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25)
E = (32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1)
P = (16, 7, 20, 21,
     29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2, 8, 24, 14,
     32, 27, 3, 9,
     19, 13, 30, 6,
     22, 11, 4, 25)
S = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
      [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
      [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
      [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

     [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
      [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
      [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
      [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

     [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
      [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
      [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
      [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

     [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
      [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
      [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
      [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

     [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
      [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
      [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
      [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

     [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
      [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
      [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
      [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

     [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
      [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
      [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
      [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

     [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
      [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
      [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
      [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
PC_1L = (57, 49, 41, 33, 25, 17, 9,
         1, 58, 50, 42, 34, 26, 18,
         10, 2, 59, 51, 43, 35, 27,
         19, 11, 3, 60, 52, 44, 36)
PC_1R = (63, 55, 47, 39, 31, 23, 15,
         7, 62, 54, 46, 38, 30, 22,
         14, 6, 61, 53, 45, 37, 29,
         21, 13, 5, 28, 20, 12, 4)
PC_2 = (14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32)


def Permute(block, b_len, PP):
    # 通过置换矩阵PP对block进行置换,b_len是块长度(位，bit)
    res = 0
    for i in PP:
        res = res << 1
        # 第i-1的位置 即倒数第
        res |= (block >> (b_len - i)) & 0x01
    return res


def bytesToblocks(m):
    # 字节序列转换位blocks    b'\x00\x01\x02\x03\xff\xff\xff\xff' -> [0x00010203,0xffffffff]
    while len(m) % 8 != 0 or len(m)==0:
        m += b'\x00'
    blocks = []
    for i in range(len(m) // 4):
        blocks.append((m[4 * i] << 24) | (m[4 * i + 1] << 16) |
                      (m[4 * i + 2] << 8) | (m[4 * i + 3]))
    return blocks


def blocksTobytes(blocks):
    # blocks转换为字节序列    [0x00010203,0xffffffff] -> b'\x00\x01\x02\x03\xff\xff\xff\xff'
    res = b''
    for i in blocks:
        res += i.to_bytes(4, byteorder="big")
    return res


L = lambda x, n: ((x << n) | (x >> (28 - n))) & 0x0fffffff
# 对一个28bits的数x进行循环左移n位

class DES(object):

    def F(self, block, subKeyid):
        """

        :param block: 32bits
        :param subKeyid:
        :return: res: 32bits
        """
        temp = Permute(block, 32, E) ^ self.subKs[subKeyid]
        res = 0
        for i in range(8):
            res = res << 4
            yxxxxy = (temp >> 6 * (7 - i)) & 0x3f
            xxxx = (yxxxxy & 0x1f) >> 1
            yy = ((yxxxxy >> 5) << 1) | (yxxxxy & 0x01)
            res |= S[i][yy][xxxx]
        res = Permute(res, 32, P)
        return res & 0xffffffff

    def __init__(self, K: bytes):
        # 通过密钥K生成实例
        self.K = K
        self.K_blocks = bytesToblocks(K)[:2]
        # 生成字密钥self.subKs[16]
        self.subKs = None
        self.generate_subKs()

    def Encrypt(self, m: bytes) -> bytes:
        # 加密
        blocks = bytesToblocks(m)
        cblocks = []
        for i in range(len(blocks) // 2):
            # 每个64bits的高32bits，低32bits
            high, low = blocks[2 * i], blocks[2 * i + 1]
            # 第一步：初始置换IP
            temp = Permute((high << 32) | low, 64, IP) & 0xffffffffffffffff
            # 第二步：获取 Li 和 Ri
            high, low = temp >> 32, temp & 0xffffffff
            # 第三步：共16轮迭代
            for j in range(16):
                high, low = low, (high ^ self.F(low, j))
            # 第四步：合并L16和R16，注意合并为 R16L16
            high, low = low, high
            # 第五步：末尾置换FP
            temp = Permute((high << 32) | low, 64, FP) & 0xffffffffffffffff
            high, low = temp >> 32, temp & 0xffffffff
            cblocks.append(high)
            cblocks.append(low)
        return blocksTobytes(cblocks)

    def Decrypt(self, e: bytes) -> bytes:
        # 解密
        blocks = bytesToblocks(e)
        cblocks = []
        for i in range(len(blocks) // 2):
            # 每个64bits的高32bits，低32bits
            high, low = blocks[2 * i], blocks[2 * i + 1]
            # 第一步：初始置换IP
            temp = Permute((high << 32) | low, 64, IP) & 0xffffffffffffffff
            # 第二步：获取 Li 和 Ri
            high, low = temp >> 32, temp & 0xffffffff
            # 第三步：共16轮迭代, 子密钥逆序
            for j in range(16):
                high, low = low, (high ^ self.F(low, 15 - j))
            # 第四步：合并L16和R16，注意合并为 R16L16
            high, low = low, high
            # 第五步：末尾置换FP
            temp = Permute((high << 32) | low, 64, FP) & 0xffffffffffffffff
            high, low = temp >> 32, temp & 0xffffffff
            cblocks.append(high)
            cblocks.append(low)
        return blocksTobytes(cblocks)

    def generate_subKs(self):
        # print(bin((self.K_blocks[0] << 32) | self.K_blocks[1])[2:].rjust(32, '0'))
        C = Permute((self.K_blocks[0] << 32) | self.K_blocks[1], 64, PC_1L)  & 0x0fffffff
        D = Permute((self.K_blocks[0] << 32) | self.K_blocks[1], 64, PC_1R)  & 0x0fffffff
        # print(bin(C)[2:].rjust(28, '0'))
        # print(bin(D)[2:].rjust(28, '0'))
        self.subKs = []
        for i in range(16):
            if i in (0, 1, 8, 15):
                C, D = L(C, 1), L(D, 1)
            else:
                C, D = L(C, 2), L(D, 2)
            self.subKs.append(Permute((C << 28) | D, 56, PC_2))
            # print(hex(self.subKs[i]))

    def getK(self) -> bytes:
        # 返回密钥K
        return self.K

    def generateK(self) -> bytes:
        # 随机产生密钥K
        pass


def print_bytes_hex(m):
    for i in m:
        print(hex(i)[2:].rjust(2, '0'), end='')
    print()


if __name__ == '__main__':
    # 密钥不足64bits 添零，多于64bits 使用前64bits
    # messages 不足64bits的倍数 补零
    m = b'zengjie123213' # 明文
    k = b'' # 密钥
    a = DES(k)
    cc = a.Encrypt(m)
    mm = a.Decrypt(cc)
    print("明文:", end='')
    print(m)
    print("密钥:", end='')
    print(a.K)
    print("密文:", end='')
    print_bytes_hex(cc)  # 以bytes输出
    print("解密:", end='')
    print(mm)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')