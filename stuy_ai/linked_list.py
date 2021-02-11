from typing import Generator, Generic, Iterable, Iterator, Optional, TypeVar
from collections import abc

T = TypeVar('T')


class Node(Generic[T]):
    data: T
    next: Optional['Node[T]']

    def __init__(self, data: T):
        self.data = data
        self.next = None

    def value(self) -> T:
        return self.data

    def attach_to(self, other:  Optional['Node[T]']) -> 'Node[T]':
        '''
        Point `self.next` to `other`, returns `self`
        '''
        self.next = other
        return self


class SLL(Generic[T], abc.Sequence):
    '''
    Singly linked list.
    '''
    head: Optional[Node[T]]
    tail: Optional[Node[T]]
    curr: Optional[Node[T]]
    _length: int

    def __init__(self, data_list: Optional[Iterable[T]] = None):
        '''
        If data_list is provided, it must be a list of values, and they are pushed one-by-one onto SLL.
        '''
        if data_list is None:
            self.head = None
            self.tail = None
            self.curr = None
            self._length = 0
        else:
            data_iter = iter(data_list)
            self.head = Node(next(data_iter))
            self.tail = self.head
            self._length = 1
            for data in data_iter:
                self.head = Node(data).attach_to(self.head)
                self._length += 1
            self.curr = self.head

            # self.tail = reduce(self._concat, map(
            # lambda data: Node(data), data_iter), self.head)

    def push(self, data: T):
        '''
        Adds a Node with data to the front of SLL, assume data is not None.
        '''
        node = Node(data)
        if self.head is None:
            self.head = self.tail = node
        else:
            self.head = node.attach_to(self.head)

        self._length += 1

    def pop(self) -> Optional[T]:
        '''
        If SLL is empty, returns None.  Else returns the data of the first Node, and removes the Node.
        '''
        if self._length == 0:
            return None
        else:
            node = self.head
            self.head = self.head.next
            node.next = None
            self._length -= 1
            return node.data

    def getFirst(self) -> Optional[T]:
        '''
        returns the data from the first Node, makes the first Node 'current', else None if SLL is empty
        '''
        self.curr = self.head
        return self.curr.data

    def getNext(self) -> Optional[T]:
        '''
        moves internally to the Node after 'current' (if possible), and returns its data, else None
            cannot be used after push() or pop() calls, only after getFirst() or getNext()
        '''
        if self.curr is None or self.curr.next is None:
            return None
        else:
            self.curr = self.curr.next
            return self.curr.data

    def length(self) -> int:
        '''
        returns number of Nodes in SLL
        '''
        return len(self)

    # standard compliant
    def __len__(self) -> int:
        return self._length

    def clear(self):
        '''
        empties SLL, returns None
        '''
        self.head = None
        self.tail = None
        self.curr = None
        self._length = 0

    def __iter__(self) -> Generator[T, None, None]:
        p = self.head
        while p is not None:
            yield p.data
            p = p.next
        # return SSLIterator(self.head)

    def __repr__(self) -> str:
        return f'SSL({list(self).__repr__()})'

    def __getitem__(self, key: int) -> T:
        if not (0 <= key < self._length):
            raise IndexError("Index out of bounds")
        p = self.head
        while key > 0:
            key -= 1
            p = p.next
        return p.data

# class SSLIterator(Generic[T], abc.Iterator):
#     curr: Optional[Node[T]]

#     def __init__(self, node: Optional[Node[T]]) -> None:
#         self.curr = node

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.curr is None:
#             raise StopIteration
#         else:
#             val = self.curr.data
#             self.curr = self.curr.next
#             return val
