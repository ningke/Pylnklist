# Linked List
    This is a Linux style linked list implementation. In fact, it is copied from
    Linux kernel's include/linux/list.h. For Linux kernel people, this will
    feel right at home. This performs much better than Python's built-in list
    for very large list and/or list where deletion/insert happens everywhere
    in the list. Advantages over Python's built-in list are:
       - Fast for non-tail insert and deletion. Cost is O(1)
       - Using the list_next_iter/list_prev_iter routines, you can delete
         an entry while iterating over the list.
    Of course, the biggest disadvantage is that list corruption may (or rather
    will) occur due to programming errors.

## License
GPL v2