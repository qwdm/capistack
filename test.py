import sys, os
import time
from multiprocessing import Process

sys.path.append('build/lib.linux-x86_64-2.7')
import stack


try:
    N_TESTS = int(sys.argv[1])
except IndexError:
    N_TESTS = 1000


def pushup(stackobj, numtests, maxheight):
    for i in xrange(numtests):
         for j in xrange(maxheight):
              stackobj.push(i)
         for j in xrange(maxheight):
              stackobj.pop()


def LEAK_TEST():

    def leak_test():
        s = stack.Stack()
        pushup(s, N_TESTS, 100)
            
    test = Process(target=leak_test, args=())
    test.start()

    print "Test Process PID: %s" % test.pid
    while test.is_alive():
            with open("/proc/%s/status" % test.pid) as f:
                    line = [line for line in f.readlines() 
                                 if "VmSize" in line][0]
                    print line
            time.sleep(1)
            
    print 'test ends'


def PERFOMANCE_TEST():
    def timeit(func):
        def _(*args, **kwargs):
            t0 = time.time()
            func(*args, **kwargs)
            return time.time() - t0
        return _


    numt = 10
    maxh = 10000000

    @timeit
    def pystack_test():
        s = type("PyStack", (list, ), {})()
        s.push = s.append
        pushup(s, numt, maxh)

    @timeit
    def mystack_test():
        s = stack.Stack()
        pushup(s, numt, maxh)

    print "pystack: %s" % pystack_test()
    print "mystack: %s" % mystack_test()


if __name__ == '__main__':
    PERFOMANCE_TEST()
