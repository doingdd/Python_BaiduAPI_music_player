# coding: utf-8
import wave
import os
from pyaudio import PyAudio,paInt16
import pyaudio
from aip import AipSpeech
# import time
import numpy as np
import random

framerate=8000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2
chunk=2014
# 利用pyaudio录音
def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    print("开始缓存录音")
    monitor = False
    while not monitor:
        print 'begin '
        frames = []
        for i in range(0, 5):
            data = stream.read(NUM_SAMPLES)
            frames.append(data)
        audio_data = np.fromstring(data, dtype=np.short)
        # print type(data),data
        print audio_data

        large_sample_count = np.sum(audio_data > 800)
        temp = np.max(audio_data)
        # print time.clock()
        if temp > 800:
            print "检测到信号"
            print '当前阈值：', temp
            monitor = True
    else:
        print 'record now.'
        count=0
        while count<TIME*10:#控制录音时间
            string_audio_data = stream.read(NUM_SAMPLES)#一次性录音采样字节大小
            frames.append(string_audio_data)
            # print string_audio_data
            count+=1
            print('.')
        save_wave_file('01.wav',frames)
        stream.stop_stream()
        stream.close()
        pa.terminate()
# def record_cb_mode():
#     pa = PyAudio()
#     stream = pa.open(format=paInt16, channels=1,
#                      rate=framerate, input=True,
#                      # output = True,
#                      stream_callback=callback)
#     stream.start_stream()
#     while stream.is_active():
#         time.sleep(0.1)
#
#     stream.stop_stream()
#     stream.close()
#     pa.terminate()
def callback(in_data, frame_count, time_info, status):
    # data = wf.readframes(frame_count)
    return (in_data, pyaudio.paContinue)
def play(file):
    wf=wave.open(file,'rb')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
                  wf.getnchannels(),rate=wf.getframerate(),output=True)
    while True:
        data=wf.readframes(chunk)
        if data=="":break
        stream.write(data)
    stream.close()
    p.terminate()

def baidu_speech():
    #// 成功返回
     #{
     #    "err_no": 0,
     #    "err_msg": "success.",
    #     "corpus_no": "15984125203285346378",
    #     "sn": "481D633F-73BA-726F-49EF-8659ACCC2F3D",
    #     "result": ["北京天气"]
    # }
    # // 失败返回
    # {
    #     "err_no": 2000,
    #     "err_msg": "data empty.",
    #     "sn": null
    # }
    # 你的 APPID AK SK
    APP_ID = '10639428'
    API_KEY = '6u8eL2q96PntqBX4cuwgb684'
    SECRET_KEY = 'ane4qq7jOokBfCQ2WzypHh8ZIVs5Pjqm'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    # 识别本地文件
    re = client.asr(get_file_content('01.wav'), 'wav', 8000, {'lan': 'zh',})
    # print re.get('err_no')
    # print re.get('result','Err')[0].encode('utf-8')
    return re.get('result','Err')[0].encode('utf-8')
    # 从URL获取文件识别
    # client.asr('', 'wav', 8000, {
    #     'url': 'http://121.40.195.233/res/16k_test.pcm',
    #     'callback': 'http://xxx.com/receive',
    # })

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

if __name__ == '__main__':
    get_your_word = False
    while not get_your_word:
        my_record()
        print('Over!')
        # play(r'01.wav')
        speech_word = baidu_speech()
        print speech_word
        if '老铁老铁' in speech_word and '音乐' in speech_word:
            music = os.listdir('F:\KuGou')
            random.shuffle(music)
            for i in music:
                if i.endswith('.wav'):
                    play("F:\KuGou\{}".format(i))
        else:
            print "Don't know what you're talking!"
