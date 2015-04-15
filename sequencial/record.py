# coding:utf-8
# 이 응용에서의 레코드는
# id, 이름, 주소, 전화번호, 성별로 이루어져 있다.

__author__ = 'micky'

class Record(object):

    class __RecordIndex(object):
        ID = 0
        NAME = 1
        ADDR = 2
        PHONE_NUM = -2
        SEX = -1

    @staticmethod
    def generate(buf):
        """
        문자열을 레코드로 변환한다.
        :param buf: 레코드의 데이터가 있는 문자열
        :return: 레코드
        """
        buf = buf.split(' ')
        return Record(buf[Record.__RecordIndex.ID]
                      , buf[Record.__RecordIndex.NAME]
                      , "".join((n+" " for n in buf[Record.__RecordIndex.NAME+1:Record.__RecordIndex.PHONE_NUM]))
                      , buf[Record.__RecordIndex.PHONE_NUM]
                      , buf[Record.__RecordIndex.SEX])

    def __init__(self, id, name, addr, phone_num, sex):

        self.id = id
        self.name = name
        self.addr = addr
        self.phone_num = phone_num
        self.sex = sex

    def __str__(self):
        return "%s %s %s %s %s" % (self.id, self.name, self.addr, self.phone_num, self.sex)

    def __ge__(self, other):
        if isinstance(other, Record):
            return self.id >= other.id
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, Record):
            return self.id > other.id
        else:
            return False

    def __le__(self, other):
        if isinstance(other, Record):
            return self.id <= other.id
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Record):
            return self.id < other.id
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Record):
            return self.id != other.id
        else:
            return False


class TransactionRecord(Record):
    """
    트랜젝션 작업이 들어가는 레코드
    """

    @staticmethod
    def generate(buf):
        """
        생성
        :param buf:
        :return:
        """
        buf = buf.split(' ')
        new_record = TransactionRecord(buf[1+Record.__RecordIndex.ID]
                      , buf[1+Record.__RecordIndex.NAME]
                      , "".join((n+" " for n in buf[1+Record.__RecordIndex.ADDR:Record.__RecordIndex.PHONE_NUM]))
                      , buf[Record.__RecordIndex.PHONE_NUM]
                      , buf[Record.__RecordIndex.SEX])
        new_record.operation = buf[0]

        return new_record

    def __str__(self):
        return self.operation+" "+super(TransactionRecord, self).__str__()