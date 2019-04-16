# encoding=utf8
# python 3
# https://github.com/yang-an-china/wechat_interesting_python_idioms_war

import matplotlib.pyplot as plt

def get_idioms(file):
    """
    获取所有成语
    返回值:[ ['正襟危坐', 'zheng.jin.wei.zuo'], ['正人君子', 'zheng.ren.jun.zi'], ... ]
    """
    idioms = []
    with open(file, "r") as f:
        idioms = [x.strip('\n').split(' ') for x in f.readlines()]
    return idioms


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


def check_idiom_dead(idioms, start_pinyin_set):
    """
    找出无法被接龙的成语
    """
    idiom_dead = {}
    for idiom in idioms:
        [hz, py] = idiom
        last = py.split('.')[-1]  # 成语最后一个字拼音
        if last not in start_pinyin_set:
            if last not in idiom_dead:
                idiom_dead[last] = [(hz, py)]
            else:
                idiom_dead[last].append((hz, py))
    return idiom_dead


def idiom_dead_stat(idiom_dead):
    """
    统计无法被接龙成语的最后一个字的拼音
    """
    data = sorted([(len(idiom_dead[py]), py)
                   for py in idiom_dead], reverse=True)
    y = [d[0] for d in data]
    y_py = [d[1] for d in data]
    x = range(0, len(y))

    plt.figure(figsize=(10, 6))
    plt.bar(x, y, color='g')
    plt.xticks(x, y_py)
    plt.title('idiom dead', y=0.9)
    plt.show()
    pass

def print_result(idiom_dead):
    count = 0
    for py in idiom_dead:
        if count != 0:
            print('')
        print('`',py,'`', sep='')
        count = 0
        for idiom in idiom_dead[py]:
            print('`',idiom[0],'`',sep='', end=' ')
            count += 1
            if count >= 3:
                print('')
                count = 0

if __name__ == "__main__":
    idioms = get_idioms(u"成语大全.txt")
    start_pinyin_set = get_start_pinyin_set(idioms)
    idiom_dead = check_idiom_dead(idioms, start_pinyin_set)
    idiom_dead_stat(idiom_dead)
    print_result(idiom_dead)
    pass
