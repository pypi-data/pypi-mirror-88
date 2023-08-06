from .Node import Node

class Stack:
    def __init__(self):
        self.head = None
        self.__size = 0

    def push(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node 
        self.__size += 1

    def pop(self):
      if(self.head == None): return None
      result = self.head.data
      nextNode = self.head.next
      self.head = nextNode
      self.__size -= 1
      return result

    def top(self):
      return self.head.data

    def empty(self): return self.head == None

    def clear(self): self.head = None

    @property
    def size(self): return self.__size

    def __repr__(self):
        if self.head == None: return "[]"
        nextNode = self.head
        result = "["
        while not nextNode.next == None:
            result += str(nextNode.data) + ", "
            nextNode = nextNode.next
        result += str(nextNode.data) + "]"
        return result