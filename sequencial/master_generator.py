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
        self.__buf_q.append(buf)

    def onFinish(self):
        with open(self.__file_path, "w") as f:
            for buf in self.__buf_q:
                f.write(buf.join('\n'))


def main():
    prologue = "insert new master file data\n"
    prologue += "record type\n"
    prologue += "\tname address phone number sex\n"
    prologue += "ps. id is auto generate"

    loop = MasterMakerLooper(prologue)
    loop(logging = True)

if __name__ == "__main__":
    main()