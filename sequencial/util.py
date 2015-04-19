# coding:utf-8
"""
공통 모듈을 정의
"""
__author__ = 'micky'
import collections
import os
import record


class InputLooper(object):
    """
    입력을 받으며 계속 루프를 도는 function object
    """

    def __init__(self, prologue="main loop", prompt=">"):
        self.prologue = prologue
        self.prompt = prompt

    def __call__(self, *args, **kwargs):
        """
        메인 루프의 시작
        """

        print self.prologue
        try:
            while True:
                in_str = raw_input(self.prompt)
                if "logging" in kwargs and kwargs["logging"]:
                    print in_str

                self.on_input(in_str)
        except EOFError:
            pass
        except KeyboardInterrupt:
            pass
        finally:
            self.on_finish()

    def on_input(self, buf):
        """
        입력이 들어 왔을 때의 작업
        :param buf : 입력
        """
        raise NotImplementedError

    def on_finish(self):
        """
        입력이 끝나고 EOF가 들어왔을 때의 작업
        """
        raise NotImplementedError


class MutableString(object):
    """
    길이를 바꿀 수 있는 스트링
    """

    def __init__(self, init):
        self.__data = []
        if isinstance(init, collections.Iterable):
            for d in init:
                self.__data.append(d)
        else:
            self.__data.append(init)

    def __repr__(self):
        return "".join(self.__data)

    def __str__(self):
        return self.__repr__()

    def append(self, data):
        if isinstance(data, collections.Iterable):
            for d in data:
                self.__data.append(d)
        else:
            self.__data.append(data)

    def __getitem__(self, item):
        assert type(item) == int
        return self.__data[item]

    def __setitem__(self, key, value):
        assert type(key) == int
        self.__data[key] = value

    def __delitem__(self, key):
        assert type(key) == int
        del self.__data[key]

    def __add__(self, other):
        self.append(other)


def record_merge(f, r1, r2):
    """
    레코드를 비교해 더 빠른 순서의 레코드를 파일에 저장한다.
    :param f: 저장할 파일
    :param r1: 비교할 레코드1
    :param r2: 비교할 레코드2
    :return: 저장된 레코드
    """

    if isinstance(r1, record.Record) and isinstance(r2, record.Record):
        min_r = min(r1, r2)
        print >> f, min_r
        return min_r
    else:
        raise TypeError("r1, r2 must Record instance")
