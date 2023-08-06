#coding: utf-8
# Pythonのリストを使った行列演算

from io import BytesIO
import io
import numpy as np
from imageio import imread
import scipy
from scipy.io import wavfile
from scipy import ndimage
import IPython
import requests
from PIL import Image


def array_add(the_list, d):
    """
    リストを受け取り，行列演算の加算を実行してリストを返す
    """
    the_arr = np.array(the_list)
    the_arr += d
    return the_arr.tolist()


def array_mul(the_list, d):
    """
    リストを受け取り，行列演算の乗算を実行してリストを返す
    """
    the_arr = np.array(the_list)
    the_arr = the_arr.astype(dtype="float64")*d
    return the_arr.tolist()


def load_sound():
    """
    音声ファイルを読み込み，リスト形式で返す
    """
    url = "http://ecee.colorado.edu/~mathys/ecen1200/hwcl09/c6.wav"
    res = requests.get(url)
    freq, snd_arr = wavfile.read(BytesIO(res.content))
    return freq, snd_arr.astype(dtype="float64").tolist()


def show_player(freq, the_list):
    """
    サンプリング周波数と音声のリストを受け取り，プレイヤーを表示する
    """

    return IPython.display.Audio(np.array(the_list), rate=freq)


def load_image(url="http://cdn.akc.org/A_Pembroke_Welsh_Corgi_Does_It_-_BODY2.jpg"):
    """
    画像を読み込み，リスト形式で返す
    """
    res = requests.get(url)
    img_arr = imread(BytesIO(res.content))
    return img_arr.astype(np.int16).tolist()


def show_image(img_list):
    """
    画像のリストを受け取り，表示する
    """
    img_arr = np.array(img_list, 'uint8')
    im = Image.fromarray(img_arr)
    buf = BytesIO()
    im.save(buf,"PNG")
    data = buf.getvalue()
    IPython.display.display(IPython.display.Image(data))


def convolve(img_list, list2):
    """
    画像とフィルタのlistを受け取り，convoludeを実行
    """
    img_arr = np.array(img_list, 'int16')
    f = np.array(list2)
    r = ndimage.convolve(img_arr, f)
    r[r > 255] = 255
    r[r < 0] = 0    

    return r.astype(np.int16).tolist()
    