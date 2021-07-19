# coding=utf-8
from __future__ import unicode_literals
import requests
import json
from django.conf import settings
from rest_framework import exceptions

class WechatMessageSender(object):
    def __init__(self):
        self.wx_app_id = settings.WX_APP_ID
        self.wx_app_secret = settings.WX_APP_SECRET
        self.wx_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'
        self.wx_template_url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/uniform_send?access_token={}'
        self.wx_official_appid = settings.WX_OFFICIAL_APPID
        self.wx_template_id = settings.WX_TEMPLATE_ID

    def _request(self, method='get', **kwargs):
        url = self.wx_access_token_url.format(self.wx_app_id, self.wx_app_secret)
        try:
            response = requests.request(method=method, url=url, timeout=10)
            result = json.loads(response.text)
            access_token = result.get('access_token')
        except (requests.ConnectionError, requests.Timeout) as e:
            raise exceptions.ValidationError('网络错误，无法连接微信！')
        except Exception as e:
            raise exceptions.ValidationError('获取access_token错误')

        return self.wx_template_url.format(access_token)

    def _error_handle(self, errcode):
        """
        统一错误处理
        :param errcode:
        :type errcode:
        :return:
        :rtype:
        """
        pass

    def _send_wechat_template_msg(self, data):
        """
        统一发送模板消息
        :param data:
        :type data:
        :return:
        :rtype:
        """
        url = self._request()
        headers = {'Content-Type': 'application/json'}
        try:
            result = requests.post(url=url, headers=headers, data=json.dumps(data), timeout=2)
            result_data = json.loads(result.text)
            return result_data
        except (requests.ConnectionError, requests.Timeout) as e:
            raise exceptions.ValidationError('网络错误，无法连接微信！')
        except Exception as e:
            raise exceptions.ValidationError('微信消息发送失败')

    def get_openid(self, user):
        raise NotImplementedError("get_openid 此方法必须实现")


    def send_test_msg(self, user, data):
        """
        测试消息
        :param user:
        :type user:
        :param data:
        :type data:
        :return:
        :rtype:
        """
        data = {
            "touser": self.get_openid(user),
            "mp_template_msg": {
                "appid": self.wx_official_appid,
                "template_id": self.wx_template_id,
                "data": {
                    "first": {
                        "value": "测试消息",
                    },
                    "keyword2": {
                        "value": data
                    },
                }
            }
        }
        self._send_wechat_template_msg(data)