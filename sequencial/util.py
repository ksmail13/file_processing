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
    입력을 받으며 계속 루프를 도는 functor
    """

    def __init__(self, prologue = "main loop", prompt = ">"):
        self.prologue = prologue
        self.prompt = prompt

    def __call__(self, *args, **kwargs):
        """
        메인 루프의 시작
        """

        print self.prologue
        try:
            while True:
                str = raw_input(self.prompt)
                if kwargs.has_key("logging") and kwargs["logging"]:
                    print str

                self.onInput(str)
        except EOFError:
            pass
        except KeyboardInterrupt:
            pass
        finally:
            self.onFinish()

    def onInput(self, buf):
        """
        입력이 들어 왔을 때의 작업
        :param buf : 입력
        """
        raise NotImplementedError

    def onFinish(self):
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
        assert(item, int)
        return self.__data[item]

    def __setitem__(self, key, value):
        assert(key, int)
        self.__data[key] = value

    def __delitem__(self, key):
        assert(key, int)
        del self.__data[key]

    def __add__(self, other):
        self.append(other)


def merge(mem_q, file, new_file_name, merge_type):
    """
    메모리에 있는 레코드와 파일의 레코드를 합친다.
    새 파일을 만들어 저장하고 기존 파일은 삭제한다.
    :param mem_q: 메모리에 있는 레코드
    :param file: 레코드가 있는 파일
    :param merge_type: 트랜잭션에 대한 머지인지 마스터/ 트랜젝션에 대한 머지인지 판별
    :return:
    """
    assert(mem_q, list)
    os.rename(file.name, "temp.dat")
    mem_q.sort()
    record_type = None
    index = 0

    if merge_type == 'T':
        record_type = record.TransactionRecord
    else:
        record_type = record.Record

    with open(new_file_name, "w") as new_file:
        buf = file.readline()
        while True:
            f_record = record_type.generate(buf)
            if f_record >= mem_q[index]:
                new_file.write(mem_q[index])
                index += 1
            else:
                new_file.write(buf)
                buf = file.readline()