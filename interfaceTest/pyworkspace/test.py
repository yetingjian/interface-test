# coding=utf-8
import openpyxl
import os
import json


def Build():
    data = {}
    data['msg_type'] = msg_type
    data['msg_id'] = msg_id
    data['direction'] = direction
    data['content'] = content
    return (json.dumps(data) + '\r\n').encode()


if __name__ == '__main__':
    print Build()