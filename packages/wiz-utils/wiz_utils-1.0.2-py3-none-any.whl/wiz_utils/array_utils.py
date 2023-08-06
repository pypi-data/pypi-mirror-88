# coding=utf-8
class ArrayUtils(object):
    @staticmethod
    def is_empty(array: tuple or list) -> bool:
        return array is None or len(array) == 0

    @staticmethod
    def spilt(array: tuple or list, number_per_sublist: int = 1) -> list:
        if ArrayUtils.is_empty(array):
            return []
        return [array[i:i + number_per_sublist] for i in range(0, len(array), number_per_sublist)]
