# coding:utf-8
# 이 응용에서의 레코드는
# id, 이름, 주소, 전화번호, 성별로 이루어져 있다.

__author__ = 'micky'


class Record(object):
    class RecordIndex(object):
        ID = 0
        NAME = 1
        ADDRESS = 2
        PHONE_NUM = -2
        SEX = -1

    @staticmethod
    def generate(buf, r_id=-1):
        """
        문자열을 레코드로 변환한다.
        :param buf: 레코드의 데이터가 있는 문자열
        :return: 레코드
        """
        if len(buf.strip()) == 0:
            return None
        buf = [attr.strip() for attr in buf.split(' ')]

        if r_id == -1:
            return Record(int(buf[Record.RecordIndex.ID])
                          , buf[Record.RecordIndex.NAME]
                          , "".join((n + " " for n in buf[Record.RecordIndex.ADDRESS:Record.RecordIndex.PHONE_NUM]))
                          , buf[Record.RecordIndex.PHONE_NUM]
                          , buf[Record.RecordIndex.SEX].strip())
        else:
            return Record(r_id
                          , buf[Record.RecordIndex.NAME-1]
                          , "".join((n + " " for n in buf[Record.RecordIndex.ADDRESS-1:Record.RecordIndex.PHONE_NUM]))
                          , buf[Record.RecordIndex.PHONE_NUM]
                          , buf[Record.RecordIndex.SEX].strip())

    def __init__(self, r_id, name, address, phone_num, sex):

        self.id = r_id
        self.name = name
        self.address = address
        self.phone_num = phone_num
        self.sex = sex

    def __str__(self):
        return "%s %s %s %s %s" % (self.id, self.name, self.address, self.phone_num, self.sex)

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
            print self.id, other.id, self.id == other.id
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
        if len(buf.strip()) == 0:
            return None
        buf = [attr.strip() for attr in buf.split(' ')]
        new_record = TransactionRecord(int(buf[1 + TransactionRecord.RecordIndex.ID])
                                       , buf[1 + TransactionRecord.RecordIndex.NAME]
                                       , "".join((n + " " for n in buf[
                                                                   1 + TransactionRecord.RecordIndex.ADDRESS:TransactionRecord.RecordIndex.PHONE_NUM]))
                                       , buf[TransactionRecord.RecordIndex.PHONE_NUM]
                                       , buf[TransactionRecord.RecordIndex.SEX].strip())
        new_record.operation = buf[0]

        return new_record

    def record_str(self):
        return super(TransactionRecord, self).__str__()

    def __str__(self):
        return self.operation + " " + super(TransactionRecord, self).__str__()