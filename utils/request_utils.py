# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib.parse import urljoin

import requests
from rest_framework import exceptions, status


class BaseRequest(object):

    def __init__(self, host):
        self.host = host
        self.time_out = 5

    def _url(self, url):
        """
        动态url可以使用此方法拼接
        :param url:
        :type url:
        :return:
        :rtype:
        """
        return urljoin(self.host, url)


    def error_handle(self, data):
        """
        统一异常处理 一般针对于错误类型一致的可以统一处理
        :param data:
        :type data:
        :return:
        :rtype:
        """
        pass

    def _request(self, url, method, *args, **kwargs):
        raise NotImplementedError("_request 方法必须实现")


class SimpleSendRequest(BaseRequest):

    def _request(self, url, method, *args, **kwargs):
        try:
            response = requests.request(method=method, url=self._url(url), timeout=self.time_out, **kwargs)
        except (requests.ConnectionError, requests.Timeout) as e:
            raise exceptions.ValidationError('网络错误')
        except Exception as e:
            raise exceptions.ValidationError('未知错误')

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            raise exceptions.ValidationError('请求参数错误！')

        if response.status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            raise exceptions.ValidationError('其他错误')

        response_data = response.json()

        return response_data
