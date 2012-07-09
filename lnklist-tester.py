# testing lnklist module

from lnklist import *
import time
import random

class Foo(object):
    def __init__(self, v):
        self.v = v
        self.lnode = ListEntry(self)
    def __str__(self):
        return str(self.v)

def mk_lnklist(nentries):
    ''' Make a linked list of ''nentries'' '''
    lhead = ListEntry(None)
    # Keep track of list entries separately in a regular python list
    fvec = []
    for i in xrange(0, nentries):
        f = Foo(i)
        fvec.append(f)
        list_add_tail(f.lnode, lhead)
    return (lhead, fvec)

def walk_lnklist(lhead, cb=None):
    ''' Walk the list '''
    for e in list_next_iter(lhead):
        if cb:
            cb(e)

def del_head(lhead):
    ''' Delete a list entry from the "head" of list. Do this until list is
    empty '''
    while not list_empty(lhead):
        e = list_remove_head(lhead)

def mk_pylist(nentries):
    fvec = []
    pylist = []
    for i in xrange(0, nentries):
        f = Foo(i)
        f.idx = i # Need to keep track list index for random deletion
        fvec.append(f)
        pylist.append(f)
    return (pylist, fvec)


def timeit(func):
    s = time.clock()
    res = func()
    e = time.clock()
    return (e - s), res

class ListProf(object):
    def __init__(self, numentries):
        self.numentries = numentries

    def reinit(self):
        self.create_time = 0.0
        self.walk_time = 0.0
        self.delhead_time = 0.0
        self.randop_time = 0.0

    def __str__(self):
        return "Create %f Walk %f DelHead %f RandOp %f" % \
            (self.create_time, self.walk_time, self.delhead_time,
             self.randop_time)

    def prof_lnklist(self):
        ''' Profiles our linked list '''
        # Create
        self.create_time, (lhead, fvec) = \
            timeit(lambda : mk_lnklist(self.numentries))
        # Walk
        self.walk_time, dummy = timeit(lambda: walk_lnklist(lhead))
        # Delete head
        self.delhead_time, dummy = timeit(lambda: del_head(lhead))
        assert(list_empty(lhead))
        # Re-create the linked list
        for f in fvec:
            list_add_tail(f.lnode, lhead)
        # Random delete and insert at the end
        def randop(num):
            random.seed("seed")
            while num:
                i = random.randint(0, len(fvec) - 1)
                f = fvec[i]
                list_del(f.lnode)
                list_add_tail(f.lnode, lhead)
                num -= 1
        self.randop_time, dummy = timeit(lambda: randop(100000))

    def prof_pylist(self):
        ''' Profiles the Python list '''
        # Create
        self.create_time, (lhead, fvec) = \
            timeit(lambda : mk_pylist(self.numentries))
        # Walk
        def pywalk():
            for f in lhead:
                pass
        self.walk_time, dummy = timeit(pywalk)
        # Delete head
        def pydelhead():
            while len(lhead):
                lhead.pop(0)
        self.delhead_time, dummy = timeit(pydelhead)
        assert(len(lhead) == 0)
        # Re-create the linked list
        for f in fvec:
            lhead.append(f)
        # Random delete and insert at the end
        def randop(num):
            random.seed("seed")
            while num:
                i = random.randint(0, len(fvec) - 1)
                f = fvec[i]
                lhead.pop(f.idx)
                lhead.append(f)
                num -= 1
        self.randop_time, dummy = timeit(lambda: randop(100000))


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        rounds = int(sys.argv[1])
    else:
        rounds = 100000
    prof = ListProf(rounds)
    prof.prof_lnklist()
    print "Number of Rounds: %d" % rounds
    print "Linked List Profile result:\n%s" % prof
    prof.reinit()
    prof.prof_pylist()
    print "Python List Profile result:\n%s" % prof


#########################################################################
# Results on my laptop (Intel Core2 Duo CPU T6500 @ 2.10GHz, 3GB RAM
#
# me@mylaptop:~/path/util-modules$ python lnklist-tester.py 1000
#    Number of Rounds: 1000
#    Linked List Profile result:
#    Create 0.000000 Walk 0.000000 DelHead 0.010000 RandOp 0.400000
#    Python List Profile result:
#    Create 0.000000 Walk 0.000000 DelHead 0.000000 RandOp 0.290000
#
# me@mylaptop:~/path/util-modules $ python lnklist-tester.py 10000
#    Number of Rounds: 10000
#    Linked List Profile result:
#    Create 0.050000 Walk 0.000000 DelHead 0.020000 RandOp 0.500000
#    Python List Profile result:
#    Create 0.040000 Walk 0.000000 DelHead 0.030000 RandOp 0.610000
#
# me@mylaptop:~/path/util-modules$ python lnklist-tester.py 50000
#    Number of Rounds: 50000
#    Linked List Profile result:
#    Create 0.300000 Walk 0.010000 DelHead 0.090000 RandOp 0.540000
#    Python List Profile result:
#    Create 0.430000 Walk 0.000000 DelHead 0.880000 RandOp 1.780000
#
# me@mylaptop:~/path/util-modules$ python lnklist-tester.py 100000
#    Number of Rounds: 100000
#    Linked List Profile result:
#    Create 0.740000 Walk 0.030000 DelHead 0.190000 RandOp 0.530000
#    Python List Profile result:
#    Create 0.980000 Walk 0.010000 DelHead 3.240000 RandOp 3.540000
#
# me@mylaptop:~/path/util-modules$ python lnklist-tester.py 500000
#    Number of Rounds: 500000
#    Linked List Profile result:
#    Create 5.270000 Walk 0.170000 DelHead 0.930000 RandOp 0.520000
#    Python List Profile result:
#    Create 6.390000 Walk 0.040000 DelHead 454.610000 RandOp 98.520000
#
