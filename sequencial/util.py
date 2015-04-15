# coding:utf-8
"""
공통 모듈을 정의
"""
__author__ = 'micky'


class InputLooper(object):
    """
    입력을 받으며 계속 루프를 도는 functor
    """

    def __init__(self, prologue = "main loop", prompt = ">"):
        self.prologue = prologue
        self.prompt = prompt

    def __call__(self, *args, **kwargs):
        """
        메인 루프의 시작
        """

        print self.prologue
        try:
            while True:
                str = raw_input(self.prompt)
                if kwargs.has_key("logging") and kwargs["logging"]:
                    print str

                self.onInput(str)
        except EOFError:
            pass
        except KeyboardInterrupt:
            pass
        finally:
            self.onFinish()

    def onInput(self, buf):
        """
        입력이 들어 왔을 때의 작업
        :param buf : 입력
        """
        raise NotImplementedError

    def onFinish(self):
        """
        입력이 끝나고 EOF가 들어왔을 때의 작업
        """
        raise NotImplementedError
