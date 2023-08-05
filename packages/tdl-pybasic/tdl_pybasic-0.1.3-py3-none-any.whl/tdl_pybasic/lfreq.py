#coding: utf-8
# 英字の頻度表

from collections import Counter
import matplotlib.pyplot as plt


freq_table = [
        ['a', 8.167], ['b', 1.492], ['c', 2.782], ['d', 4.253],
        ['e', 12.702], ['f', 2.228], ['g', 2.015], ['h', 6.094],
        ['i', 6.966], ['j', 0.153], ['k', 0.772], ['l', 4.025],
        ['m', 2.406], ['n', 6.749], ['o', 7.507], ['p', 1.929],
        ['q', 0.095], ['r', 5.987], ['s', 6.327], ['t', 9.056],
        ['u', 2.758], ['v', 0.978], ['w', 2.36], ['x', 0.15],
        ['y', 1.974], ['z', 0.074]]

def show_freq_graph(freq2=None):
    tmp_tf = freq_table[:]
    tmp_tf.sort(key=lambda x: x[1])
    tmp_tf.reverse()
    if freq2:
        freqd = dict(freq2)
        tfreq = [(k, freqd[k]) for k, f in tmp_tf]
        plt.bar([x*2.2 for x in range(len(tmp_tf))],
              [x[1] for x in tmp_tf], 1,
              tick_label=[x[0] for x in tmp_tf])
        plt.bar([x*2.2+1 for x in range(len(tfreq))],
              [x[1] for x in tfreq],
              tick_label=[x[0] for x in tfreq])

    else:
        plt.bar(range(len(tmp_tf)),
              [x[1] for x in tmp_tf],
              tick_label=[x[0] for x in tmp_tf])

def calc_freq_table(text):
    """
    文字(アルファベット大文字)の出現頻度を調べる関数
    """
    flist = list(Counter(text.replace(' ', '')).items())
    length = len(text)
    flist = [(x[0], x[1]/length*100) for x in flist]
    flist.sort(key=lambda x: x[1])
    flist.reverse()
    return flist
