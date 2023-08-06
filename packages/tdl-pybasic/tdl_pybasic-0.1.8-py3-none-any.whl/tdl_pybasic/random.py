#coding: utf-8
# 乱数関連のモジュール

from random import randint, seed, random

def initialize():
    """
    seed()を使って乱数を初期化
    常に同じ答えが返ってくるように
    """
    seed(20)


def throw_coin():
    """
    サイコロを振る。0なら表，1なら裏
    """
    return randint(0, 1)