import time
import threading
import multiprocessing
from coveragePy.coverage_logger import CoverageLoggerThread


class RunnerProcess(multiprocessing.Process):
    daemon = True
    def __init__(self, idx, delay):
        self.idx = idx
        self.delay = delay
        super().__init__(name="Proc{}".format(idx))

    def run(self):
        time.sleep(self.delay)
        fname1 = "func{}".format(self.idx)


class RunnerThread(threading.Thread):

    def __init__(self, idx, delay):
        self.idx = idx
        self.delay = delay
        super().__init__(name="Proc{}".format(idx))

    def run(self):
        time.sleep(self.delay)
        import coveragePy.flash
        coveragePy.flash.app.run(host='0.0.0.0', port=8090)


def last_func():
    print("run this last")


class mainThread:

    def main(threads):
        thread_cov = CoverageLoggerThread()
        thread_cov.start()
        threads += [RunnerThread(*(0, 0.5))]
        for t in threads:
            t.start()
            print('@@@@@@@@@@@@@@@@@@' + t.name)

        for t in threads:
            t.join()

        last_func()

        thread_cov.shutdown()
        thread_cov.join()

# def main():
#     thread_cov = CoverageLoggerThread()
#     thread_cov.start()
#     threads = []
#     for args, cls in [((0, 0.5), RunnerThread), ((1, 2), RunnerProcess),
#                       ((2, 2), RunnerProcess), ((2, 4), RunnerProcess),
#                       ((3, 1), RunnerProcess), ((4, 1), RunnerProcess),
#                       ((5, 1), RunnerProcess), ((6, 1), RunnerProcess)]:
#         threads += [cls(*args)]
#         threads[-1].start()
#         print('@@@@@@@@@@@@@@@@@@' + threads[-1].name)
#
#     for t in threads:
#         t.join()
#
#     last_func()
#
#     thread_cov.shutdown()
#     thread_cov.join()


if __name__ == '__main__':
    threads = []
    # threads += [RunnerMainThread()]
    mainThread.main(threads)