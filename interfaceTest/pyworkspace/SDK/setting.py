#coding=utf8

import os


LogFileDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
LogFilePath = os.path.join(LogFileDir, 'AutomationTesting.log')


TestCasePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TestCase')


TestSetting = {
    'TestCase': 'SyncDevicesList',
    'Timeout': 60,  # Unit /second
    'Cycle': True,
    'CycleTimes': 0,    # Endless
    'CycleInterval': 0.2,   # Unit /second
    'FailedTimesLimit': 10,
    'Host': '',
    'Port': 12345,
}

TestSetting2 = [{
    'TestCaseList':
        {
            'StartSDK': True,
            'AuthUser': True,
            'SyncDevicesList': True,
            'SyncDeviceDatapoint': True,
            'SetDeviceDatapoint': False,
        },
    'Timeout': 60,  # Unit /second
    'Cycle': True,
    'CycleTimes': 0,    # Endless
    'CycleInterval': 0.2,   # Unit /second
    'FailedTimesLimit': 10,
    'Host': '',
    'Port': 12345,
},
]

