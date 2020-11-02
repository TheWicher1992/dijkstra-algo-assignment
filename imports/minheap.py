class min_heap():
    def __init__(self):
        self.heap = []

    def insert(self, data, priority):
        self.heap.append(
            (data, priority)
        )

        if(len(self.heap) == 1):
            return

        
     
