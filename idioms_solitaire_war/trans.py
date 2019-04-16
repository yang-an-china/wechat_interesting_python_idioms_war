# encoding=utf8

import random
import time

def get_idioms(file):
    """
    获取所有成语
    返回值:[ ['正襟危坐', 'zheng.jin.wei.zuo'], ['正人君子', 'zheng.ren.jun.zi'], ... ]
    """
    idioms = []
    with open(file, "r") as f:
        idioms = [x.strip('\r\n').split(' ') for x in f.readlines()]
    return idioms

def idioms_to_dict(idioms):
    """
    获取所有成语 拆分模式
    返回值: ['正襟危坐', '正人君子', ...], ['zheng.jin.wei.zuo', 'zheng.ren.jun.zi', ...]
    """
    return zip(*idioms)

def get_start_pinyin_set(idioms):
    """
    获取成语的第一个字的拼音集合
    """
    start_pinyin_set = {}
    for idiom in idioms:
        [hz, py] = idiom
        start = py.split('.')[0]  # 成语第一个字拼音
        if start not in start_pinyin_set:
            start_pinyin_set[start] = [(hz, py)]
        else:
            start_pinyin_set[start].append((hz, py))
    return start_pinyin_set

def cal_run_time(f):
    def wrapper(*args,**kws):
        start = time.time()
        ret = f(*args,**kws)
        end = time.time()
        print("{} using {} ms".format(f.__name__, str((end-start)*1000)))
        return ret
    return wrapper

STEP = 0.001
KILL = 100000
#TRANS_COUNT = 20000
TRANS_COUNT = int(KILL / STEP)

def tran_once(idioms, start_pinyin_set, depth):
    r = random.choice(idioms)
    flag = False
    back = []
    while depth:
        depth -= 1
        end = r[1].split('.')[-1]
        if end in start_pinyin_set:
            r = random.choice(start_pinyin_set[end])
            back.append(r[0])
        else:
            flag = True
            break
    return flag, back

def tran_more(idioms, start_pinyin_set, depth, trans_count):
    hanyus, pinyins = idioms_to_dict(idioms)
    p = dict(zip(hanyus, [0] * len(hanyus)))
    start = time.time()
    while trans_count:
        trans_count -= 1
        if not (trans_count%10000):
            end = time.time()
            print("{} using {} ms".format(trans_count, str((end-start)*1000)))
            start = end
        flag, back = tran_once(idioms, start_pinyin_set, depth)
        if flag:
            for index, x in enumerate(back):
                p[x] += (index+1)*STEP
            if back:
                p[back[-1]] = KILL
    return p

def trans():
    idioms = get_idioms(u"成语大全.txt")
    start_pinyin_set = get_start_pinyin_set(idioms)
    p = tran_more(idioms, start_pinyin_set, 10000, TRANS_COUNT)

    with open("trans" + time.strftime("_%Y%m%d_%H%M%S") + ".txt", "w") as dst:
        for index in range(len(p)):
            dst.write(idioms[index][0] + ' ' + idioms[index][1] + ' ' + str(p[idioms[index][0]]) + '\r\n')

if __name__ == "__main__":
    trans()
    pass
