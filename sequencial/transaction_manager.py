# coding:utf-8
import util
import record
import sys
import os

if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf-8')
else:
    # print >> sys.stderr, "sys hasn't setdefaultencoding"
    pass

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

    def on_input(self, buf):
        if len(buf.strip()) > 0:
            new_record = record.TransactionRecord.generate(buf)
            self.__buf_q.append(new_record)

    def on_finish(self):
        self.__buf_q.sort()
        try:
            with open(self.__file_path, "r") as f:
                merge(self.__buf_q, f)
        except IOError:
            with open(self.__file_path, "w") as f:
                for rec in self.__buf_q:
                    print >> f, rec


def merge(mem_q, origin_file):
    """
    입력된 트랜젝션과 기존 트랜젝션파일을 합친다.
    :param mem_q: 입력된 레코드
    :param origin_file: 트랜젝션 파일
    :return:
    """
    assert type(mem_q) == list
    record_type = record.TransactionRecord
    index = 0

    with open("temp.dat", "w") as new_file:
        buf = origin_file.readline()

        while True:
            f_record = record_type.generate(buf)
            m_record = mem_q[index]
            if util.record_merge(new_file, f_record, m_record) == f_record:
                # 기존파일의 레코드가 저장되면 파일을 다시 불러온다.
                try:
                    buf = origin_file.readline()
                    if origin_file.tell() == os.fstat(origin_file.fileno()).st_size:
                        raise EOFError
                except EOFError:
                    for i in xrange(index, len(mem_q)):
                        print >> new_file, mem_q[i]
                    break
            else:
                # 입력받은 레코드가 저장되면 레코드의 인덱스를 가르킨다.
                index += 1
                if len(mem_q) == index:
                    for line in origin_file:
                        print >> new_file, record_type.generate(line)
                    break

    name = origin_file.name
    os.unlink(name)
    os.rename("temp.dat", name)


def main():
    prologue = "insert transaction file data\n"
    prologue += "record type\n"
    prologue += "\ttransaction type(A, U, D) id name address phone number sex"

    loop = TransactionLooper(prologue, "?")

    loop(logging=True)


if __name__ == "__main__":
    main()
