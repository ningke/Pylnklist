##
# A linked list implementation based on that of Linux Kernel's:
#     include/linux/list.h
# This is useful if you have a very large list and/or need delete/insert
# in everywhere in the list, in which case, this linked list will perform
# much better than the built-in Python list.
#

class ListEntry(object):
    ''' A linked list entry. To use this linked list implementation, you
    need to embedded this object in your own object. '''
    def __init__(self, data):
        ''' Here ''data'' is usually an object (e.x., foo_obj), with one of
        its member being this ListEntry object (''self''). For example,
                foo_obj.listnode = ListEntry(foo_obj)
        In this case, a reference cycle forms. So be careful: don't define
        the "__del__" method for the "Foo" class, otherwise the foo_object will
        never be collected '''
        self.data = data
        self._prev = self
        self._next = self

def list_empty(lhead):
    ''' Is the list empty? '''
    return lhead._prev == lhead._next

def _list_init(lentry):
    ''' Initialize a list entry so it is empty '''
    lentry._prev = lentry
    lentry._next = lentry

def list_destroy(lentry):
    ''' Invalidate list entry ''lentry''. The result of this is that any
    reference cycle will be broken '''
    lentry.data = None
    lentry._prev = None
    lentry._next = None

def _list_add(lentry, p, n):
    ''' Add ''lentry'' between p and n. This is only useful if you already
    know the precise prev and next list entries. '''
    n._prev = lentry
    lentry._next = n
    lentry._prev = p
    p._next = lentry

def list_add(lentry, lhead):
    ''' Add a list entry right after list head '''
    _list_add(lentry, lhead, lhead._next)

def list_add_tail(lentry, lhead):
    ''' Add a list entry right before list head '''
    _list_add(lentry, lhead._prev, lhead)

def _list_del(lentry):
    ''' Internal list del function - doesn't reinit the _prev and _next fields.
    So they still refer the other entries in the list. Don't use this unless
    you will change those fields right away (as in list_move_) '''
    p = lentry._prev
    n = lentry._next
    p._next = n
    n._prev = p

def list_del(lentry):
    ''' Deletes list entry ''lentry'' from list. Note that list head is not
    needed '''
    _list_del(lentry)
    _list_init(lentry)

def list_move_head(lentry, lhead):
    ''' Deletes ''lentry'' from the list it's in currently in and moves it to
    the head of the another list ''lhead''. '''
    _list_del(lentry)
    list_add(lentry, lhead)

def list_move_tail(lentry, lhead):
    ''' Deletes ''lentry'' from the list it's in currently in and moves it to
    the tail of the another list ''lhead''. '''
    _list_del(lentry)
    list_add_tail(lentry, lhead)

def list_remove_head(lhead):
    ''' Removes first entry - Note if list is empty then this function does
    nothing'''
    if list_empty(lhead):
        raise ValueError("List Empty!")
    e = lhead._next
    list_del(e)
    return e

def list_remove_tail(lhead):
    ''' Removes last entry - Note if list is empty then this function does
    nothing'''
    if list_empty(lhead):
        raise ValueError("List Empty!")
    e = lhead._prev
    list_del(e)
    return e

def _list_iter(lentry, getnext):
    ''' list iterator - implemented as a generator. It is safe to delete
    an entry while using this iterator. '''
    # Start from the next item. ''next_item'' is saved before yield so even
    # if item is deleted from the list, iteration wouldn't be affected.
    next_item = getnext(lentry)
    while True:
        item = next_item
        next_item = getnext(next_item)
        if item == lentry:
            return
        yield item

def list_next_iter(lentry):
    ''' Forward iterator '''
    return _list_iter(lentry, lambda e: e._next)

def list_prev_iter(lentry):
    ''' Backward iterator '''
    return _list_iter(lentry, lambda e: e._prev)

