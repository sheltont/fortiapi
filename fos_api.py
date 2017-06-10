#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import json
from fgt import FGT
from fgt import AuthenticationError


ERROR = 'Error'
SUCCESS = 'Success'


def get_object(fgt, objpath, params, data):
    return fgt.get(objpath, params, data)


def create_object(fgt, objpath, params, data):
    return fgt.post(objpath, params, data)


def update_object(fgt, objpath, params, data):
    return fgt.put(objpath, params, data)


def delete_object(fgt, objpath, params, data):
    return fgt.delete(objpath, params, data)


def list_object(fgt, objpath, params, data):
    return fgt.get(objpath, params, data)

"""
Currently I only implement GET/CREATE/UPDATE/DELETE/LIST actions.
Acctually, MOVE/CLONE/APPEND are also supported in Fortinet API
"""
cmd_to_func = {
    'get': get_object,
    'create': create_object,
    'update': update_object,
    'delete': delete_object,
    'list': list_object
}


def is_valid_action(action):
    return action in cmd_to_func


def read_command_data():
    try:
        data = json.load(sys.stdin)
        return data
    except IndexError:
        return None


def parse_command_parameters(data):
    """
    Parse the command line parameters like "key1=value1&key2=value2&key3=value3
    """
    if not data:
        return {}
    pairs = data.split('&', 1)
    params = dict([pair.split('=', 1) for pair in pairs])
    return params


def response_auth_error():
    response_to_stdout(ERROR, 'FGT authentication error')


def response_bad_data():
    response_to_stdout(ERROR, 'Invalid json parameters from STDIN')


def response_bad_action():
    response_to_stdout(ERROR, 'Unsupported command action')


def response_other_errors(message):
    status = ERROR
    response_to_stdout(status, message)


def response_to_stdout(status=SUCCESS, message=None, data=None):
    res = {'status': status, 'message': message, 'data': data}
    json.dump(res, sys.stdout, sort_keys=False, indent=4)


def main():
    """
    解析命令行参数,并且从STDIN中读取一个JSON输入.在通过REST API完成调用后,将结果作为一个JSON写到STDOUT
    :return:
    """

    parser = argparse.ArgumentParser(description='FortiGate REST API command line wrapper')
    parser.add_argument('-U', dest='username', required=True, action='store', help='Fortigate username')
    parser.add_argument('-P', dest='password', required=True, action='store', help='the password of the user')
    parser.add_argument('-H', dest='host', required=True, action='store', help='Fortigate Host IP address')
    parser.add_argument('-X', dest='action', required=True, action='store', help='Action to be executed')
    parser.add_argument('-O', dest='object', required=True, action='store', help='Object to be manipulated')

    parser.add_argument('-p', dest='port', required=False, type=int,
                        action='store', default=443, help='Fortigate HTTPS listening port')
    parser.add_argument('-d', dest='vdom', required=False,
                        action='store', default='root', help='Fortigate VDOM')
    parser.add_argument('-a', dest='params', default='', action='store', help='Optional command parameters')

    parser.add_argument('-v', '--verbose', dest='verbose', required=False,
                        action='store_true', default=False,
                        help='Logging option')
    args = parser.parse_args()

    # 判断action参数是否在支持的范围中
    action = args.action.tolower()
    if not is_valid_action(action):
        response_bad_action()
        return 1

    # 从命令行中读取url参数
    params = parse_command_parameters(args.params)

    # 从stdin中读取命令的参数
    data = read_command_data()
    if not data:
        response_bad_data()
        return 1

    # 拼接一个https的url前缀并创建FGT对象. 端口默认是 443
    url_prefix = 'https://{0}:{1}'.format(args.host, args.port)
    fgt = FGT(url_prefix, args.vdom)

    try:
        # 使用指定的用户名&密码登录
        fgt.login(args.username, args.password)
        # 根据action调用对应的命令函数. vdom作为params输入
        result = cmd_to_func[action](fgt, args.object, params, data)
        # 将结果写到stdout中
        response_to_stdout(result)
        return 0
    except AuthenticationError:
        response_auth_error()
    except Exception as e:
        response_other_errors(repr(e))
    finally:
        if fgt:
            fgt.logout()


if __name__ == '__main__':
    main()
