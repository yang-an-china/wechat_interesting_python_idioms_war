# encoding=utf8
# python 3
# https://github.com/yang-an-china/wechat_interesting_python_idioms_war

import sys
import struct

PIN_YIN_TAG_LEN = 4


def get_hanzi_offset(buff):
    mask = buff[4]
    return 0x2628 if mask == 0x44 else 0x26c4 if mask == 0x45 else None


def get_pinyin_offset(buff):
    offset = 0x1540
    return offset if buff[offset:offset + PIN_YIN_TAG_LEN] == b"\x9d\x01\x00\x00" else None


def get_piyin_table(buff, py_offset, hz_offset):
    py_table = {}
    data = buff[py_offset + PIN_YIN_TAG_LEN:hz_offset]

    pos = 0
    while pos < len(data):
        # 序号
        index = struct.unpack('H', data[pos:pos + 2])[0]
        pos += 2
        # 拼音长度
        l = struct.unpack('H', data[pos:pos + 2])[0]
        pos += 2
        # 拼音
        py = data[pos:pos + l]
        pos += l
        py_table[index] = py.decode('UTF-16LE')
        print(index, l, py.decode('UTF-16LE'))
    return py_table


def get_hanzi_and_pinyin(buff, hz_offset, py_table):

    def _get_py(data, py_table):
        length = len(data)
        pos = 0
        py = u''
        while pos < length:
            index = struct.unpack('H', data[pos:pos + 2])[0]
            py += u'.' + py_table[index]
            pos += 2
        return py[1:]

    hz_all = {}
    pos = 0
    hz_table = buff[hz_offset:]
    while pos < len(hz_table):
        # 同音词数量
        same = struct.unpack('H', hz_table[pos:pos + 2])[0]
        pos += 2
        # 拼音索引表长度
        py_table_len = struct.unpack('H', hz_table[pos:pos + 2])[0]
        pos += 2
        # 拼音索引表
        data = hz_table[pos:pos + py_table_len]
        py = _get_py(data, py_table)
        pos += py_table_len

        print(same, py_table_len, py)
        # 中文词组
        for i in range(same):
            # 中文词组长度
            hz_len = struct.unpack('H', hz_table[pos:pos + 2])[0]
            pos += 2
            # 中文词组
            word = hz_table[pos:pos + hz_len]
            pos += hz_len
            # 扩展数据长度
            ext_len = struct.unpack('H', hz_table[pos:pos + 2])[0]
            pos += 2
            # 序号
            count = struct.unpack('H', hz_table[pos:pos + 2])[0]
            pos += ext_len
            hz_all[count] = (word.decode('UTF-16LE'), py)
            print(hz_len, word.decode('UTF-16LE'), ext_len, count)
    return hz_all


def scel_to_txt(scel, out):
    with open(scel, "rb") as src, open(out, "w") as dst:
        buff = src.read()
        hz_offset = get_hanzi_offset(buff)
        py_offset = get_pinyin_offset(buff)
        if not hz_offset or not py_offset:
            print("scel format changed, not support now \
                [hz_offset = {} py_offset = {}]!".format(hz_offset, py_offset))
            sys.exit(1)

        py_table = get_piyin_table(buff, py_offset, hz_offset)
        hz_py_all = get_hanzi_and_pinyin(buff, hz_offset, py_table)
        for x in hz_py_all:
            dst.write(hz_py_all[x][0] + ' ' + hz_py_all[x][1] + '\n')
    pass


if __name__ == "__main__":
    scel_to_txt(u"成语大全.scel", u"成语大全.txt")
    scel_to_txt(u"常用成语141231.scel", u"常用成语141231.txt")
    pass
