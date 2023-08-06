#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/12/01 12:43
# @Blog    : https://blog.zbmain.com

from zbmain.utils import config
from zbmain.utils import robot
import json
import random
import requests
import time


class UnitRobot(object):
    def __init__(self,
                 app_id,
                 secret_key,
                 unit_url='https://aip.baidubce.com/oauth/2.0/token',
                 robot_url='https://aip.baidubce.com/rpc/2.0/unit/service/chat',
                 chat_reply='不好意思，我正在学习中，随后回复你。', timeout: float = 0.6):
        '''官方api'''
        grant_type = 'client_credentials'
        self.unit_url = unit_url + f'?grant_type={grant_type}&client_id={app_id}&client_secret={secret_key}'
        self.robot_url = robot_url
        self.chat_reply = chat_reply
        self.timeout = timeout

    def __call__(self, chat_input, robot_id='S40811', user_id='88888'):
        '''
        调用百度UNIT接口，回复聊天内容
        :param chat_input: 输入上文
        :param user_id: 用户id（日志记录）
        :return:
        输出下文（答复）
        '''
        res = requests.get(self.unit_url)
        print(res)
        access_token = eval(res.text)["access_token"]
        self.robot_url = self.robot_url + '?access_token=' + str(access_token)
        post_data = {
            "log_id": str(random.random()),
            "request": {
                "query": chat_input,
                "user_id": user_id
            },
            "session_id": "",
            "service_id": robot_id,
            "version": "2.0"
        }
        res = requests.post(url=self.robot_url, json=post_data)
        time.sleep(self.timeout)  # 不支持并发，防止报错，暂时强制等待
        unit_chat_obj = json.loads(res.content)
        if unit_chat_obj["error_code"] != 0: return self.chat_reply

        unit_chat_obj_result = unit_chat_obj["result"]
        unit_chat_response_list = unit_chat_obj_result["response_list"]
        unit_chat_response_obj = random.choice(
            [unit_chat_response for unit_chat_response in unit_chat_response_list if
             unit_chat_response["schema"]["intent_confidence"] > 0.0])
        unit_chat_response_action_list = unit_chat_response_obj["action_list"]
        unit_chat_response_action_obj = random.choice(unit_chat_response_action_list)
        unit_chat_response_say = unit_chat_response_action_obj["say"]
        return unit_chat_response_say


single_unit = None
config_data = None


def unit_chat(text: str, userId='88888', timeout=0.6):
    '''
    unit_chat 快速接口
    不支持0.5s内api并发，此处使用单例模式。如果追求效率，且不会0.5s并发接口，手动timeout=0
    '''
    global single_unit
    global config_data
    if not config_data:
        config_data = config._getRobotConfigFromJson()
    _, ak, sk, ri = config_data
    # print(_, ak, sk, ri)
    if not single_unit:  # 单例模式：免费版这种接口写法不支持异步并发 （待以后写个机器人池再换）
        single_unit = robot.UnitRobot(ak, sk, timeout=timeout)  #

    return single_unit(text, ri, userId)


if __name__ == '__main__':
    print(unit_chat('你'))
    print(unit_chat('我是谁？'))
    print(unit_chat('你好吗'))
