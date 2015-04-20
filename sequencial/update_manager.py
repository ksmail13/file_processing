# coding:utf-8
import util
from record import Record, TransactionRecord
from datetime import datetime
import sys
import optparse
import os

if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf-8')
else:
    # print >> sys.stderr, "sys hasn't setdefaultencoding"
    pass

__author__ = 'micky'


def master_update(master_path, transaction_path, backup):
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
            print "write master in add", m_record
            print >> new_file, m_record
            buf = master_file.readline()
            if len(buf.strip()) > 0:
                m_record = Record.generate(buf)
            else:
                break

        print "add\nmaster : {}\ntran : {}".format(m_record, t_record)

        if m_record == t_record:
            print >> new_file, m_record
            m_record = Record.generate(master_file.readline())
            print >> error_file, "Add fail: exist id {}".format(t_record.id)
        else:
            print "Write master in add tran",t_record.record_str()
            print >> new_file, t_record.record_str()

        return m_record

    def del_operation(master_file, error_file, m_record, t_record, new_file):
        """
        delete 연산
        :param master_file: 기존 마스터 파일
        :param error_file: 에러 파일
        :param m_record: 마스터 레코드
        :param t_record: 트랜젝션 레코드
        :return:
        """
        while m_record < t_record:
            print >> new_file, m_record
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
            # m_record = Record.generate(master_file.readline())
            print >> new_file, t_record.record_str()
        else:
            print >> error_file, "Update fail: id {} is not exist ".format(t_record.id)

        return m_record

    operations = {
        'A': add_operation,
        'U': up_operation,
        'D': del_operation
    }

    def merge(old_master_name, new_master_name="master.dat"):
        """
        기존 마스터파일과 기존 트랜젝션파일을 합친다.
        :return:
        """
        with open("temp.dat", "w") as new_file:
            with open("error.dat", "w") as error_file:
                # 임시 마스터 파일 생성
                master_line = master.readline()
                transaction_line = transaction.readline()

                # m_record : 마스터 파일의 레코드
                # t_record : 트랜젝션 파일의 레코드
                m_record = Record.generate(master_line)
                t_record = TransactionRecord.generate(transaction_line)
                while True:

                    try:
                        m_record = operations[t_record.operation](master, error_file, m_record, t_record, new_file)
                        if master.tell() == os.fstat(master.fileno()).st_size:
                            raise EOFError
                    except EOFError:
                        for line in transaction:
                            t_record = TransactionRecord.generate(line)
                            if t_record.operation == 'A':
                                print >> new_file, t_record.record_str()
                            else:
                                print >> error_file, \
                                    "{} fail: id{} is not exist".format(
                                        "Update" if t_record.operation == 'U' else "Delete", t_record.id)
                        break

                    try:
                        t_record = TransactionRecord.generate(transaction.readline())
                        if transaction.tell() == os.fstat(transaction.fileno()).st_size:
                            raise EOFError
                    except EOFError:
                        for line in master:
                            print "write master", Record.generate(line)
                            print >> new_file, Record.generate(line)
                        break

                if backup:
                    temp = master.name
                    os.rename(temp, old_master_name)
                    os.rename("temp.dat", new_master_name)

    with open(master_path, "r") as master:
        with open(transaction_path, "r") as transaction:
            merge("master_{}.dat".format(datetime.now().strftime("%y%m%d%H%M%S")))


def main():
    param = optparse.OptionParser()

    param.add_option("-n", "--NoBackup",
                     action="store_false", dest="backup",
                     help="Do not create backup file")
    param.set_default("backup", True)
    (options, args) = param.parse_args()

    master_update("master.dat", "transact.dat", options.backup)


if __name__ == "__main__":
    main()
