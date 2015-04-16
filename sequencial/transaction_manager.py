# coding:utf-8
import util
import record

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
        with open(self.__file_path, "a") as f:
            for buf in self.__buf_q:
                # assert isinstance(buf, str)
                print >> f, buf
            f.flush()


def main():
    prologue = "insert transaction file data\n"
    prologue += "record type\n"
    prologue += "\ttransaction type(A, U, D) id name address phone number sex"

    loop = TransactionLooper(prologue, "?")

    loop(logging=True)


if __name__ == "__main__":
    main()
