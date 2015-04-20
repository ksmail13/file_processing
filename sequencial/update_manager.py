# coding:utf-8
import util
from record import Record, TransactionRecord, record_reader
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

delete_err_msg = lambda x: "Delete fail : id[{}] is not exist".format(x.id)
update_err_msg = lambda x: "Update fail : id[{}] is not exist".format(x.id)
add_err_msg = lambda x: "Add fail : id[{}] is exist".format(x.id)


class MasterUpdate(object):

    def __init__(self, master_path, transaction_path, backup=True):
        self.master_path = master_path
        self.transaction_path = transaction_path
        self.is_backup = backup

        self.new_file = open("temp.dat", "w")
        self.error_file = open("error.dat", "w")
        self.is_closed = False
        # 마지막에 적용된 아이디
        self.last_id = -1

    def merge(self):
        master_gen = record_reader(Record, self.master_path)
        transaction_gen = record_reader(TransactionRecord, self.transaction_path)

        m_r = master_gen.next()
        t_r = transaction_gen.next()

        while True:
            operator = self.get_transaction_operator(t_r.operation)

            if operator(m_r, t_r) >= 0:
                try:
                    t_r = transaction_gen.next()
                except StopIteration:
                    for other_r in master_gen:
                        print >> self.new_file, other_r
                    break
            else:
                try:
                    m_r = master_gen.next()
                except StopIteration:
                    if t_r.operation == 'A':
                        print >> self.new_file, t_r.record_str()
                    for other_r in transaction_gen:
                        if other_r.operation == 'A':
                            print >> self.new_file, other_r.record_str()
                        else:
                            error_msg = (update_err_msg if other_r.operation == 'U' else delete_err_msg)
                            print >> self.error_file, error_msg(other_r)
                    break

        if self.is_backup:
            temp = os.path.splitext(self.master_path)
            old_master_name = temp[0]+"_"+datetime.now().strftime("%y%m%d%H%M%S")+temp[1]
            os.rename(self.master_path, old_master_name)
            os.rename("temp.dat", self.master_path)

        self.close()

    def close(self):
        self.new_file.close()
        self.error_file.close()
        self.is_closed = True

    def __del__(self):
        if self.is_closed is False:
            self.close()

    def get_transaction_operator(self, operator):
        """
        각 연산자 함수를 리턴한다.
        :param operator:
        :return:
        """
        return self.add if operator == 'A' else self.update if operator == 'U' else self.delete

    def add(self, m_r, t_r):
        """
        transaction의 add연산을 수행한다.
        :param m_r:
        :param t_r:
        :return: -1 : 마스터가 트랜젝션 레코드보다 작다(마스터를 읽는다)
                  0 : 이상 없음(트랜잭션을 읽는다)
                  1 : 중복되는 레코드가 있다.(트랜젝션을 읽는다)
        """
        if m_r < t_r:
            # 마스터가 트랜젝션보다 작으면 마스터를 파일에 입력한다.
            if m_r.id != self.last_id:
                print >> self.new_file, m_r
                self.last_id = m_r.id
            return -1
        elif m_r == t_r:
            # 마스터가 트랜젝션과 같으면 에러 메시지를 출력하고 종료한다.
            print >> self.error_file, add_err_msg(t_r)
            return 1
        else:
            # 마스터가 트랜젝션 보다 크면 트랜젝션을 파일에 입력한다.
            print >> self.new_file, t_r.record_str()
            self.last_id = t_r.id
            return 0

    def update(self, m_r, t_r):
        """
        transaction의 update연산을 수행한다.
        :param m_r:
        :param t_r:
        :return: -1 : 마스터가 트랜젝션 레코드보다 작다(마스터를 읽는다)
                  0 : 이상 없음(트랜잭션을 읽는다)
                  1 : 중복되는 레코드가 있다.(트랜젝션을 읽는다)
        """
        if m_r < t_r:
            # 마스터가 트랜젝션보다 작으면 마스터를 파일에 입력한다.
            print >> self.new_file, m_r
            self.last_id = m_r.id
            return -1
        elif m_r == t_r:
            # 마스터가 트랜젝션과 같으면 트랜젝션을 파일에 입력한다.
            print >> self.new_file, t_r.record_str()
            self.last_id = t_r.id
            return 0
        else:
            # 마스터가 트랜젝션보다 크면 에러메시지를 출력한다.(업데이트할 데이터가 없다)
            print >> self.error_file, update_err_msg(t_r)
            return 1

    def delete(self,  m_r, t_r):
        """
        transaction의 update연산을 수행한다.
        :param m_r:
        :param t_r:
        :return: -1 : 마스터가 트랜젝션 레코드보다 작다(마스터를 읽는다)
                  0 : 이상 없음(트랜잭션을 읽는다)
                  1 : 중복되는 레코드가 있다.(트랜젝션을 읽는다)
        """
        if m_r < t_r:
            # 마스터가 트랜젝션보다 작으면 마스터를 파일에 입력한다.
            print >> self.new_file, m_r
            self.last_id = m_r.id
            return -1
        elif m_r == t_r:
            # 마스터가 트랜젝션과 같으면 아무일도 하지 않는다.
            return 0
        else:
            # 마스터가 트랜젝션보다 크면 에러메시지를 출력한다.(삭제할 데이터가 없다)
            print >> self.error_file, delete_err_msg(t_r)
            return 1


def main():
    param = optparse.OptionParser()

    param.add_option("-n", "--NoBackup",
                     action="store_false", dest="backup",
                     help="Do not create backup file")
    param.set_default("backup", True)
    (options, args) = param.parse_args()

    # master_update("master.dat", "transact.dat", options.backup)
    updater = MasterUpdate("master.dat", "transact.dat", options.backup)
    updater.merge()

if __name__ == "__main__":
    main()
