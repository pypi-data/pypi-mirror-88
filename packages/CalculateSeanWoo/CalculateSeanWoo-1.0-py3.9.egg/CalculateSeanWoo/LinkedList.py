from .Node import Node

class LindedList:
    def __init__(self):
        self.head = None
        self.__size = 0

    def add(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node 
        self.__size += 1
    
    def append(self, item):
        node = Node(item)
        if(self.head == None): 
            self.head = node
            self.__size += 1
            return

        nextNode = self.head
        while not nextNode.next == None:
            nextNode = nextNode.next

        nextNode.next = node
        self.__size += 1

    def get_first(self):
        if(self.head == None): return None
        return self.head.data

    def remove_first(self):
        if(self.head == None): return None
        result = self.head.data
        self.remove(self.head.data)
        return result

    def get_last(self):
        if(self.head == None): return None

        nextNode = self.head
        while not nextNode.next == None:
            nextNode = nextNode.next
        return nextNode.data
        
    def remove_last(self):
        if(self.head == None): return None

        nextNode = self.head
        lastNode = None
        while not nextNode.next == None:
            lastNode = nextNode
            nextNode = nextNode.next
        result = nextNode.data
        lastNode.next = None
        self.__size -= 1
        return result

    def insert(self, item, position):
        if(self.head == None): return
        if(not self.size > position): return
        if(position == 0):
            self.add(item)
            return
        if(position == self.size - 1):
            self.append(item)
            return
        counter = 0
        node = Node(item)

        lastNode = self.head
        nextNode = self.head
        while not nextNode.next == None:
            if(position == counter):
                node.next = nextNode
                lastNode.next = node
                self.__size += 1
                return
            counter += 1
            lastNode = nextNode
            nextNode = nextNode.next

    def delete(self, position):
        if(self.head == None): return
        if(not self.size > position): return
        if(position == 0):
            self.remove_first()
            return
        counter = 0

        lastNode = self.head
        nextNode = self.head
        while not nextNode.next == None:
            if(position == counter):
                lastNode.next = nextNode.next
                self.__size -= 1
                return
            counter += 1
            lastNode = nextNode
            nextNode = nextNode.next
        
        if(position == counter):
            lastNode.next = None
            self.__size -= 1
            return

    def empty(self):
        return self.head == None

    def search(self, item):
        if(self.head == None): return False

        nextNode = self.head
        while not nextNode.next == None:
            if nextNode.data == item:
                return True
            nextNode = nextNode.next
        if nextNode.data == item:
            return True
        return False

    def remove(self, item):
        if(self.head == None): return

        lastNode = None
        nextNode = self.head
        if nextNode.data == item:
            self.head = nextNode.next
            self.__size -= 1
            return
        while not nextNode.next == None:
            if nextNode.data == item:
                lastNode.next = nextNode.next
                self.__size -= 1
                return
            lastNode = nextNode
            nextNode = nextNode.next
        if nextNode.data == item:
            lastNode.next = None
            self.__size -= 1
        

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