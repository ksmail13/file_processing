# coding:utf-8
import util
import record
import sys

if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf-8')
else:
    print >> sys.stderr, "sys hasn't setdefaultencoding"

__author__ = 'micky'


class TransactionLooper(util.InputLooper):
    """
    트랜젝션 파일을 생성하기 위한 루프를
    """

    def __init__(self, prologue="main loop", prompt=">", file_path="transact.dat"):
        """
        initial object
        :param file_path: 파일을 저장할 경로
        :type file_path: str
        """
        super(TransactionLooper, self).__init__(prologue, prompt)
        self.__file_path = file_path
        self.__buf_q = []

    def onInput(self, buf):
        if len(buf.strip()) > 0:
            new_record = record.TransactionRecord.generate(buf)
            self.__buf_q.append(new_record)

    def onFinish(self):
        self.__buf_q.sort()
        with open(self.__file_path, "r") as f:
            merge(self.__buf_q, f, self.__file_path)


def merge(mem_q, file):
    """
    입력된 트랜젝션과 기존 트랜젝션파일을 합친다.
    :param mem_q: 입력된 레코드
    :param file: 트랜젝션 파일
    :return:
    """
    assert(mem_q, list)
    mem_q.sort()
    record_type = record.TransactionRecord
    index = 0

    with open("temp.dat", "w") as new_file:
        buf = file.readline()
        f_record = record_type.generate(buf)
        m_record = record_type.generate(mem_q[index])
        


def main():
    prologue = "insert transaction file data\n"
    prologue += "record type\n"
    prologue += "\ttransaction type(A, U, D) id name address phone number sex"

    loop = TransactionLooper(prologue, "?")

    loop(logging=True)


if __name__ == "__main__":
    main()
