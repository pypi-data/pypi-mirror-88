# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import requests
import traceback
import os

from .config import *


class Authorize(object):
    """优矿
    """
    def __init__(self, username='', password='', token='', account_file='', session=None):
        self.__username = username
        self.__password = password
        self.__token = token
        self.__account_file = account_file
        self.session = session


    def _authorize(self):
        """账户验证
        """
        username, password, token, account_file = self.__username, self.__password, \
                                                  self.__token, self.__account_file
        if username and password:
            self._isvalid, token = self.__authorize_user(username, password)
            cookies = {'cloud-sso-token': token}
            if not self._isvalid:
                print ('抱歉，您的用户名{}验证失败，可能是用户名不存在或者密码不正确'.format(username))
            else:
                token = self.__get_permanent_token_and_set_to_cookie(cookies=cookies)
                print ('''验证成功，您的 token为{}，您使用的登录方法已废弃，为保障您的账户稳定性，推荐使用uqer.Client(token='')方法进行账号验证'''.format(token))

        elif token:
            self._isvalid = self.__is_token_valid(token)
            if not self._isvalid:
                print ('抱歉，您的 token 验证失败：{}'.format(token))
            else:
                token = self.__get_permanent_token_and_set_to_cookie(token=token)
                username = os.environ.get('DatayesPrincipalName', 'unknow')
                print ('{} 账号登录成功'.format(username))

        elif account_file:
            username, password = file(account_file, 'r').readline().strip().split(',')
            self.isvalid, token = self.__authorize_user(username, password)
            cookies = {'cloud-sso-token': token}
            if not self.isvalid:
                print ('抱歉，您的账户文件验证失败：{}'.format(account_file))
            else:
                token = self.__get_permanent_token_and_set_to_cookie(cookies=cookies)
                print ('''验证成功，您的 token为{}，您使用的登录方法已废弃，为保障您的账户稳定性，推荐使用uqer.Client(token='')方法进行账号验证'''.format(token))



    def __get_permanent_token_and_set_to_cookie(self, token='', cookies={}):
        if not token:
            ret_json = requests.post(TOKEN_URL, data={'grant_type':'permanent'}, cookies=cookies).json()
            token = ret_json.get('access_token')

        self.__set_token_to_cookie(token)

        return token


    def __set_token_to_cookie(self, token):

        os.environ['access_token'] = token

        cookie_dict = {'cloud-sso-token': token}
        self.session.cookies = requests.utils.cookiejar_from_dict(cookie_dict)
        return token


    def __authorize_user(self, user, pwd):

        ### 2 user type
        data_type = dict(username=user, password=pwd, app='mercury_sdk')

        def user_type(data=None):
            res = self.session.post(AUTHORIZE_URL, data)

            if not res.ok or not res.json().get('content', {}).get('accountId', 0):
                return False, None
            else:
                result = res.json()
                token = result.get('content', {}).get('token', {}).get('tokenString', '')
                principal_name = result.get('content', {}).get('principalName', '')
                os.environ['DatayesPrincipalName'] = principal_name
                return True, token

        valid, token = user_type(data_type)

        if not valid:
            return False, None
        else:
            os.environ['cloud_sso_token'] = token
            return True, token


    def __is_token_valid(self, token):
        """检验 token 是否有效
        """
        try:
            r = self.session.get(MERCURY_URL, cookies={'cloud-sso-token': token})
            r_json = r.json()

            if type(r_json) == list:
                r = self.session.get(UQER_AUTH_URL, cookies={'cloud-sso-token': token})
                r_json = r.json()

                os.environ['DatayesPrincipalName'] = r_json['user']['principalName']
                
                return True
            elif type(r_json) == dict and r_json.get('code', 0) == -403:
                print ('token {} 无效或过期'.format(token))
                return False
            else:
                print ('token 验证异常: {}'.format(r.text))
                return False
        except:
            print ('token 验证异常')
            print ('-' * 80)
            traceback.print_exc()
            print ('-' * 80)
            return False









