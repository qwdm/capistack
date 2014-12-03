import sys, os
import time
from multiprocessing import Process

sys.path.append('build/lib.linux-x86_64-2.7')
import stack


try:
	N_TESTS = int(sys.argv[1])
except IndexError:
	N_TESTS = 10

def leak_test():
        s = stack.Stack()
        for i in xrange(N_TESTS):
                for j in xrange(100):
                        s.push(i)
                for j in xrange(100):
                        s.pop()

test = Process(target=leak_test, args=())
test.start()

#watch = Process(target=os.system, args=("watch -n 1 free -h",))
#watch.start()

print "Test Process PID: %s" % test.pid
while test.is_alive():
        with open("/proc/%s/status" % test.pid) as f:
                line = [line for line in f.readlines() 
                             if "VmSize" in line][0]
                print line
        time.sleep(1)
        
        

#test.join()
print 'test ends'
