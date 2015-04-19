# coding:utf-8
import util
from record import Record, TransactionRecord
import sys
import optparse
import os

if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf-8')
else:
    # print >> sys.stderr, "sys hasn't setdefaultencoding"
    pass

__author__ = 'micky'


def master_update(master_path, transaction_path, option):
    def add_operation(master_file, error_file, m_record, t_record, new_file):
        """
        transaction의 add연산
        :param new_file: 새로운 마스터파일
        :param master_file: 기존 마스터 파일
        :param error_file: 에러를 저장할 파일
        :param m_record: 마스터 파일의 레코드
        :param t_record: 트랜젝션 파일의 레코드
        :return: 새로운 마스터 파일 레코드
        """
        while m_record < t_record:
            print >> new_file, m_record
            m_record = Record.generate(master_file.readline())

        if m_record == t_record:
            print >> error_file, "Add fail: exist id {}".format(t_record.id)
        else:
            print >> new_file, t_record.record_str()

        return m_record

    def del_operation(master_file, error_file, m_record, t_record):
        """
        delete 연산
        :param master_file: 기존 마스터 파일
        :param error_file: 에러 파일
        :param m_record: 마스터 레코드
        :param t_record: 트랜젝션 레코드
        :return:
        """
        while m_record < t_record:
            m_record = Record.generate(master_file.readline())

        if m_record == t_record:
            m_record = Record.generate(master_file.readline())
        else:
            print >> error_file, "Delete fail: id{} not exist ".format(t_record.id)

        return m_record

    def up_operation(master_file, error_file, m_record, t_record, new_file):
        while m_record < t_record:
            print >> new_file, m_record
            m_record = Record.generate(master_file.readline())

        if m_record == t_record:
            print >> new_file, t_record.record_str()
        else:
            print >> error_file, "Update fail: id {} is not exist ".format(t_record.id)

        return m_record

    operations = {
        'A':add_operation,
        'U':up_operation,
        'D':del_operation
    }

    def merge(master, transaction,
          old_master_name, new_master_name="master.dat"):
        """
        기존 마스터파일과 기존 트랜젝션파일을 합친다.
        :param master: 마스터 파일
        :param transaction: 트랜젝션 파일
        :return:
        """
        with open("temp.dat", "w"), open("error.dat", "w") as (new_file, error_file):
            # 임시 마스터 파일 생성
            master_line = master.readline()
            transaction_line = transaction.readline()

            while True:
                # m_record : 마스터 파일의 레코드
                # t_record : 트랜젝션 파일의 레코드
                m_record = Record.generate(master_line)
                t_record = TransactionRecord.generate(transaction_line)

                m_record = operations[t_record.operation](master, error_file, m_record, t_record)
                t_record = TransactionRecord.generate(transaction.readline())

    with (open(master_path, "r"), open(transaction_path, "r")) as (master, transaction):
        merge(master, transaction)


def main():
    param = optparse.OptionParser()

    param.add_option("-n", "--NoBackup",
                     action="store_false", dest="backup",
                     help="Do not create backup file")
    param.set_default(backup=True)
    (options, args) = param.parse_args()
    print options, args

    # print "merge master and transaction file"

    # loop = TransactionLooper(prologue, "?")

    # loop(logging=True)


if __name__ == "__main__":
    main()
