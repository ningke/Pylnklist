from lnklist import *

class Foo(object):
    def __init__(self, v):
        self.v = v
        self.lnode = ListEntry(self)
    def __str__(self):
        return str(self.v)


# Test lnklist. The last entry of list points back to the first (lhead).
lhead = ListEntry(None)
# Add 1 (lhead <-> 1 <-> ~) "~" means pointing back at lhead
a = Foo(1)
list_add(a.lnode, lhead)
# Add 2 (lhead <-> 2 <-> 1 <-> ~)
b = Foo(2)
list_add(b.lnode, lhead)
# Add 3 (lhead <-> 3 <-> 2 <-> 1 <-> ~)
c = Foo(3)
list_add(c.lnode, lhead)
# Insert 100 between 3 and 2
m = Foo(100)
list_add(m.lnode, c.lnode)

def find_value(x, start):
    ''' Find the Foo object whose ".v" value equals ''x'', starting from list
    entry ''start''. '''
    for e in list_next_iter(start):
        if e.data.v == x:
            return e.data
    return None

# find 100
e = find_value(100, lhead)
print "find 100 returns %s" % e

# Previous and next of 100
print "Previous of 100 is %s, Next of 100 is %s" % (e.lnode._prev.data, e.lnode._next.data)
# Previous and next of 3
e = c
print "Previous of 3 is %s, Next of 3 is %s" % (e.lnode._prev.data, e.lnode._next.data)

# find 101
print "find 101 returns %s" % find_value(101, lhead)

# Now print the list
for e in list_next_iter(lhead):
    print e.data
