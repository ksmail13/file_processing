# coding:utf-8
__author__ = 'micky'
import util


class MasterMakerLooper(util.InputLooper):

    def __init__(self, prologue="main loop", prompt=">", file_path="master.dat"):
        """
        initial object
        :type file_path: str
        """
        super(MasterMakerLooper, self).__init__(prologue, prompt)
        self.__file_path = file_path
        self.__buf_q = []
        self.__id = 0

    def onInput(self, buf):
        if len(buf.strip()) > 0:
            self.__buf_q.append(buf)

    def onFinish(self):
        self.__buf_q.sort()
        with open(self.__file_path, "a") as f:
            for buf in self.__buf_q:
                assert isinstance(buf, str)
                print >> f, buf
            f.flush()


def main():
    prologue = "insert new master file data\n"
    prologue += "record type\n"
    prologue += "\tname address phone number sex\n"
    prologue += "ps. id is auto generate"

    loop = MasterMakerLooper(prologue)
    loop(logging=True)

if __name__ == "__main__":
    main()