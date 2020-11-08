class min_heap():
    def __init__(self):
        self.heap = [()]
        self.size = 0
        self.indexes = {}

    def insert(self, data, priority):
        self.heap.append(())

        self.size += 1
        hole = self.size

        while(hole > 1 and priority < self.heap[int(hole/2)][1]):
            self.heap[hole] = self.heap[int(hole / 2)]
            self.indexes[self.heap[int(hole / 2)][0]] = hole
            hole = int(hole / 2)

        self.heap[hole] = (data, priority)
        self.indexes[data] = hole

    def is_leaf(self, i):
        # print("called")
        if(2*i > self.size):
            return True
        return False

    def has_left(self, i):
        if(2*i <= self.size):
            return True
        return False

    def has_right(self, i):
        if(2*i + 1 <= self.size):
            return True
        return False

    def get_child_with_higher_p(self, hole):
        if(self.has_left(hole) and self.has_right(hole)):
            if(self.heap[2*hole][1] < self.heap[2*hole+1][1]):
                return 2*hole
            else:
                return 2*hole+1
        if(self.has_left(hole)):
            return 2*hole
        if(self.has_right(hole)):
            return 2*hole+1

    def decrease_key(self, data, priority, old_p):
        if(self.size == 0):
            return -1
        # for i in range(1, self.size):
        #     if(self.heap[i][0] == data):
        #         self.heap.pop(i)
        #         self.size -= 1
        #         break

        i = self.heap.index((data, old_p))
        self.heap.pop(i)
        self.size -= 1

        self.insert(data, priority)

    def delete_min(self):
        if(self.size == 0):
            return -1
        if(self.size == 1):
            self.size -= 1
            item = self.heap[1]
            self.heap.pop(1)
            return item
        item = self.heap[1]
        #print("ejected prt: ", item[1])
        self.heap[1] = self.heap[self.size]
        self.heap.pop(self.size)
        self.size -= 1

        hole = 1
        while ((hole * 2) <= self.size):
            child = self.get_child_with_higher_p(hole)
            if(self.heap[hole][1] > self.heap[child][1]):
                tmp = self.heap[hole]
                self.heap[hole] = self.heap[child]
                self.heap[child] = tmp
            hole = child

        return item

    def is_empty(self):
        return self.size == 0
