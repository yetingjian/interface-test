global false, true
false = False
true = True

from xlinkutils import Xlink_Utils


class DataPoint:
    def __init__(self, index, types, value):
        self.index = index
        self.type = types
        self.value = value
        self.length = {
            Xlink_Utils.ValueType.BOOL: 1,
            Xlink_Utils.ValueType.INT_16: 2,
            Xlink_Utils.ValueType.UNSIGNED_INT_16: 2,
            Xlink_Utils.ValueType.INT_32: 4,
            Xlink_Utils.ValueType.UNSIGNED_INT_32: 4,
            Xlink_Utils.ValueType.INT_64: 8,
            Xlink_Utils.ValueType.UNSIGNED_INT_64: 8,
            Xlink_Utils.ValueType.FLOAT: 4,
            Xlink_Utils.ValueType.DOUBLE: 8,
            Xlink_Utils.ValueType.STRING: len(self.value) if type(self.value) == str else 0,
            Xlink_Utils.ValueType.BYTES: len(self.value) if type(self.value) == list else 0,
        }.get(self.type, 0)

    def __setitem__(self, key, value):
        pass

    def __eq__(self, other):
        """比较两个DataPoint是否相等，只比较index，value的值"""
        return self.index == other.index and self.value == other.value

    def __str__(self):
        """字符串类型输出DataPoint对象"""
        return '{"index":' + str(self.index) + ',"type":' + str(self.type) + ',"value":' + str(self.value) + '}'

    def __repr__(self):
        """自定义输出格式，字典类型输出DataPoint对象"""
        return '{"index":' + str(self.index) + ',"type":' + str(self.type) + ',"value":' + str(self.value) + '}'



