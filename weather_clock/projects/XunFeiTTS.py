#!/usr/bin/python3
# -*- coding:utf-8 -*-

import hashlib
import base64
import time
import json
import requests
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()],
    format='%(levelname)s:%(asctime)s:%(message)s'
)

class XunFeiTTS:
    def __init__(self) -> None:
        self.app_id = "5c5ff407" # 讯飞的应用id
        self.app_key = "544c08f8193d0a4473c88d18d4c289ce" # 讯飞的token
        self.tts_url = "http://api.xfyun.cn/v1/service/v1/tts"

    def __gen_sig(self, req_params_base64, time_now):
        """
        授权认证，生成认证信息
        :param req_params_base64: 请求参数的base64串
        :param time_now: 当前时间
        :return:
        """
        s = self.app_key + time_now + req_params_base64
        hl = hashlib.md5()
        hl.update(s.encode(encoding='utf8'))
        return hl.hexdigest()

    def __gen_req_header(self, time_now, req_params_base64, sig):
        """
        生成请求头
        :param time_now: 当前时间
        :param req_params_base64: 请求参数的base64串
        :param sig:
        :return:
        """
        header = {
            "X-Appid": self.app_id,
            "X-CurTime": time_now,
            "X-Param": req_params_base64,
            "X-CheckSum": sig,
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
        }
        return header

    def fetch_voice(self, text):
        """
        根据传入text生成语音
        :param text: 
        :return: 
        """
        req_params = {
            "auf": "audio/L16;rate=16000",
            "aue": "raw", # 返回的语音格式 raw为wav格式语音, lame为MP3格式语音
            "voice_name": "xiaoyan",
            "speed": "50",
            "volume": "50",
            "pitch": "50",
            "engine_type": "intp65",
            "text_type": "text",
            "text": text + " 噻"
        }

        time_now = str(time.time()).split('.')[0]
        req_params_json = json.dumps(req_params)
        req_params_base64 = str(base64.b64encode(req_params_json.encode('ascii')).decode('ascii'))
        header = self.__gen_req_header(time_now, req_params_base64, self.__gen_sig(req_params_base64, time_now))

        resp = requests.post(url=self.tts_url, data=req_params, headers=header)
        content_type = resp.headers['Content-type']

        # 请求成功时， contentType为audio.mpeg, 失败时，contentType为text/plain, 返回异常信息
        if content_type == 'audio/mpeg':
            # 将语音写入文件voice.wav
            f = open('voice.wav', 'wb')
            f.write(resp.content)
            f.close()

            logging.info("[XunFeiTTS.fetch_voice] - Fetch Voice Success! Save As %s" % f.name)
        else:
            resp_json = resp.content.decode('utf-8')
            logging.info("[XunFeiTTs.fetch_voice] - %s" % resp_json)
            resp_dict = json.loads(resp_json)
            logging.error("[XunFeiTTS.fetch_voice] - ErrCode = %s, Desc = %s" % (resp_dict['code'], resp_dict['desc']))