class Notification:
    CLOUD_STATE = 'cloud_state'
    USER_LOGOUT = 'user_logout'
    DATAPOINT_UPDATE = 'datapoint_update'
    DEVICE_CONNECTION_STATE_CHANGED = 'device_connection_state_changed'
    DEVICE_CHANGE = 'device_change'
    EVENT_NOTIFY = 'event_notify'

    def __init__(self, data):
        self.data = data

    def get_notify_result(self):
        return self.data['notify_content']