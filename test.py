import sys, os
import time
from multiprocessing import Process

sys.path.append('build/lib.linux-x86_64-2.7')
import stack


try:
    N_TESTS = int(sys.argv[1])
except IndexError:
    N_TESTS = 1000

try: 
    MAX_HEIGHT = int(sys.argv[2])
except IndexError:
    MAX_HEIGHT = 1000



def pushup(stackobj, numtests, maxheight):
    for i in xrange(numtests):
         for j in xrange(maxheight):
              stackobj.push(i)
         for j in xrange(maxheight):
              stackobj.pop()


def LEAK_TEST():

    def leak_test():
        s = stack.Stack()
        pushup(s, N_TESTS, MAX_HEIGHT)
            
    test = Process(target=leak_test, args=())
    test.start()

    print "Test Process PID: %s" % test.pid
    while test.is_alive():
            with open("/proc/%s/status" % test.pid) as f:
                    line = [line for line in f.readlines() 
                                 if "VmSize" in line][0]
                    print line.rstrip()
            time.sleep(1)
            
    print "Leakage test ends....\n"


def PERFOMANCE_TEST():
    def timeit(func):
        def _(*args, **kwargs):
            t0 = time.time()
            func(*args, **kwargs)
            return time.time() - t0
        return _


    numt = N_TESTS
    maxh = MAX_HEIGHT

    @timeit
    def pystack_test():
        s = type("PyStack", (list, ), {})()
        s.push = s.append
        pushup(s, numt, maxh)

    @timeit
    def mystack_test():
        s = stack.Stack()
        pushup(s, numt, maxh)

    print "pystack: %s sec" % pystack_test()
    print "mystack: %s sec" % mystack_test()
    print "Perfomance test ends....\n"


if __name__ == '__main__':
    PERFOMANCE_TEST()
    LEAK_TEST()
