# encoding=utf8

import random
import codecs
import pickle
import time

# 全局
def get_names():
    with open("names.pickle", "rb") as pk:
        return pickle.load(pk)

def get_trans(file):
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

# 全局数据
names = get_names() # 随机名字
trans = get_trans(u"trans.txt") # 训练数据
hanzi, pinyin, p = zip(*trans)
start_pinyin_set = get_start_pinyin_set(zip(hanzi, pinyin))
x = dict(zip(hanzi, pinyin))
y = dict(zip(hanzi, p))
z = dict(zip(pinyin, hanzi))

def strategy(strategy, give, input_idiom = None):
    def _get_start(idiom):
        start = x[idiom].split('.')[0]
        return start if start in start_pinyin_set else None
    def _get_end(idiom):
        end = x[idiom].split('.')[-1]
        return end if end in start_pinyin_set else None

    end = _get_end(give)
    if not end:
        return None

    if strategy == "human":
        if input_idiom in x:
            start = _get_start(input_idiom)
            if start == end:
                return input_idiom
        return None

    if strategy == "primer":
        return z[random.choice(start_pinyin_set[end])[1]]

    if strategy == "expert":
        min_prob = 9999
        got = None
        for key in z:
            if key.split('.')[0] == end:
                candidate = z[key]
                prob = float(y[candidate])
                if prob > 9999:
                    return candidate
                if prob < min_prob:
                    min_prob = prob
                    got = candidate
        return got

class player(object):
    """player"""
    def __init__(self, name = None, strategy = "primer"):
        super(player, self).__init__()
        self._playing = True
        self._strategy = strategy
        self._name = self.__set_name() if not name else name

    def give(self, idiom):
        input_idiom = input("请输入成语：") if self._strategy == "human" else None
        return strategy(self._strategy, idiom, input_idiom) if self._playing else None

    def set_dark(self):
        self._playing = False

    def __set_name(self):
        return input("请输入名字：") if self._strategy == "human" else random.choice(names)

    @property
    def name(self):
        return self._name

    @property
    def strategy(self):
        return self._strategy

    @property
    def is_playing(self):
        return self._playing

class game(object):
    """game"""
    def __init__(self, players):
        super(game, self).__init__()
        self.players = players
        
    def start(self):
        count = len(self.players)
        win = count
        took_part_in = count * [False]
        
        token = 0
        last_token = token
        given = random.choice(hanzi)
        last_given = given
        print(u"随机生成的成语是：{}".format(str(given)))
        while True:
            took_part_in[token] = True
            if self.players[token].is_playing:
                given = self.players[token].give(last_given)
                if given == last_given:
                    break
                if given:
                    last_token = token
                    last_given = given
                else:
                    self.players[token].set_dark()
                    win -= 1
            print("[{}]{}：{}".format(self.players[token].strategy, self.players[token].name, str(given)))

            token += 1
            token = token % count

            if False not in took_part_in and win <= 1:
                break

        print(u"获胜者是：{}".format(self.players[last_token].name) if win > 0 else u"本轮没有获胜者！")
        return (self.players[last_token].strategy, self.players[last_token].name) # 返回值方便数据统计

def primer_AI_war():
    AI1 = player("AI1", "primer")
    AI2 = player("AI2", "primer")
    AI3 = player("AI3", "primer")
    return game([AI1, AI2, AI3]).start()

def Human_vs_primer_AI():
    human = player(strategy = "human")
    primer = player(strategy = "primer")
    game([human, primer]).start()

def primer_AI_vs_expert_AI_war():
    primer = player(strategy = "primer")
    expert = player(strategy = "expert")
    return game([primer, expert]).start()

def stat_primer_AI_war(count):
    stat = {"AI1": 0, "AI2": 0, "AI3": 0}
    while count:
        stat[primer_AI_war()[1]] += 1
        count -= 1
    print(stat)

def stat_primer_AI_vs_expert_AI_war(count):
    stat = {"expert": 0, "primer": 0}
    while count:
        stat[primer_AI_vs_expert_AI_war()[0]] += 1
        count -= 1
    print(stat)

if __name__ == "__main__":
    #primer_AI_war()
    #primer_AI_vs_expert_AI_war()
    #stat_primer_AI_war(1000)
    #stat_primer_AI_vs_expert_AI_war(1000)
    Human_vs_primer_AI()


